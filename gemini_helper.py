# --- File: gemini_helper.py ---
import streamlit as st
import google.generativeai as genai

@st.cache_resource
def get_gemini_model():
    """Initializes and returns the Gemini model, cached for efficiency."""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Fatal Error: Could not configure Gemini model. Please check GOOGLE_API_KEY in secrets. Error: {e}")
        return None

def ask_gemini(prompt_text):
    """Sends a prompt to the Gemini model and returns the response text."""
    model = get_gemini_model()
    if model is None:
        return "The AI model is not available due to a configuration error."
    
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the AI model: {e}"