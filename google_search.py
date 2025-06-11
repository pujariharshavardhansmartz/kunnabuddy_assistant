# --- File: google_search.py ---
import requests
import json
import streamlit as st
from gemini_helper import ask_gemini

def google_search(query: str):
    api_key = st.secrets.get("SERPER_API_KEY")
    if not api_key:
        return "ERROR: SERPER_API_KEY is missing from Streamlit secrets. I cannot perform a web search."

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()
        
        if not results.get("organic"):
            return f"I searched for '{query}' but found no results."

        context = f"Based on these search results, answer the user's query: '{query}'\n\n"
        for result in results["organic"][:5]:
            context += f"Title: {result.get('title')}\nSnippet: {result.get('snippet')}\n---\n"
        
        return ask_gemini(context)
    except Exception as e:
        return f"API ERROR: The web search failed. This could be due to an invalid API key or a billing issue. Error: {e}"