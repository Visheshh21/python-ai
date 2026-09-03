"""
main.py - Entry Point to Run the QA Agent
==========================================

Run this file to interact with the agent:
    python main.py

The agent will process the sample call transcripts, categorize them,
store the results (mock), and give you an executive summary.

You can also modify the prompt at the bottom to ask different questions,
for example:
    - "Fetch 3 calls and only categorize them, don't store."
    - "How many calls were about billing issues?"
    - "Show me only the frustrated customers."
"""

from langchain_core.messages import HumanMessage
from agent import qa_agent


def run_agent(user_message: str):
    """Sends a message to the QA agent and prints the response.
    
    Args:
        user_message: The natural language instruction for the agent.
    """
    print("=" * 60)
    print("🎯 USER REQUEST:")
    print(f"   {user_message}")
    print("=" * 60)
    print("\n⏳ Agent is working...\n")

    response = qa_agent.invoke({
        "messages": [HumanMessage(content=user_message)]
    })

    # The last message in the response is the agent's final answer
    final_answer = response["messages"][-1].content
    
    # ── AGGREGATE TOKENS ──
    from tools import AGENT_STATE
    orchestration_tokens = {"prompt": 0, "completion": 0, "total": 0}
    
    for msg in response["messages"]:
        if hasattr(msg, "response_metadata") and "token_usage" in msg.response_metadata:
            usage = msg.response_metadata["token_usage"]
            orchestration_tokens["prompt"] += usage.get("prompt_tokens", 0)
            orchestration_tokens["completion"] += usage.get("completion_tokens", 0)
            orchestration_tokens["total"] += usage.get("total_tokens", 0)
            
    total_prompt = orchestration_tokens["prompt"] + AGENT_STATE["token_usage"]["prompt_tokens"]
    total_completion = orchestration_tokens["completion"] + AGENT_STATE["token_usage"]["completion_tokens"]
    grand_total = orchestration_tokens["total"] + AGENT_STATE["token_usage"]["total_tokens"]

    print("\n" + "=" * 60)
    print("📊 AGENT RESPONSE:")
    print("=" * 60)
    try:
        print(final_answer)
    except UnicodeEncodeError:
        print(final_answer.encode('ascii', 'replace').decode('ascii'))
    
    print("\n" + "=" * 60)
    print("🪙 TOTAL TOKEN USAGE:")
    print("=" * 60)
    print(f"Prompt Tokens:     {total_prompt}")
    print(f"Completion Tokens: {total_completion}")
    print(f"Grand Total:       {grand_total}")

    return final_answer


if __name__ == "__main__":

    # ── Example 1: Full Pipeline ──
    # The agent will: fetch → categorize → store → compute metrics → summarize
      run_agent(
        "Fetch 5 calls, categorize each one, store the results, "
        "and give me an executive summary with metrics and recommendations."
    )

    # ── Example 2: Selective Query (uncomment to try) ──
    # run_agent("Fetch 3 calls and categorize them. Don't store anything. Just show me the categories.")

    # ── Example 3: Specific Analysis (uncomment to try) ──
    # run_agent("Fetch all calls and categorize them. How many are billing issues? What are customers angry about?")
