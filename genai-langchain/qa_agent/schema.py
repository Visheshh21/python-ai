"""
schema.py - Pydantic Models for Structured LLM Output
=====================================================

This file defines the EXACT shape of data the LLM must return.
By using Pydantic models with `Literal` types, we force the LLM
to pick from a fixed set of categories — no hallucinated labels.

Key Concept:
    When you call `llm.with_structured_output(SomeModel)`,
    LangChain tells the LLM: "Your response MUST be valid JSON
    that matches this schema." If it doesn't, it retries automatically.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class CallCategorization(BaseModel):
    """Schema for a single categorized call.
    
    The LLM will return one of these for every transcript it processes.
    The `Literal` type locks the model into exactly 4 choices.
    """

    call_id: str = Field(
        description="The unique identifier for this call"
    )

    category: Literal[
        "Ignoring and Suppressing Escalation Requests",
        "Severe Responsiveness Failures",
        "Erroneous Cancellations",
        "Normal / No Issue"
    ] = Field(
        description="The primary category of the AI behavior during the call. Must be exactly one of the 4 options."
    )

    sentiment: Literal["Positive", "Neutral", "Frustrated", "Angry"] = Field(
        description="The emotional tone of the customer during the call."
    )

    resolution: Literal["Resolved", "Unresolved", "Escalated"] = Field(
        description="Whether the customer's primary issue was resolved, remained unresolved, or was escalated to a human."
    )

    key_issues: list[str] = Field(
        description="List of 1-3 specific issues the customer raised"
    )
