"""
tools.py - Agent Tools (The Actions the LLM Can Take)
======================================================

In LangGraph, a "tool" is just a Python function decorated with @tool.
The LLM reads the function's docstring and parameter types to understand
WHAT the tool does and WHEN to use it.
"""

import json
from collections import Counter
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas as pd

from schema import create_dynamic_categorization_schema
import re

load_dotenv()

# ─────────────────────────────────────────────────
# SHARED STATE
# ─────────────────────────────────────────────────
# We use a shared state dictionary so that the tools don't have to pass 
# massive raw transcripts through the LLM's JSON arguments. Passing massive 
# JSON strings via tool arguments can cause "Failed to parse tool call arguments" 
# errors in smaller LLMs.
AGENT_STATE = {
    "raw_calls": [],
    "categorized_calls": [],
    "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
}

# ─────────────────────────────────────────────────
# Tool 1: Fetch Calls (Data Source)
# ─────────────────────────────────────────────────
@tool
def fetch_calls(dealerships: list[str] = None, start_date: str = None, end_date: str = None, limit: int = None) -> str:
    """Fetches real call transcripts from the BigQuery outcomes table using provided filters.
    
    Args:
        dealerships: Optional list of dealership agent_names to filter by.
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.
        limit: Maximum number of calls to fetch. Defaults to 5.
    """
    bq_client = bigquery.Client()
    
    base_query = """
        SELECT conversation_id, conversation_transcript, conversation_summary, agent_name 
        FROM `fir-test-7d4bb.dialogflow_test_v3.unified_conversation_outcomes`
        WHERE current_conversation_outcome != 'Calls Resolved'
        AND conversation_transcript IS NOT NULL
    """
    
    conditions = []
    job_config = bigquery.QueryJobConfig()
    query_params = []
    
    if dealerships and len(dealerships) > 0:
        conditions.append("agent_name IN UNNEST(@dealerships)")
        query_params.append(bigquery.ArrayQueryParameter("dealerships", "STRING", dealerships))
        
    if start_date:
        conditions.append("start_date_local >= @start_date")
        query_params.append(bigquery.ScalarQueryParameter("start_date", "STRING", start_date))
        
    if end_date:
        conditions.append("start_date_local <= @end_date")
        query_params.append(bigquery.ScalarQueryParameter("end_date", "STRING", end_date))
        
    if conditions:
        base_query += " AND " + " AND ".join(conditions)
        
    if limit is not None:
        base_query += f" LIMIT {limit}"
    
    job_config.query_parameters = query_params
    
    results = bq_client.query(base_query, job_config=job_config).result()
    
    # Map to our standard dictionary format
    calls = [{"call_id": row.conversation_id, "transcript": row.conversation_transcript, "summary": row.conversation_summary, "agent_name": row.agent_name} for row in results]
    
    AGENT_STATE["raw_calls"] = calls
    return f"Successfully fetched {len(AGENT_STATE['raw_calls'])} real calls from BigQuery. They are saved in internal state ready to be categorized."


# ─────────────────────────────────────────────────
# Tool 2: Categorize Calls (The LLM Structured Output)
# ─────────────────────────────────────────────────
@tool
def categorize_calls() -> str:
    """Categorizes the raw calls that were previously fetched.
    
    Reads from the internal state, categorizes each one, and saves results back to state.
    """
    calls = AGENT_STATE["raw_calls"]
    if not calls:
        return "No raw calls found. You must fetch calls first."

    llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.1, max_tokens=None)
    
    # Get custom categories from state (comma separated)
    custom_categories_text = AGENT_STATE.get("audit_config", {}).get("custom_categories", "Normal / No Issue")
    
    # Parse by comma
    category_names = []
    for part in custom_categories_text.split(','):
        clean_name = part.strip()
        if clean_name and clean_name not in category_names:
            category_names.append(clean_name)
            
    if "Normal / No Issue" not in category_names:
        category_names.append("Normal / No Issue")
        
    DynamicCallCategorization = create_dynamic_categorization_schema(category_names)
    evaluator = llm.with_structured_output(DynamicCallCategorization, include_raw=True)
    
    categorized = []
    total = len(calls)
    
    # Initialize progress state for the UI
    AGENT_STATE["progress"] = {"current": 0, "total": total}
    
    print(f"\n⚙️ Starting categorization for {total} calls...")
    
    for i, call in enumerate(calls, 1):
        print(f"   [{i}/{total}] Analyzing Call ID: {call['call_id']} ...", end=" ", flush=True)
        
        # Update progress state for the UI
        AGENT_STATE["progress"]["current"] = i
        
        prompt = f"""Analyze this customer service AI conversation transcript and categorize its behavior based strictly on these specific defects:

{custom_categories_text}

Call ID: {call['call_id']}
Transcript:
{call['transcript']}"""
        try:
            result = evaluator.invoke(prompt)
            
            parsed = result["parsed"]
            raw = result["raw"]
            
            # Track Tokens
            usage = raw.response_metadata.get("token_usage", {})
            AGENT_STATE["token_usage"]["prompt_tokens"] += usage.get("prompt_tokens", 0)
            AGENT_STATE["token_usage"]["completion_tokens"] += usage.get("completion_tokens", 0)
            AGENT_STATE["token_usage"]["total_tokens"] += usage.get("total_tokens", 0)
            
            # Inject the pre-existing data from BigQuery
            final_data = parsed.model_dump()
            final_data["call_id"] = call["call_id"]
            final_data["agent_name"] = call["agent_name"]
            final_data["summary"] = call["summary"]
            final_data["transcript"] = call["transcript"]
            
            categorized.append(final_data)
            print("Done ✅")
        except Exception as e:
            print(f"Failed ❌ (Error: {e})")
        
    AGENT_STATE["categorized_calls"] = categorized
    return f"Successfully categorized {len(categorized)} calls. Ready to store or generate metrics."


# ─────────────────────────────────────────────────
# Tool 3: Store Results (Database Write)
# ─────────────────────────────────────────────────
@tool
def store_results() -> str:
    """Saves the categorized call results to a local CSV file."""
    categorized = AGENT_STATE["categorized_calls"]
    if not categorized:
        return "No categorized calls found to store."
        
    df = pd.DataFrame(categorized)
    output_file = "categorized_calls_export.csv"
    df.to_csv(output_file, index=False)
    
    return f"Successfully saved {len(categorized)} categorized calls to local CSV file: {output_file}"


# ─────────────────────────────────────────────────
# Tool 4: Generate Metrics Summary
# ─────────────────────────────────────────────────
@tool
def generate_metrics() -> str:
    """Computes quantitative metrics from categorized call data."""
    categorized = AGENT_STATE["categorized_calls"]
    if not categorized:
        return "No categorized calls found to generate metrics for."
        
    total = len(categorized)
    categories = dict(Counter(c["category"] for c in categorized))
    sentiments = dict(Counter(c["sentiment"] for c in categorized))
    resolutions = dict(Counter(c["resolution"] for c in categorized))
    
    metrics = {
        "total_calls_analyzed": total,
        "category_breakdown": categories,
        "sentiment_breakdown": sentiments,
        "resolution_breakdown": resolutions
    }
    
    return json.dumps(metrics, indent=2)


# Export the list of tools for the agent to use
ALL_TOOLS = [fetch_calls, categorize_calls, store_results, generate_metrics]
