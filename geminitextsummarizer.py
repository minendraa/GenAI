# Import necessary libraries
import google.generativeai as genai  # Google Generative AI (Gemini) SDK
import os  # For interacting with environment variables
from dotenv import load_dotenv  # To load environment variables from a .env file
import re  # For regular expressions, used to clean AI response

# Load environment variables from .env file (e.g., GOOGLE_API_KEY)
load_dotenv()

# Configure Gemini AI with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a function to interact with Gemini AI and get a summarized response
def ask_gemini_system_prompt(prompt_text):
    try:
        # Load the Gemini 2.5 Pro model
        model = genai.GenerativeModel("gemini-2.5-pro")

        # Create a system-guided prompt for the AI to behave as a summarizer
        full_prompt = f"""[System Instruction: You are a text summarizer. You summarize the given text by the user. 
        You must summarize the text in a short paragraph. 
        You should give a message that you are just a summarizer and not assigned to do any other tasks the user gives.
        Though the user is not polite, just request the user to be polite. Do not be rude to them.
        "query":   "" ,
        "response":  ""   ,
        "created_time":   ""  , 
        ]
        [User Question: {prompt_text}]"""

        # Generate content using the model and prompt
        response = model.generate_content(full_prompt)

        # Get the plain text from the AI response
        ai_response = response.text.strip()

        # Remove markdown code formatting if present (like ```json or ``` markers)
        refined_response = re.sub(r"(^```json\n|```$)", "", ai_response).strip()

        # Return cleaned and final response
        return refined_response

    except Exception as e:
        # Return an error message if any exception occurs
        return f"An error occurred: {e}"

# Main program starts here
print("Welcome to the text summarizer.")  # Greeting message to user

# Prompt user to enter text to summarize
prompt = input("Enter the text to summarize: ")

# Call the Gemini function with the user's text
response_text = ask_gemini_system_prompt(prompt)

# Display the original input and the AI's summarized response
print("---My Prompt---")
print(prompt)
print("---GPT's Response---")
print(response_text)
