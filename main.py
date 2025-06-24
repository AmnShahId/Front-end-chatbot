import streamlit as st
import os
from dotenv import load_dotenv # Used to load environment variables from .env file
import google.generativeai as genai # The official Google GenAI client library

# --- Configuration and Initialization ---

# Load environment variables from .env file.
# This must be done at the very beginning of your script.
load_dotenv()

# Retrieve the Gemini API key from environment variables.
# For Streamlit Cloud, it's highly recommended to use st.secrets for production,
# but for local development, .env is convenient.
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is available. If not, stop the app and show an error.
if not gemini_api_key:
    st.error(
        "GEMINI_API_KEY not found in environment variables. "
        "Please set it in a `.env` file (for local development) "
        "or as a secret in Streamlit Cloud (for deployment)."
    )
    st.stop() # Halts the execution of the app

# Configure the generative model with your API key.
genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model. Using 'gemini-2.0-flash' as specified.
model = genai.GenerativeModel('gemini-2.0-flash')

# Define the agent's persona and instructions.
AGENT_INSTRUCTIONS = (
    "You are a helpful frontend developer who assists people in creating their own frontends. "
    "Also, provide guidance for different situations and challenges in frontend development."
)

# --- Streamlit UI Setup ---

# Set basic page configuration for the Streamlit app.
st.set_page_config(page_title="White-box.AI", layout="centered")

# Display the main title and a separator.
st.title("White-box, The Ultimate Frontend Master Chatbot")
st.markdown("---")

# Initialize chat history in Streamlit's session state if it doesn't already exist.
# Session state ensures that the chat history persists across reruns of the app.
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add an initial greeting from the assistant to start the conversation.
    st.session_state.messages.append(
        {"role": "assistant", "content": "Hello! I am your Frontend Master. How can I help you create a frontend for your business today?"}
    )

# Display all chat messages from history on each app rerun.
# This loop iterates through the `st.session_state.messages` list.
for message in st.session_state.messages:
    with st.chat_message(message["role"]): # Uses Streamlit's built-in chat message styling
        st.markdown(message["content"])

# --- Chat Input and Response Generation ---

# Create the main chat input field at the bottom of the app.
# `st.chat_input` returns the user's message when they press Enter or click send.
if prompt := st.chat_input("Type your message..."):
    # Add the user's message to the chat history.
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user's message immediately in the chat interface.
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the full prompt for the Gemini model by combining agent instructions and user's query.
    # This helps guide the model's response according to the persona.
    full_prompt_text = f"{AGENT_INSTRUCTIONS}\n\nUser: {prompt}\nFrontend Master:"

    # Display a loading message while waiting for the Gemini API response.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."): # Shows a spinner to indicate activity
            try:
                # Call the Gemini API to generate content based on the full prompt.
                response = model.generate_content(full_prompt_text)

                # Extract the text response from the Gemini model.
                assistant_response = response.text

                # Display the assistant's response in the chat interface.
                st.markdown(assistant_response)

                # Add the assistant's response to the chat history.
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                # Catch any errors during API call or response processing.
                error_message = f"An error occurred while fetching a response: {e}"
                st.error(error_message) # Display a Streamlit error message
                # Add a generic error message to the chat history for the user.
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})

# --- Sidebar for Additional Information ---

# Adds a sidebar to the Streamlit application for "About" information.
with st.sidebar:
    st.header("About Whitebox.AI")
    st.info(
        "This is an AI-powered chatbot designed to assist you with frontend development "
        "queries. It uses the Google Gemini API (specifically 'gemini-2.0-flash') "
        "and is built using the Streamlit framework."
    )
    st.markdown("---")
    st.write("Developed by M Amaan")
