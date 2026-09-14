"""
tools.py - Agent Tools (The Actions the LLM Can Take)
======================================================

In LangGraph, a "tool" is just a Python function decorated with @tool.
The LLM reads the function's docstring and parameter types to understand
WHAT the tool does and WHEN to use it.
"""

import json
import time
from collections import Counter
from langchain_core.tools import tool
import os
from langchain_google_genai import ChatGoogleGenerativeAI
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
        limit: Maximum number of calls to fetch. Must specify the user's requested limit.
    """
    cfg = AGENT_STATE.get("audit_config", {})
    if not dealerships and cfg.get("dealerships"):
        dealerships = cfg.get("dealerships")
    if not start_date and cfg.get("start_date"):
        start_date = cfg.get("start_date")
    if not end_date and cfg.get("end_date"):
        end_date = cfg.get("end_date")
        
    # If single date provided (start_date without end_date), audit that specific day
    if start_date and not end_date:
        end_date = start_date
    if limit is None and cfg.get("limit"):
        limit = cfg.get("limit")

    print(f"\n[FETCH] Fetching calls from BigQuery (dealerships={dealerships}, start_date={start_date}, end_date={end_date}, limit={limit})...")
    bq_client = bigquery.Client()
    
    base_query = """
        SELECT conversation_id, conversation_transcript, conversation_summary, agent_name, start_date_local 
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
        query_params.append(bigquery.ScalarQueryParameter("start_date", "DATE", str(start_date).strip()))
        
    if end_date:
        conditions.append("start_date_local <= @end_date")
        query_params.append(bigquery.ScalarQueryParameter("end_date", "DATE", str(end_date).strip()))
        
    if conditions:
        base_query += " AND " + " AND ".join(conditions)
        
    base_query += " ORDER BY start_date_local DESC"

    if limit is not None:
        base_query += f" LIMIT {limit}"
    
    job_config.query_parameters = query_params
    
    results = bq_client.query(base_query, job_config=job_config).result()
    
    # Map to our standard dictionary format
    calls = [{"call_id": row.conversation_id, "transcript": row.conversation_transcript, "summary": row.conversation_summary, "agent_name": row.agent_name, "timestamp": str(row.start_date_local) if row.start_date_local else ""} for row in results]
    
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

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    llm = ChatGoogleGenerativeAI(
        model=gemini_model,
        google_api_key=api_key,
        temperature=0.1
    )
    
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

IMPORTANT RULES:
1. LATENCY: Check the timestamps in the transcript. If you encounter any instance where the delay between the caller's turn and the agent's turn is 20 seconds or more, you MUST set `has_high_latency` to True. Otherwise, set it to False.
2. ESCALATIONS: If a call is escalated to a human agent, you must ONLY consider the transcript up until the exact point of escalation. Any conversation or latency that occurs after the escalation is irrelevant and should be ignored for both categorization and latency tagging.

Call ID: {call['call_id']}
Transcript:
{call['transcript']}"""
        max_retries = 5
        for attempt in range(max_retries):
            try:
                result = evaluator.invoke(prompt)
                break  # Success — exit retry loop
            except Exception as e:
                error_str = str(e)
                if ("429" in error_str or "ResourceExhausted" in error_str or "RetryInfo" in error_str) and attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1s, 2s, 4s, 8s, 16s
                    print(f"\n      ⏳ Rate limited. Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...", end=" ", flush=True)
                    time.sleep(wait_time)
                else:
                    print(f"Failed ❌ (Error: {e})")
                    break  # Non-retryable error or max retries hit
        else:
            # All retries exhausted
            print(f"Failed ❌ (Max retries exceeded)")
            continue  # Skip this call
        
        if 'result' not in dir():
            continue
            
        try:
            parsed = result["parsed"]
            raw = result["raw"]
            
            # Track Tokens
            usage = getattr(raw, "usage_metadata", None)
            if not usage and hasattr(raw, "response_metadata"):
                usage = raw.response_metadata.get("token_usage", {})
            if usage:
                prompt_toks = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                completion_toks = usage.get("completion_tokens") or usage.get("output_tokens") or 0
                total_toks = usage.get("total_tokens") or (prompt_toks + completion_toks)
                AGENT_STATE["token_usage"]["prompt_tokens"] += prompt_toks
                AGENT_STATE["token_usage"]["completion_tokens"] += completion_toks
                AGENT_STATE["token_usage"]["total_tokens"] += total_toks
            
            # Inject the pre-existing data from BigQuery
            final_data = parsed.model_dump()
            final_data["call_id"] = call["call_id"]
            final_data["agent_name"] = call["agent_name"]
            final_data["timestamp"] = call["timestamp"]
            final_data["summary"] = call["summary"]
            final_data["transcript"] = call["transcript"]
            
            categorized.append(final_data)
            AGENT_STATE["categorized_calls"] = categorized
            # Progressively update CSV so results are never lost if interrupted
            try:
                pd.DataFrame(categorized).to_csv("categorized_calls_export.csv", index=False)
            except Exception:
                pass
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
    high_latency_count = sum(1 for c in categorized if c.get("has_high_latency", False))
    
    metrics = {
        "total_calls_analyzed": total,
        "calls_with_high_latency_above_20s": high_latency_count,
        "category_breakdown": categories,
        "sentiment_breakdown": sentiments,
        "resolution_breakdown": resolutions
    }
    
    return json.dumps(metrics, indent=2)


# Export the list of tools for the agent to use
ALL_TOOLS = [fetch_calls, categorize_calls, store_results, generate_metrics]
