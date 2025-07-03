import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the model
model = genai.GenerativeModel('gemini-2.5-flash')

# Generate a response
response = model.generate_content("Capital of Nepal?")

# Print the result
print(response.text)
