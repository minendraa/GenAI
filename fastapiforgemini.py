from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define FastAPI app
app = FastAPI()

# Pydantic model for request body
class PromptRequest(BaseModel):
    prompt: str

# Gemini interaction function
def ask_gemini(prompt_text):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt_text)
        return response.text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error from Gemini: {str(e)}")

# POST endpoint
@app.post("/ask")
def ask_gemini_api(req: PromptRequest):
    response = ask_gemini(req.prompt)
    return {"prompt": req.prompt, "response": response}
