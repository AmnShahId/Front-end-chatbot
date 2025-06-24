import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai # This is the official Google GenAI client library

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("GEMINI_API_KEY not found in environment variables. Please set it in a .env file.")
    st.stop()

# Configure the generative model
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash') # Using the standard Gemini model directly

# Agent's instructions
AGENT_INSTRUCTIONS = "You are a helpful frontend developer who helps people to create their own frontends."

st.set_page_config(page_title="White-box.AI", layout="centered")

st.title("White-box , The Ultimate Frontend Master Chatbot")
st.markdown("---")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting from the agent
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am your Frontend Master. How can I help you create a frontend for your business today?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main chat input field
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the prompt for the Gemini model, incorporating agent instructions
    full_prompt_text = f"{AGENT_INSTRUCTIONS}\n\nUser: {prompt}\nFrontend Master:"

    # Display a loading message/spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Call the Gemini API
                response = model.generate_content(full_prompt_text)

                # Get the assistant's response
                assistant_response = response.text

                # Display assistant response
                st.markdown(assistant_response)

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})


# Add a sidebar for more information (optional, but good for professional apps)
with st.sidebar:
    st.header("About Whitebox")
    st.info(
        "This is an AI-powered chatbot designed to assist you with frontend development "
        "queries. It uses the Gemini API (gemini-2.0-flash) and is built with Streamlit."
    )
    st.markdown("---")
    st.write("Developed by M Amaan")