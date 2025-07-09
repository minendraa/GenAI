import google.generativeai as genai
import os 
from dotenv import load_dotenv

#set your api key

# Load environment variables from .env file
load_dotenv()
# Configure Gemini AI with API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini(prompt_text):
    try:
        model=genai.GenerativeModel("gemini-2.5-flash")

        response=model.generate_content(prompt_text)

        return response.text.strip()
    
    except Exception as e:
        return f"An error occured: {e}"
    

prompt = "Guess a random number between 1 and 50."
response_text = ask_gemini(prompt)

print("---My Prompt---")
print(prompt)
print("---GPT's Response---")
print(response_text)
