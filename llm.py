# Import the openai library to interact with OpenAI's API
import openai
# Import the os library to access environment variables
import os
# Import the load_dotenv function to load environment variables from a .env file
from dotenv import load_dotenv

# Load environment variables from the .env file (e.g., OPENAI_API_KEY)
load_dotenv()

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a function to send a prompt to the GPT model and return the response
def ask_gpt(prompt_text):
    try:
        # Create an OpenAI client instance
        client = openai.OpenAI()

        # Send a chat-based prompt to the GPT-3.5-turbo model
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',  
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},  # System message to guide the assistant's behavior
                {'role': 'user', 'content': prompt_text}  # User prompt
            ]
        )

        # Extract and return the assistant's reply (cleaned with .strip())
        return response.choices[0].message.content.strip()
    
    # If any error occurs (like network or API error), return the error message
    except Exception as e:
        return f"An Error Occurred: {e}"

# Define the input prompt to send to the assistant
prompt = "Explain what large language model is in three simple sentences."

# Call the function with the prompt and store the response
response_text = ask_gpt(prompt)

# Print the original prompt
print("---My Prompt---")
print(prompt)

# Print the response generated by GPT
print("---GPT's Response---")
print(response_text)
