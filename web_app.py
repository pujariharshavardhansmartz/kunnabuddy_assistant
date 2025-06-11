# --- File: web_app.py (COMPLETE AND FINAL) ---

import streamlit as st
# This now correctly imports from 'dispatcher.py' to match your file.
from agent_router import determine_command
from dispatcher import dispatch_command 

# --- Page Configuration ---
st.set_page_config(
    page_title="KunnaBuddy Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 KunnaBuddy AI Assistant")
st.caption("Your personal AI-powered assistant. I can search the web, manage your calendar, and more!")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input ---
if prompt := st.chat_input("What can I do for you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KunnaBuddy is thinking..."):
            command_data = determine_command(prompt)
            st.info(f"**DEBUG:** Router decided on command: `{command_data}`")
            # This now calls your 'dispatcher.py' file.
            response = dispatch_command(command_data, prompt)
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})