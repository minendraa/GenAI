import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model
model = genai.GenerativeModel('gemini-2.5-flash')
chat = model.start_chat(history=[])

# Start interactive loop
while True:
    query = input("Enter your query: ")

    # Send message with full history for context
    response = chat.send_message(query)

    # Print the model's contextual response
    print("\n" + response.text)

    next_step = input("\nDo you want to ask another question? (y/n): ").lower()
    if next_step != 'y':
        break

                        