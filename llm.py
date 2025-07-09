import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt_text):
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role':'system','content':'You are a helpful assistant.'},
                {'role':'user','content':prompt_text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An Error Occurred: {e}"

prompt = "Explain what large language model is in three simple sentences."
response_text = ask_gpt(prompt)

print("---My Prompt---")
print(prompt)
print("---GPT's Response---")
print(response_text)