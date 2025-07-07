import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize model and chat once per session
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-2.5-flash")
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# Set page configuration
st.set_page_config(page_title="NeoMood AI", page_icon="🤖", layout="centered")

# Mood selector
mood = st.selectbox("🧠 Choose your mood:", ["Happy 😊", "Curious 🤔", "Professional 🧑‍💼", "Chill 😎"])

# Mood-based settings
mood_colors = {
    "Happy 😊": "#fff8dc",
    "Curious 🤔": "#f0e6ff",
    "Professional 🧑‍💼": "#e0f7fa",
    "Chill 😎": "#e8f5e9"
}
chat_bg = mood_colors[mood]

welcome_messages = {
    "Happy 😊": "🌞 Let's brighten your day!",
    "Curious 🤔": "🔍 Ask me anything you're curious about.",
    "Professional 🧑‍💼": "📊 Ready for serious business questions.",
    "Chill 😎": "🍹 Let's keep it casual and fun."
}

prompt_prefix = {
    "Happy 😊": "Speak in a joyful tone: ",
    "Curious 🤔": "Explain with curiosity: ",
    "Professional 🧑‍💼": "Keep it professional: ",
    "Chill 😎": "Make it relaxed and easy-going: "
}

# Inject custom CSS
st.markdown(f"""
    <style>
    body {{
        background-color: #f4f6f9;
    }}
    .main {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }}
    input, button {{
        border-radius: 8px !important;
    }}
    .user-msg {{
        background-color: #daf5dc;
        padding: 12px;
        border-radius: 12px;
        text-align: right;
        margin-bottom: 10px;
        color: #000;
    }}
    .ai-msg {{
        background-color: {chat_bg};
        padding: 12px;
        border-radius: 12px;
        text-align: left;
        margin-bottom: 10px;
        color: #000;
    }}
    </style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🤖 Welcome to NeoMood AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #7f8c8d;'>{welcome_messages[mood]}</p>", unsafe_allow_html=True)

# Chat history
chat_container = st.container()
with chat_container:
    if st.session_state.messages:
        st.markdown("---")
        for role, message in st.session_state.messages:
            if role == "user":
                st.markdown(f"<div class='user-msg'><strong>You:</strong><br>{message}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-msg'><strong>NeoMind:</strong><br>{message}</div>", unsafe_allow_html=True)

# Input area
st.markdown("---")
st.markdown("🎤 **Record your voice or type below:**")
audio_text = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop", just_once=True, use_container_width=True)
typed_text = st.text_input("Ask something...", placeholder="e.g., Explain quantum computing", key="input", label_visibility="collapsed")
user_query = audio_text if audio_text else typed_text

col1, col2 = st.columns([5, 1])
with col2:
    ask_btn = st.button("💬 Send", use_container_width=True)

col_reset = st.columns([1, 6, 1])[1]
with col_reset:
    reset_btn = st.button("🔁 Reset Chat", use_container_width=True)

# Chat logic
if ask_btn:
    if user_query:
        st.session_state.messages.append(("user", user_query))
        full_query = prompt_prefix[mood] + user_query

        with st.spinner("NeoMind is generating a response..."):
            response = st.session_state.chat.send_message(full_query)
            ai_text = response.text
            st.session_state.messages.append(("ai", ai_text))

            # Convert response to speech
            tts = gTTS(ai_text)
            tts.save("response.mp3")

            # Encode audio for web playback
            with open("response.mp3", "rb") as audio_file:
                audio_bytes = audio_file.read()
                b64_audio = base64.b64encode(audio_bytes).decode()

            # Stream audio player
            st.markdown(f"""
                <audio autoplay controls>
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)

        st.rerun()
    else:
        st.warning("Please say or type something.")

# Reset button
if reset_btn:
    model = genai.GenerativeModel("gemini-2.5-flash")
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    st.success("Conversation has been reset.")
    st.rerun()
