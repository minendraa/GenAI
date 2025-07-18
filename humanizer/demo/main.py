# main.py
from fastapi import FastAPI
from pydantic import BaseModel

# Import our custom logic
from humanize import humanize_text

import nltk
nltk.download('punkt')

# --- Pydantic Models for API data validation ---

class InputText(BaseModel):
    ai_text: str

class HumanizedText(BaseModel):
    original_text: str
    humanized_text: str
    message: str


# --- FastAPI Application ---

app = FastAPI(
    title="Text Humanizer API",
    description="An API to transform AI-like text into a more natural, human-sounding format.",
    version="1.0.0"
)

@app.post("/humanize/", response_model=HumanizedText)
async def create_humanized_text(data: InputText):
    """
    Accepts AI-generated text and applies transformations to make it
    sound more human by varying sentence structure, simplifying vocabulary,
    and adding contractions.
    """
    transformed_text = humanize_text(data.ai_text)
    
    return HumanizedText(
        original_text=data.ai_text,
        humanized_text=transformed_text,
        message="Text has been processed to sound more human."
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Text Humanizer API. Please send a POST request to /humanize/."}