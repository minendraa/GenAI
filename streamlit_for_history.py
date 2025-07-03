import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize model and chat once per session
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-2.5-flash")
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# Streamlit page config
st.set_page_config(page_title="Gemini Chat", page_icon="💬", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>💬 Chat with Gemini</h1>", unsafe_allow_html=True)

# Container for chat history
chat_container = st.container()

# Display chat history
if st.session_state.messages:
    with chat_container:
        st.markdown("---")
        for role, message in st.session_state.messages:
            if role == "user":
                st.markdown(
                    f"""
                    <div style='background-color:#dcf8c6; padding:10px; border-radius:10px; margin-bottom:10px; text-align:right; color:#000;'>
                        <strong>You:</strong><br>{message}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""
                    <div style='background-color:#e6f2ff; padding:10px; border-radius:10px; margin-bottom:10px; text-align:left; color:#000;'>
                        <strong>Gemini:</strong><br>{message}
                    </div>
                    """, unsafe_allow_html=True)

# Container for input at the bottom
input_container = st.container()
with input_container:
    st.markdown("---")
    # Chat input and buttons in columns
    col1, col2 = st.columns([4, 1])
    with col1:
        user_query = st.text_input("Type your question:", 
                                  placeholder="e.g. What is the height of Mount Everest?", 
                                  key="input",
                                  label_visibility="collapsed")
    with col2:
        ask_btn = st.button("Ask", use_container_width=True)
        reset_btn = st.button("🔄 Reset", use_container_width=True)

    # Handle button actions
    if ask_btn:
        if user_query:
            # Append user message
            st.session_state.messages.append(("user", user_query))

            # Get Gemini response
            with st.spinner("Gemini is thinking..."):
                response = st.session_state.chat.send_message(user_query)
                st.session_state.messages.append(("gemini", response.text))
            # Rerun to update the display
            st.rerun()
        else:
            st.warning("Please enter a message before submitting.")

    if reset_btn:
        model = genai.GenerativeModel("gemini-2.5-flash")
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.messages = []
        st.success("Conversation reset.")
        st.rerun()