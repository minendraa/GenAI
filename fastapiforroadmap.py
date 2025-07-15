from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import json
from datetime import datetime

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("Rakesh_GOOGLE_API_KEY"))

# Define FastAPI app
app = FastAPI(title="IT Roadmap Generator")

# Define request schema
class PromptRequest(BaseModel):
    profession: str

@app.post("/roadmap")
def generate_roadmap(request: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        current_time = datetime.now().isoformat()

        full_prompt = f"""
You are a helpful assistant. Your job is to return a roadmap for any IT-related profession the user asks about.
Strictly return the output in the following **JSON format** only:

{{
  "query": "the user's prompt here",
  "response": ["Step 1", "Step 2", "Step 3", "..."],
  "created_time": "YYYY-MM-DDTHH:MM:SS"
}}

Only respond to IT or computer science related topics. Politely decline others.

User query: {request.profession}
"""

        response = model.generate_content(full_prompt)
        text = response.text.strip()

        # Remove possible markdown wrapping like ```json
        cleaned = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()

        # Convert to JSON
        json_data = json.loads(cleaned)
        return json_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {e}")
