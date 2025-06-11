# --- UPDATED FILE: tasks/gemini_helper.py ---

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Make this module self-sufficient by loading the .env file
load_dotenv()

try:
    # Use os.getenv() which is safer as it returns None if the key is not found
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("🔴 ERROR: GOOGLE_API_KEY environment variable not set.")
    else:
        genai.configure(api_key=api_key)
        
except Exception as e:
    print(f"🔴 ERROR during Gemini configuration: {e}")


# It's better to create the model instance inside the function
# to ensure configuration has run first.
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini:\n\n{e}"