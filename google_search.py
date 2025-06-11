# --- File: google_search.py (COMPLETE AND FINAL) ---

import os
import requests
import json
# This import is now CORRECTED (no leading dot)
from gemini_helper import ask_gemini

def google_search(query: str):
    """
    Performs a Google search using the Serper API and returns a summarized answer.
    """
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        search_results = response.json()
        
        # Check if there are any results
        if not search_results.get("organic"):
            return "I couldn't find any relevant results for that search."
            
        # Prepare the context for Gemini
        context = f"Based on these search results, answer the user's query: '{query}'\n\n"
        for result in search_results["organic"][:5]: # Use top 5 results
            context += f"Title: {result.get('title')}\n"
            context += f"Snippet: {result.get('snippet')}\n"
            context += "---\n"
            
        # Get a summarized answer from Gemini
        return ask_gemini(context)

    except requests.exceptions.HTTPError as http_err:
        return f"A search API error occurred: {http_err}. Please check your SERPER_API_KEY."
    except Exception as e:
        return f"An unexpected error occurred during the search: {e}"