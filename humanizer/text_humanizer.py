from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from typing import List

app = FastAPI()

# Load model and tokenizer
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")

class HumanizeRequest(BaseModel):
    text: str
    creativity: float = 0.8
    num_return_sequences: int = 3

class HumanizeResponse(BaseModel):
    original: str
    humanized: str
    all_versions: List[str]

@app.post("/humanize", response_model=HumanizeResponse)
async def humanize_text(request: HumanizeRequest):
    prompt = f"Paraphrase this in a more natural, human way: {request.text}"
    input_ids = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True).to(model.device)

    outputs = model.generate(
        input_ids,
        max_length=512,
        num_beams=5,
        num_return_sequences=request.num_return_sequences,
        temperature=0.7 + request.creativity,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        early_stopping=True,
        repetition_penalty=2.0,
    )

    paraphrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    best_paraphrase = max(paraphrases, key=lambda x: len(set(x.split()) - set(request.text.split())))
    
    return HumanizeResponse(
        original=request.text,
        humanized=best_paraphrase,
        all_versions=paraphrases
    )

@app.get("/")
async def health_check():
    return {"status": "healthy", "model": model_name}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)