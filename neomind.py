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
    page_title="NeoMind AI Chat",  # Shows in browser tab
    page_icon="🤖",               # Robot emoji favicon
    layout="centered"             # Centers the content on page
)

# ========== CUSTOM STYLING ==========
# Inject custom CSS to style the application
st.markdown("""
    <style>
    /* Set overall page background */
    body {
        background-color: #f4f6f9;
    }
    /* Style the main content container */
    .main {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    /* Style input fields and buttons */
    input, button {
        border-radius: 8px !important;
    }
    /* Style user message bubbles */
    .user-msg {
        background-color: #daf5dc;  /* Light green background */
        padding: 12px;
        border-radius: 12px;
        text-align: right;        /* Right-align user messages */
        margin-bottom: 10px;
        color: #000;              /* Black text */
    }
    /* Style AI message bubbles */
    .ai-msg {
        background-color: #e8f0fe;  /* Light blue background */
        padding: 12px;
        border-radius: 12px;
        text-align: left;         /* Left-align AI messages */
        margin-bottom: 10px;
        color: #000;              /* Black text */
    }
    </style>
""", unsafe_allow_html=True)  # Allow raw HTML for styling

# ========== APPLICATION HEADER ==========
# Main title with centered styling
st.markdown(
    "<h1 style='text-align: center; color: #2c3e50;'>🤖 Welcome to NeoMind AI</h1>",
    unsafe_allow_html=True
)
# Subtitle with centered styling
st.markdown(
    "<p style='text-align: center; color: #7f8c8d;'>Ask anything. NeoMind will respond intelligently.</p>",
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
        # Loop through all stored messages in chronological order
        for role, message in st.session_state.messages:
            if role == "user":
                # Display user messages with special styling
                st.markdown(
                    f"<div class='user-msg'><strong>You:</strong><br>{message}</div>",
                    unsafe_allow_html=True
                )
            else:
                # Display AI messages with different styling
                st.markdown(
                    f"<div class='ai-msg'><strong>NeoMind:</strong><br>{message}</div>",
                    unsafe_allow_html=True
                )

# ========== USER INPUT SECTION ==========
# Add horizontal divider before input area
st.markdown("---")
# Create columns for input field and send button (5:1 width ratio)
col1, col2 = st.columns([5, 1])

with col1:
    # Text input field for user queries
    user_query = st.text_input(
        "Ask something...",  # Placeholder text
        placeholder="e.g., Explain quantum computing",  # Example prompt
        key="input",        # Unique identifier
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
        
        # Show loading spinner while generating response
        with st.spinner("NeoMind is generating a response..."):
            # Send query to Gemini AI
            response = st.session_state.chat.send_message(user_query)
            # Store AI response in history
            st.session_state.messages.append(("ai", response.text))
        
        # Rerun the app to update the display
        st.rerun()
    else:
        # Show warning if user tries to send empty message
        st.warning("Please enter a message to send.")

# ========== RESET LOGIC ==========
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