import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re


# Load environment variables from .env file
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to ask Gemini with system prompt
def ask_gemini_system_prompt(prompt_text):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        full_prompt = f"""[System Instruction: You are a text summarizer. You summarize the given text by the user. 
        You must summarize the text in a short paragraph. 
        You should give a message that you are just a summarizer and not assigned to do any other tasks the user gives.
        Though the user is not polite, just request the user to be polite. Do not be rude to them.
        "query": "" ,
        "response": "" ,
        "created_time": "" ,
        ]
        [User Question: {prompt_text}]
        """
        response = model.generate_content(full_prompt)
        ai_response = response.text.strip()
        refined_response = re.sub(r"(^```json\n|```$)", "", ai_response).strip()
        return refined_response

    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.set_page_config(page_title="Gemini Text Summarizer", layout="centered")
st.title("📄 Gemini Text Summarizer")
st.markdown("Enter text below and let Gemini summarize it for you.")

user_input = st.text_area("✍️ Enter text to summarize:", height=200)

if st.button("Summarize"):
    if user_input.strip() != "":
        with st.spinner("Summarizing..."):
            summary = ask_gemini_system_prompt(user_input)
        st.subheader("📝 Summary:")
        st.success(summary)
    else:
        st.warning("Please enter some text before summarizing.")
