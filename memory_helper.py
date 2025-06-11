# --- File: memory_helper.py (COMPLETE AND CLOUD-READY) ---

import streamlit as st

def initialize_memory():
    """Ensures that the memory dictionary exists in the session state."""
    if 'memory' not in st.session_state:
        st.session_state.memory = {}

def remember_info(key, value):
    """Saves a key-value pair to the session state memory."""
    initialize_memory()
    if not key or not value:
        return "I need both a topic (key) and the information (value) to remember."
        
    st.session_state.memory[key.lower()] = value
    return f"Okay, I've remembered that '{key}' is '{value}'. You can ask me to recall it later."

def recall_info(key):
    """Recalls a value from the session state memory based on a key."""
    initialize_memory()
    if not key:
        return "What topic do you want me to recall?"
        
    value = st.session_state.memory.get(key.lower())
    
    if value:
        return f"I remember that '{key}' is '{value}'."
    else:
        return f"I'm sorry, I don't have any information stored for '{key}'."

def forget_info(key):
    """Forgets (deletes) a key-value pair from the session state memory."""
    initialize_memory()
    if not key:
        return "What topic do you want me to forget?"
        
    if key.lower() in st.session_state.memory:
        del st.session_state.memory[key.lower()]
        return f"Okay, I have forgotten the information about '{key}'."
    else:
        return f"I don't have any information stored for '{key}', so there is nothing to forget."