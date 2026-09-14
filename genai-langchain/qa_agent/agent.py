"""
agent.py - The LangGraph Agent Definition
==========================================

This is the heart of the application. It creates a ReAct agent that:
1. Has access to 4 tools (fetch, categorize, store, metrics)
2. Uses an LLM to decide WHICH tools to call and in WHAT ORDER
3. Loops until the LLM decides it has enough info to give a final answer

Architecture:
    ┌─────────────────────────────────────────────┐
    │                                             │
    │   User Prompt                               │
    │       │                                     │
    │       ▼                                     │
    │   ┌───────┐    tool call    ┌───────────┐   │
    │   │  LLM  │ ─────────────► │   Tools   │   │
    │   │       │ ◄───────────── │           │   │
    │   └───┬───┘   observation   └───────────┘   │
    │       │                                     │
    │       │ (loops until done)                  │
    │       ▼                                     │
    │   Final Answer                              │
    │                                             │
    └─────────────────────────────────────────────┘

Key Concept (ReAct Pattern):
    ReAct = Reasoning + Acting
    
    The LLM "thinks out loud" about what to do (Reasoning),
    then calls a tool (Acting), reads the result (Observing),
    and repeats until it can give a final answer.
    
    Example loop:
        1. LLM thinks: "The user wants me to analyze calls. First I need to fetch them."
        2. LLM calls: fetch_calls(limit=6)
        3. LLM observes: [... 6 call transcripts ...]
        4. LLM thinks: "Now I need to categorize these."
        5. LLM calls: categorize_calls(calls_json=...)
        6. LLM observes: [... 6 categorized results ...]
        7. LLM thinks: "User also asked me to store them."
        8. LLM calls: store_results(categorized_json=...)
        9. LLM observes: "Successfully saved 6 calls."
        10. LLM thinks: "Now I need metrics for the summary."
        11. LLM calls: generate_metrics(categorized_json=...)
        12. LLM observes: {metrics...}
        13. LLM gives final answer with the executive summary.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

from tools import ALL_TOOLS

load_dotenv()


# ─────────────────────────────────────────────────
# 1. Initialize the LLM (The "Brain" of the Agent)
# ─────────────────────────────────────────────────
# This is the LLM that DECIDES which tools to call.
# It needs to be a strong reasoning model — it's the orchestrator.
# (The categorization tool internally uses its own LLM for structured output)
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

llm = ChatGoogleGenerativeAI(
    model=gemini_model,
    google_api_key=api_key,
    temperature=0
)


SYSTEM_PROMPT = """You are a Lead QA Engineering Agent specializing in auditing Conversational AI and Virtual Agents.
Your objective is to ingest customer service transcripts and detect behavioral defects in the AI's logic, routing, and responsiveness according to the user's specific instructions.

You have access to 4 tools. You must use them in this exact sequence unless the user explicitly requests otherwise:
1. `fetch_calls` - Retrieves real call transcripts from BigQuery.
2. `categorize_calls` - Analyzes every transcript and maps the AI's behavior to one of the strict defect categories provided in your prompt.
3. `store_results` - Exports the categorized results to a local CSV file for external dashboarding.
4. `generate_metrics` - Computes the quantitative breakdown of the AI's defects.

OUTPUT FORMAT:
After running the full pipeline, you must synthesize the metrics and your observations into a highly professional Executive Summary using Markdown. 

Your Executive Summary MUST include:
# AI Performance Audit Report

## Quantitative Breakdown
Create a clear, clean Markdown table presenting all metric categories and the high latency count returned from generate_metrics. The table must look like this:
| Metric / Defect Category | Count | Percentage |
|---|---|---|
| Total Calls Audited | [Number] | 100% |
| Overall Defect Rate | [Number] | [Percentage] |
| Calls with > 20s Latency | [Number] | [Percentage] |
| [Category 1] | [Number] | [Percentage] |
| [Category 2] | [Number] | [Percentage] |

## Critical Defect Analysis
For each defect category that appeared, write a short paragraph explaining the context. Give specific examples of what the AI did wrong based on the summaries. Also include a brief analysis of the high latency calls if any were found.

## Actionable Engineering Recommendations
Provide 2-3 highly specific, technical recommendations for the prompt engineering or dialog flow team to fix these defects.

CRITICAL RULES:
- Be objective and data-driven.
- Do NOT hallucinate defects. If a call is 'Normal / No Issue', treat it as a success.
- Ensure the table correctly incorporates the `calls_with_high_latency_above_20s` metric generated by the tool.
- If a tool fails or returns an error, explain the error gracefully to the user and stop execution.
"""


# ─────────────────────────────────────────────────
# 3. Create the LangGraph ReAct Agent
# ─────────────────────────────────────────────────
# create_react_agent builds the full graph for you:
#   START → LLM → (tool call?) → Tool → LLM → (tool call?) → ... → END
#
# It handles:
#   - The tool calling loop automatically
#   - Parsing tool call requests from the LLM
#   - Feeding tool results back to the LLM
#   - Stopping when the LLM gives a final text response (no more tool calls)

qa_agent = create_react_agent(
    model=llm,
    tools=ALL_TOOLS,
    prompt=SYSTEM_PROMPT
)
