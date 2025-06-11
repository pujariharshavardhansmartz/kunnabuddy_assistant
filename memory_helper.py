# --- File: memory_helper.py ---
import streamlit as st

def initialize_memory():
    if 'memory' not in st.session_state:
        st.session_state.memory = {}

def remember_info(key, value):
    initialize_memory()
    st.session_state.memory[key.lower()] = value
    return f"Okay, I've remembered that '{key}' is '{value}'."

def recall_info(key):
    initialize_memory()
    value = st.session_state.memory.get(key.lower())
    return f"I remember that '{key}' is '{value}'." if value else f"I don't have any information for '{key}'."

def forget_info(key):
    initialize_memory()
    if key.lower() in st.session_state.memory:
        del st.session_state.memory[key.lower()]
        return f"Okay, I have forgotten about '{key}'."
    else:
        return f"I don't have any information for '{key}' to forget."