# Import necessary libraries
import streamlit as st  # For building the web interface
import google.generativeai as genai  # For accessing Google's Gemini AI
from dotenv import load_dotenv  # For loading environment variables
import os  # For accessing system environment variables

# Load environment variables from .env file
load_dotenv()  
# Configure Gemini AI with API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ========== SESSION STATE INITIALIZATION ==========
# Initialize model and chat history in session state to persist across reruns
if "chat" not in st.session_state:
    # Create a new Gemini model instance (using flash version for faster responses)
    model = genai.GenerativeModel("gemini-2.5-flash")
    # Start a new chat session with empty history
    st.session_state.chat = model.start_chat(history=[])
    # Initialize empty list to store message history for UI display
    st.session_state.messages = []

# ========== PAGE CONFIGURATION ==========
# Set up the page title, icon and layout
st.set_page_config(
    page_title="NeoMood AI",  # Shows in browser tab
    page_icon="🤖",          # Robot emoji favicon
    layout="centered"        # Centers the content on page
)

# ========== MOOD SELECTION SYSTEM ==========
# Create a dropdown for users to select their current mood
mood = st.selectbox(
    "🧠 Choose your mood:",  # Label with brain emoji
    ["Happy 😊", "Curious 🤔", "Professional 🧑‍💼", "Chill 😎"]  # Mood options
)

# ========== MOOD-BASED CONFIGURATIONS ==========
# Dictionary mapping moods to background colors for AI messages
mood_colors = {
    "Happy 😊": "#fff8dc",    # Light yellow - cheerful color
    "Curious 🤔": "#f0e6ff",  # Lavender - thoughtful color
    "Professional 🧑‍💼": "#e0f7fa",  # Light blue - business-like
    "Chill 😎": "#e8f5e9"     # Light green - relaxed vibe
}
# Get the background color for current mood
chat_bg = mood_colors[mood]

# Dictionary of welcome messages for each mood
welcome_messages = {
    "Happy 😊": "🌞 Let's brighten your day!",
    "Curious 🤔": "🔍 Ask me anything you're curious about.",
    "Professional 🧑‍💼": "📊 Ready for serious business questions.",
    "Chill 😎": "🍹 Let's keep it casual and fun."
}

# Dictionary of prompt prefixes to guide AI responses based on mood
prompt_prefix = {
    "Happy 😊": "Speak in a joyful tone: ",
    "Curious 🤔": "Explain with curiosity: ",
    "Professional 🧑‍💼": "Keep it professional: ",
    "Chill 😎": "Make it relaxed and easy-going: "
}

# ========== UI STYLING ==========
# Inject custom CSS to style the application
st.markdown(f"""
    <style>
    /* Set overall page background */
    body {{
        background-color: #f4f6f9;
    }}
    /* Style the main content container */
    .main {{
        background-color: #ffffff;  /* White background */
        border-radius: 12px;       /* Rounded corners */
        padding: 2rem;             /* Internal spacing */
        box-shadow: 0 0 20px rgba(0,0,0,0.1);  /* Subtle shadow */
    }}
    /* Style input fields and buttons */
    input, button {{
        border-radius: 8px !important;  /* Rounded edges */
    }}
    /* Style user message bubbles */
    .user-msg {{
        background-color: #daf5dc;  /* Light green background */
        padding: 12px;             /* Internal spacing */
        border-radius: 12px;       /* Rounded corners */
        text-align: right;         /* Right-align user messages */
        margin-bottom: 10px;      /* Space between messages */
        color: #000;              /* Black text */
    }}
    /* Style AI message bubbles with mood-based color */
    .ai-msg {{
        background-color: {chat_bg};  /* Dynamic color based on mood */
        padding: 12px;
        border-radius: 12px;
        text-align: left;          /* Left-align AI messages */
        margin-bottom: 10px;
        color: #000;
    }}
    </style>
""", unsafe_allow_html=True)  # Allow raw HTML for styling

# ========== APPLICATION HEADER ==========
# Main title with centered styling
st.markdown(
    "<h1 style='text-align: center; color: #2c3e50;'>🤖 Welcome to NeoMood AI</h1>", 
    unsafe_allow_html=True
)
# Mood-specific welcome message with centered styling
st.markdown(
    f"<p style='text-align: center; color: #7f8c8d;'>{welcome_messages[mood]}</p>",
    unsafe_allow_html=True
)

# ========== CHAT HISTORY DISPLAY ==========
# Create container to hold chat messages
chat_container = st.container()
with chat_container:
    # Only show if there are messages to display
    if st.session_state.messages:
        # Add horizontal divider
        st.markdown("---")
        # Loop through all stored messages
        for role, message in st.session_state.messages:
            if role == "user":
                # Display user messages with special styling
                st.markdown(
                    f"<div class='user-msg'><strong>You:</strong><br>{message}</div>",
                    unsafe_allow_html=True
                )
            else:
                # Display AI messages with mood-based styling
                st.markdown(
                    f"<div class='ai-msg'><strong>NeoMind:</strong><br>{message}</div>",
                    unsafe_allow_html=True
                )

# ========== USER INPUT SECTION ==========
# Add horizontal divider before input area
st.markdown("---")
# Create columns for input field and send button
col1, col2 = st.columns([5, 1])  # 5:1 width ratio

with col1:
    # Text input field for user queries
    user_query = st.text_input(
        "Ask something...",  # Placeholder text
        placeholder="e.g., Explain quantum computing",  # Example prompt
        key="input",  # Unique identifier
        label_visibility="collapsed"  # Hide the label
    )

with col2:
    # Send button with emoji
    ask_btn = st.button("💬 Send", use_container_width=True)

# Create reset button centered below input
col_reset = st.columns([1, 6, 1])[1]  # Middle column of 3
with col_reset:
    # Reset button with emoji
    reset_btn = st.button("🔁 Reset Chat", use_container_width=True)

# ========== CHAT LOGIC ==========
if ask_btn:  # When send button is clicked
    if user_query:  # Only proceed if there's input
        # Store user message in history (for display)
        st.session_state.messages.append(("user", user_query))
        # Add mood-specific prefix to guide AI response
        full_query = prompt_prefix[mood] + user_query

        # Show loading spinner while generating response
        with st.spinner("NeoMind is generating a response..."):
            # Send query to Gemini AI
            response = st.session_state.chat.send_message(full_query)
            # Store AI response in history
            st.session_state.messages.append(("ai", response.text))

        # Rerun the app to update the display
        st.rerun()
    else:
        # Show warning if user tries to send empty message
        st.warning("Please enter a message to send.")

# Reset functionality
if reset_btn:  # When reset button is clicked
    # Reinitialize the model
    model = genai.GenerativeModel("gemini-2.5-flash")
    # Clear chat history
    st.session_state.chat = model.start_chat(history=[])
    # Clear message display history
    st.session_state.messages = []
    # Show success message
    st.success("Conversation has been reset.")
    # Rerun to refresh UI
    st.rerun()