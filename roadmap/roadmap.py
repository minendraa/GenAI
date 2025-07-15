import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure Gemini AI with API key
genai.configure(api_key=os.getenv("Rakesh_GOOGLE_API_KEY"))

def ask_gemini_for_it_roadmap(prompt_text):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        current_time = datetime.now().isoformat()

        full_prompt = f"""
You are a helpful assistant. Your job is to return a roadmap for any IT-related profession the user asks about.
Strictly return the output in the following **JSON format** only:

{{
  "query": "the user's prompt here",
  "response": [{"Step 1"}, {"Step 2"}, {"Step 3"}, "..."],
  "created_time": "YYYY-MM-DDTHH:MM:SS"
}}

Only respond to IT or computer science related topics. Politely decline others.

User query: {prompt_text}
"""

        response = model.generate_content(full_prompt)
        text = response.text.strip()

        # Optional: Remove Markdown-style ```json ``` wrapping
        cleaned = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()

        # Try to parse as JSON to ensure validity
        json_data = json.loads(cleaned)
        return json.dumps(json_data, indent=2)

    except Exception as e:
        return f"An error occurred: {e}"

# Main program
print("Welcome to the IT Roadmap Generator.")
prompt = input("Enter an IT profession (e.g., 'Data Scientist', 'Web Developer'): ")
response_json = ask_gemini_for_it_roadmap(prompt)

print("\n--- My Prompt ---")
print(prompt)
print("\n--- GPT's JSON Response ---")
print(response_json)
