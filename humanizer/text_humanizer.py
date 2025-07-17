from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Use a reliable T5 model
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")

def humanize(text, creativity=0.8):
    prompt = f"Paraphrase this in a more natural, human way: {text}"
    input_ids = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True).to(model.device)

    outputs = model.generate(
        input_ids,
        max_length=512,
        num_beams=5,
        num_return_sequences=3,
        temperature=0.7 + creativity,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        early_stopping=True,
        repetition_penalty=2.0,
    )

    paraphrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    # Return the most different version
    return max(paraphrases, key=lambda x: len(set(x.split()) - set(text.split())))

# Test
robotic_text = "The sun dipped below the horizon, casting a golden hue over the futuristic skyline. As synthetic drones buzzed softly above, a lone figure stood on the rooftop, contemplating the meaning of progress."
print("Original:")
print(robotic_text)
print("\nHumanized:")
print(humanize(robotic_text)) 