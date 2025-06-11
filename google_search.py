# --- File: google_search.py (COMPLETE AND ROBUST) ---

import os
import requests
import json
import streamlit as st # Import streamlit to access secrets
from gemini_helper import ask_gemini

def google_search(query: str):
    """
    Performs a Google search using the Serper API with robust error handling.
    """
    print(f"Executing Google Search for query: {query}")
    
    # Step 1: Securely get the API key from Streamlit secrets
    api_key = st.secrets.get("SERPER_API_KEY")
    if not api_key:
        error_msg = "ERROR: SERPER_API_KEY is missing from Streamlit secrets. I cannot perform a web search."
        print(error_msg)
        return error_msg

    # Step 2: Prepare and send the request
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # This will raise an exception for 4xx or 5xx status codes
        
        search_results = response.json()
        
        # Step 3: Check if the results are valid
        if not search_results or not search_results.get("organic"):
            error_msg = f"I performed a search for '{query}' but did not find any relevant results."
            print(error_msg)
            return error_msg
            
        # Step 4: Prepare the context and ask Gemini for a summary
        context = f"Based on the following real-time search results, please provide a concise answer to the user's query: '{query}'\n\n--- Search Results ---\n"
        for result in search_results["organic"][:5]: # Use top 5 results
            context += f"Title: {result.get('title', 'N/A')}\n"
            context += f"Snippet: {result.get('snippet', 'N/A')}\n"
            context += f"Link: {result.get('link', 'N/A')}\n\n"
        context += "--- End of Search Results ---"
            
        print("Sending search context to Gemini for summarization.")
        return ask_gemini(context)

    except requests.exceptions.HTTPError as http_err:
        # This will catch errors like 401 Unauthorized (bad API key) or 402 Payment Required
        error_msg = f"API ERROR: A web search API error occurred: {http_err}. This could be due to an invalid API key or a billing issue."
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"UNEXPECTED ERROR: An unexpected error occurred during the web search: {e}"
        print(error_msg)
        return error_msg