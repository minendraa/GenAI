import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model
model = genai.GenerativeModel('gemini-2.5-flash')

# Streamlit setup
st.set_page_config(page_title="Gemini AI Q&A", page_icon="✨", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>💡Ask Gemini</h1>", unsafe_allow_html=True)
st.markdown("Enter your question below and let Gemini give you a smart answer!")

# User input
user_input = st.text_input("💬 Your Question", placeholder="e.g., What is the capital of Nepal?")

# Keep chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Handle submission
if st.button("🚀 Get Answer") and user_input:
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_input)
            answer = response.text
            st.session_state.history.append((user_input, answer, "success"))
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.session_state.history.append((user_input, error_msg, "error"))

# Show history
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Conversation History")

    for question, reply, status in reversed(st.session_state.history):
        st.markdown(f"**You:** {question}")
        if status == "success":
            st.markdown(
                f"""
                <div style="
                    background-color: #e6f2ff;
                    padding: 15px;
                    border-left: 5px solid #3399ff;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
                    margin-bottom: 20px;
                    color: black;
                    font-size: 16px;
                    line-height: 1.6;
                ">
                    <b>Gemini:</b><br>{reply}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div style="
                    background-color: #ffcccc;
                    color: #800000;
                    padding: 15px;
                    border-left: 5px solid #ff0000;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    font-size: 16px;
                    line-height: 1.6;
                ">
                    <b>Error:</b><br>{reply}
                </div>
                """,
                unsafe_allow_html=True
            )

