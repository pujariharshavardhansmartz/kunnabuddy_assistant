# --- UPDATED FILE: tasks/google_search.py ---

import os
import requests
import json
from dotenv import load_dotenv
from .gemini_helper import ask_gemini

# Make this module self-sufficient
load_dotenv()

try:
    API_KEY = os.getenv("SERPER_API_KEY") 
    if not API_KEY:
        print("🔴 WARNING: SERPER_API_KEY not set in .env file. Google Search will not work.")
except Exception as e:
    API_KEY = None
    print(f"🔴 ERROR loading SERPER_API_KEY: {e}")

# ... (the rest of the file is the same)
def google_search(query, num_results=3):
    if not API_KEY: 
        return "Google Search is not configured because the SERPER_API_KEY is missing from the .env file."
    # ... (rest of the function)
    print(f"INFO: Performing Google search for: '{query}' using Serper.dev.")
    
    url = "https://google.serper.dev/search"
    payload = json.dumps({ "q": query })
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()

        results = response.json()
        
        organic_results = results.get("organic", [])
        
        if not organic_results:
            return f"I searched online but couldn't find any direct text results for '{query}'."

        snippets = [
            r.get("snippet", "") for r in organic_results[:num_results] 
            if r.get("snippet")
        ]

        if not snippets:
            return f"I found pages for '{query}', but they did not have summary snippets."

        context = "\n---\n".join(snippets)
        
        synthesis_prompt = f"""
        Based *only* on the following search result snippets, provide a direct and concise answer to the user's query.
        User's Query: "{query}"
        Search Results:
        ---
        {context}
        ---
        Answer:
        """
        
        print("INFO: Synthesizing answer from search results...")
        return ask_gemini(synthesis_prompt)
        
    except requests.exceptions.HTTPError as http_err:
        error_message = f"An HTTP error occurred during the Google search: {http_err}"
        if response.status_code == 401:
            error_message += "\nThis is an 'Unauthorized' error. Please double-check your SERPER_API_KEY in the .env file."
        print(f"❌ {error_message}")
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred during the Google search: {e}"
        print(f"❌ {error_message}")
        return error_message