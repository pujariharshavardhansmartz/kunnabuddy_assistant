# --- UPDATED FILE: web_app.py ---

import streamlit as st
from dotenv import load_dotenv # <-- NEW IMPORT

# --- THIS IS THE CRITICAL FIX ---
# Load all the secrets from the .env file into the environment
load_dotenv()
# --- END OF FIX ---

# Import the brain of your existing agent
from tasks.agent_router import determine_command
from tasks.dispatcher import dispatch_command

# --- Page Configuration ---
st.set_page_config(
    page_title="KunnaBuddy Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 KunnaBuddy AI Assistant")
st.caption("Your personal and family assistant, ready to help.")

# --- Session State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# --- Chat History Display ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input Handling ---
if prompt := st.chat_input("What can I do for you?"):
    # 1. Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Process the command and get the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # --- REUSE YOUR EXISTING AGENT LOGIC ---
                command_data = determine_command(prompt)
                result = dispatch_command(command_data, prompt)
                
                # Display the result
                st.markdown(result)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": result})

            except Exception as e:
                error_message = f"I'm sorry, I ran into an error: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})