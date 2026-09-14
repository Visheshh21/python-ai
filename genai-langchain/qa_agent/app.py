import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from google.cloud import bigquery

from main import run_agent
from tools import AGENT_STATE

app = FastAPI(title="AI Auditor QA API")

class AuditRequest(BaseModel):
    limit: Optional[int] = None
    dealerships: List[str] = []
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    custom_categories: str = "Normal / No Issue"

@app.post("/api/audit")
def run_audit(req: AuditRequest):
    try:
        # Save audit configuration to AGENT_STATE
        AGENT_STATE["audit_config"] = {
            "dealerships": req.dealerships,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "custom_categories": req.custom_categories,
            "limit": req.limit
        }

        # Construct the user prompt dynamically
        dealership_text = ", ".join(req.dealerships) if req.dealerships else "all dealerships"
        if req.start_date and req.end_date:
            date_text = f" from {req.start_date} to {req.end_date}"
            effective_end = req.end_date
        elif req.start_date:
            date_text = f" for date {req.start_date}"
            effective_end = req.start_date
        elif req.end_date:
            date_text = f" up to {req.end_date}"
            effective_end = req.end_date
        else:
            date_text = ""
            effective_end = None

        limit_text = f"Fetch EXACTLY {req.limit} calls" if req.limit else "Fetch ALL calls"
        prompt = (
            f"{limit_text} for {dealership_text}{date_text}. "
            f"Ensure fetch_calls uses dealerships={req.dealerships or None}, start_date={repr(req.start_date)}, end_date={repr(effective_end)}, limit={req.limit}. "
            f"Categorize each one using the custom categories configured. "
            f"Store the results, and give me an executive summary starting with a Markdown table for metrics, followed by latency analysis and recommendations."
        )
        
        # Run the LangGraph agent synchronously
        markdown_summary = run_agent(prompt)
        
        # Read the generated CSV file
        csv_path = "categorized_calls_export.csv"
        calls_data = []
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Replace all NaN, NaT, and infinity with empty strings or None for safe JSON encoding
            df = df.replace({float('nan'): None, float('inf'): None, float('-inf'): None})
            df = df.where(pd.notnull(df), None)
            calls_data = df.to_dict(orient="records")
            
        return {
            "summary": markdown_summary,
            "calls": calls_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/progress")
def get_progress():
    return AGENT_STATE.get("progress", {"current": 0, "total": 0})

@app.get("/api/dealerships")
def get_dealerships():
    try:
        bq_client = bigquery.Client()
        query = "SELECT DISTINCT agent_name FROM `fir-test-7d4bb.dialogflow_test_v3.unified_conversation_outcomes` WHERE agent_name IS NOT NULL ORDER BY agent_name"
        results = bq_client.query(query).result()
        dealerships = [row.agent_name for row in results]
        return dealerships
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (this serves index.html at /)
os.makedirs("static", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
