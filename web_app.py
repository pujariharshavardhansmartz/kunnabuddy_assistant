# --- File: web_app.py (COMPLETE AND UPDATED) ---

import streamlit as st

# Assuming your helper files are now in the same root directory
# If you kept them in the 'tasks' folder, change these back to 'from tasks...'
from agent_router import determine_command
from dispatcher_cloud import dispatch_command_cloud

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
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process the prompt with the agent
    with st.chat_message("assistant"):
        with st.spinner("KunnaBuddy is thinking..."):
            # 1. Get the structured command from the router
            command_data = determine_command(prompt)

            # --- THIS IS OUR NEW DEBUG VIEW ---
            # It will show us the command the agent decided on, so we can see if it's working.
            st.info(f"**DEBUG:** Router decided on command: `{command_data}`")
            # ------------------------------------

            # 2. Execute the command using the dispatcher
            response = dispatch_command_cloud(command_data, prompt)
            
            # 3. Display the final response
            st.markdown(response)
            
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})