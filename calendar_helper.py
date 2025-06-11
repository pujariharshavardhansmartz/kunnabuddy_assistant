# --- File: calendar_helper.py (COMPLETE AND CLOUD-READY) ---

import os.path
import pickle
import json
import datetime as dt
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Handles Google Calendar authentication and returns the service object.
    Returns a specific error string if authentication fails.
    """
    creds = None
    if 'google_token' in st.session_state:
        creds = Credentials.from_authorized_user_info(st.session_state.google_token, SCOPES)

    if not creds or not creds.valid:
        # THIS IS A CRITICAL ERROR MESSAGE FOR THE CLOUD
        # It means the user has never logged in successfully in this session.
        return "I can't access Google Calendar. It seems I'm not authenticated. This can happen on a new session or after a long time. Please try running the app locally once to re-authenticate."
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        return f"An error occurred while building the calendar service: {e}"

def get_daily_briefing(day):
    """Gets events for today or tomorrow from Google Calendar."""
    service_or_error = get_calendar_service()
    if isinstance(service_or_error, str):
        # If we got an error message string, return it directly.
        return service_or_error

    service = service_or_error
    # ... rest of the function is the same ...
    if day.lower() == 'today':
        start_of_day = dt.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    elif day.lower() == 'tomorrow':
        start_of_day = (dt.datetime.utcnow() + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return "I can only check the schedule for 'today' or 'tomorrow'."

    end_of_day = start_of_day + dt.timedelta(days=1)
    start_of_day_iso = start_of_day.isoformat() + 'Z'
    end_of_day_iso = end_of_day.isoformat() + 'Z'

    try:
        events_result = service.events().list(
            calendarId='primary', timeMin=start_of_day_iso, timeMax=end_of_day_iso,
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return f"You have no upcoming events scheduled for {day}."

        briefing = f"Here is your schedule for {day}:\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_time = dt.datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%I:%M %p')
            summary = event['summary']
            briefing += f"- At {event_time}: {summary}\n"
        return briefing
    except Exception as e:
        return f"An error occurred while accessing the calendar: {e}"

# The create_calendar_event function would also be updated similarly
def create_calendar_event(summary, start_time):
    service_or_error = get_calendar_service()
    if isinstance(service_or_error, str):
        return service_or_error
    
    service = service_or_error
    # ... rest of function ...
    try:
        start = dt.datetime.fromisoformat(start_time)
        end = start + dt.timedelta(hours=1)
        event = {
            'summary': summary,
            'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
        }
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created successfully! You can see '{created_event.get('summary')}' on your calendar."
    except Exception as e:
        return f"Failed to create event: {e}"