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

from pydantic import BaseModel, Field, create_model
from typing import Literal

def create_dynamic_categorization_schema(category_names: list[str]):
    """Creates a Pydantic model for CallCategorization dynamically at runtime.
    
    By dynamically creating this model, we can enforce that the LLM's `category`
    output must be one of the dynamically generated categories provided by the user.
    """
    if not category_names:
        # Fallback if somehow no categories were parsed
        CatLiteral = str
    else:
        # Create a Literal type from the list of categories
        CatLiteral = Literal[tuple(category_names)]
    
    return create_model(
        'CallCategorization',
        call_id=(str, Field(description="The unique identifier for this call")),
        category=(CatLiteral, Field(description="The primary category of the AI behavior during the call. Must be exactly one of the options.")),
        sentiment=(Literal["Positive", "Neutral", "Frustrated", "Angry"], Field(description="The emotional tone of the customer during the call.")),
        resolution=(Literal["Resolved", "Unresolved", "Escalated"], Field(description="Whether the customer's primary issue was resolved, remained unresolved, or was escalated to a human.")),
        key_issues=(list[str], Field(description="List of 1-3 specific issues the customer raised")),
        has_high_latency=(bool, Field(description="True if the transcript timestamps indicate any delay of 20 seconds or more between the caller's turn and the agent's turn. False otherwise.")),
        __doc__="Schema for a single categorized call."
    )
