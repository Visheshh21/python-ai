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

from langchain_groq import ChatGroq
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
llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    temperature=0,         # 0 = deterministic, no randomness in tool selection
    max_tokens=None
)


SYSTEM_PROMPT = """You are a Lead QA Engineering Agent specializing in auditing Conversational AI and Virtual Agents.
Your objective is to ingest customer service transcripts and detect highly specific behavioral defects in the AI's logic, routing, and responsiveness.

You have access to 4 tools. You must use them in this exact sequence unless the user explicitly requests otherwise:
1. `fetch_calls` - Retrieves real call transcripts from BigQuery (specifically for Morehead Honda).
2. `categorize_calls` - Analyzes every transcript and maps the AI's behavior to one of the strict defect categories (or Normal).
3. `store_results` - Exports the categorized results to a local CSV file for external dashboarding.
4. `generate_metrics` - Computes the quantitative breakdown of the AI's defects.

OUTPUT FORMAT:
After running the full pipeline, you must synthesize the metrics and your observations into a highly professional Executive Summary using Markdown. 

Your Executive Summary MUST include:
# AI Performance Audit Report

## Quantitative Breakdown
- Total Calls Audited: [Number]
- Defect Rate: [Percentage of calls that were NOT 'Normal / No Issue']
- [List each defect category with exact counts and percentages]

## Critical Defect Analysis
For each defect category that appeared (e.g., Erroneous Cancellations, Severe Responsiveness Failures, etc.), write a short paragraph explaining the context. Give specific examples of what the AI did wrong based on the summaries.

## Actionable Engineering Recommendations
Provide 2-3 highly specific, technical recommendations for the prompt engineering or dialog flow team to fix these defects. (e.g., "Implement a strict intent-recognition timeout of 5 seconds," or "Update the cancellation prompt to require explicit double-opt-in before dropping the appointment block.")

CRITICAL RULES:
- Be objective and data-driven.
- Do NOT hallucinate defects. If a call is 'Normal / No Issue', treat it as a success.
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
