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
        date_text = f" from {req.start_date} to {req.end_date}" if req.start_date and req.end_date else ""
        prompt = f"Fetch {req.limit} calls for {dealership_text}{date_text}, categorize each one using the custom categories configured, store the results, and give me an executive summary with metrics and recommendations."
        
        # Run the LangGraph agent synchronously
        markdown_summary = run_agent(prompt)
        
        # Read the generated CSV file
        csv_path = "categorized_calls_export.csv"
        calls_data = []
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Fill NaN values with empty string to prevent JSON serialization errors
            df = df.fillna("")
            calls_data = df.to_dict(orient="records")
            
        return {
            "summary": markdown_summary,
            "calls": calls_data
        }
    except Exception as e:
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
