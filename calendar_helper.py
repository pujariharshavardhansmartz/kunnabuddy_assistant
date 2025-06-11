# --- File: calendar_helper.py ---
import json
import datetime as dt
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] # Read-only for safety first

def get_calendar_service():
    if 'google_token' not in st.session_state:
        return "ERROR: You are not logged into Google Calendar. The token is missing."
    
    try:
        creds = Credentials.from_authorized_user_info(st.session_state.google_token, SCOPES)
        if not creds or not creds.valid:
             return "ERROR: Your Google authentication token is invalid or expired."
        
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        return f"ERROR: Could not build Google Calendar service. Error: {e}"

def get_daily_briefing(day):
    service_or_error = get_calendar_service()
    if isinstance(service_or_error, str):
        return service_or_error
    
    # ... rest of the function is the same logic as before ...
    # This code only runs if get_calendar_service() was successful
    service = service_or_error
    now = dt.datetime.utcnow()
    time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary', timeMin=time_min, maxResults=10, 
        singleEvents=True, orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        return "You have no upcoming events today."
    
    briefing = "Here is your schedule for today:\n"
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_time = dt.datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%I:%M %p')
        briefing += f"- {event_time}: {event['summary']}\n"
    return briefing