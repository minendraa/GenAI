import google.generativeai as genai
import os 
from dotenv import load_dotenv
import re
#set your api key

# Load environment variables from .env file
load_dotenv()
# Configure Gemini AI with API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini_system_prompt(prompt_text):
    try:
        model=genai.GenerativeModel("gemini-2.5-pro")
        full_prompt=f"""[System Instruction: You are helpful assistant of Canada Project, Use only polite words in a formal way, don't be rude. Your response must be in json format with 
        "query":   "" ,
        "response":  ""   ,
        "created_time":   ""  ,
        ]
        [User Question: {prompt_text}]"""

        response=model.generate_content(full_prompt)
        ai_response=response.text.strip()
        refined_response=re.sub(r"(^```json\n|```$)","",ai_response).strip()
        return refined_response
    
    except Exception as e:
        return f"An error occured: {e}"
    

prompt = input("Enter the Query: ")
response_text = ask_gemini_system_prompt(prompt)

print("---My Prompt---")
print(prompt)
print("---GPT's Response---")
print(response_text)
