import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from main import run_agent

app = FastAPI(title="AI Auditor QA API")

class AuditRequest(BaseModel):
    limit: int = 5

@app.post("/api/audit")
def run_audit(req: AuditRequest):
    try:
        # Construct the user prompt dynamically
        prompt = f"Fetch {req.limit} calls, categorize each one, store the results, and give me an executive summary with metrics and recommendations."
        
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

from tools import AGENT_STATE

@app.get("/api/progress")
def get_progress():
    return AGENT_STATE.get("progress", {"current": 0, "total": 0})

# Mount static files (this serves index.html at /)
os.makedirs("static", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
