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

# FastAPI app
app = FastAPI(title="IT Roadmap Generator")

# In-memory storage
answers = []

# Request schema
class PromptRequest(BaseModel):
    profession: str


import json
# Save to file
def save_to_file(data: dict):
    with open("roadmaps.json", "a", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



# POST endpoint
@app.post("/roadmap")
def generate_roadmap(request: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        current_time = datetime.now().isoformat()

        full_prompt = f"""
You are a helpful assistant. Your job is to return a roadmap for any IT-related profession the user asks about.
Strictly return the output in the following **JSON format** only.
Important: response must be a list, and each step must be inside a dictionary like this:

{{
  "query": "the user's prompt here",
  "response": [
    {{ "step": "Learn basics of HTML, CSS, JavaScript" }},
    {{ "step": "Understand Git and GitHub" }},
    ...
  ],
  "created_time": "YYYY-MM-DDTHH:MM:SS"
}}

Only respond to IT or computer science related topics. Politely decline others.

User query: {request.profession}
"""
        response = model.generate_content(full_prompt)
        text = response.text.strip()

        # Clean up markdown-style code block
        cleaned = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()

        # Parse JSON
        json_data = json.loads(cleaned)

        # Add timestamp (if missing)
        json_data["created_time"] = json_data.get("created_time", current_time)

        # Store and save to file
        answers.append(json_data)
        save_to_file(json_data)

        return json_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {e}")

# GET endpoint
import json
@app.get("/roadmap/history")
def get_saved_roadmaps():
    with open("roadmaps.json", "r", encoding="utf-8") as f:
        json_data1 = json.load(f)
    return json_data1



import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/roadmap/answer", response_class=HTMLResponse)
async def get_data(request: Request):
    url = "http://localhost:8000/roadmap/history"

    response = requests.get(url)
    data = response.json()
    question = data["query"]
    answer = data["response"]

    context = {"request": request, "question": question, "answer": answer}
    return templates.TemplateResponse("answer.html", context)
