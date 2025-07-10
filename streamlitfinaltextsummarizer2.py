import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure Gemini AI with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to ask Gemini with system prompt to summarize text
def ask_gemini_system_prompt(query_text):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="You are a helpful assistant. Summarize the provided text."
        )
        response = model.generate_content(query_text)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI setup
st.set_page_config(page_title="Gemini Text Summarizer", layout="centered")
st.title("📄 Gemini Text Summarizer")
st.markdown("Enter text below and let Gemini summarize it for you.")

user_input = st.text_area("✍️ Enter text to summarize:", height=200)

if st.button("Summarize"):
    if user_input.strip():
        with st.spinner("Summarizing..."):
            summary = ask_gemini_system_prompt(user_input)
        st.subheader("📝 Summary:")
        st.success(summary)
    else:
        st.warning("Please enter some text before summarizing.")
