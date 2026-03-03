from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
import google.generativeai as genai
import json
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    description: str

def clean_json_response(text: str) -> str:
    text = text.strip()
    if text.startswith("```json"): text = text[7:]
    elif text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    return text.strip()

@app.post("/api/generate")
async def generate_brd(request: GenerateRequest):
    desc_text = request.description.lower()
    
    prompt = f"""
    You are an expert Business Analyst. Convert the provided business description into a strictly structured JSON Business Requirements Document (BRD). 
    The JSON must contain exactly these keys: `business_overview`, `stakeholders`, `capabilities`, `requirements` (array of objects with `id` like "r-001" and `description`), and `assumptions`.
    CRITICAL RULE: If the input text mentions the word "upload", you MUST explicitly include an ingestion capability within the `requirements` array.
    Output ONLY valid, raw JSON. Use lowercase text everywhere.
    Input Description: {desc_text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        brd_data = json.loads(clean_json_response(response.text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    has_upload = "upload" in desc_text
    has_ingestion = any("ingest" in req.get("description", "").lower() for req in brd_data.get("requirements", []))

    if has_upload and not has_ingestion:
        raise HTTPException(status_code=422, detail="Validation Failed: 'upload' found in description but no ingestion requirement generated.")

    api_intents = []
    for req in brd_data.get("requirements", []):
        req_desc = req.get("description", "").lower()
        if "upload" in req_desc or "ingest" in req_desc:
            api_intents.append({"intent": "file upload / document ingestion api", "requirement_id": req["id"]})
        elif "review" in req_desc or "comment" in req_desc:
            api_intents.append({"intent": "comment / review submission api", "requirement_id": req["id"]})
        elif "symptom" in req_desc:
            api_intents.append({"intent": "submit symptoms api", "requirement_id": req["id"]})
        elif "risk assessment" in req_desc:
             api_intents.append({"intent": "fetch risk assessment api", "requirement_id": req["id"]})

    return {
        "brd": brd_data,
        "api_intents": api_intents,
        "validation": {"status": "passed", "message": "Validation passed."}
    }
