# Import necessary libraries
import google.generativeai as genai  # Google's Gemini AI library
from dotenv import load_dotenv       # For loading environment variables
import os                           # For accessing system environment variables

# Load API key from .env file
load_dotenv()  # Load environment variables from a .env file
# Configure Gemini AI with the API key stored in environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the generative model instance
# Using 'gemini-2.5-flash' model which is optimized for fast responses
model = genai.GenerativeModel('gemini-2.5-flash')

# Start a new chat session with empty history
# This chat object will maintain conversation context
chat = model.start_chat(history=[])

# Start interactive conversation loop
while True:
    # Prompt user for input
    query = input("Enter your query: ")

    # Send the user's message to the model along with full chat history
    # This maintains context for multi-turn conversations
    response = chat.send_message(query)

    # Print the model's response with some formatting
    print("\n" + response.text)  # Add newline before response for readability

    # Ask user if they want to continue
    next_step = input("\nDo you want to ask another question? (y/n): ").lower()
    
    # Exit loop if user doesn't want to continue
    if next_step != 'y':
        break  # Exit the while loop