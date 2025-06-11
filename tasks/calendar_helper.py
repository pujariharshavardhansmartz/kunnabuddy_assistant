# --- File: calendar_helper.py (COMPLETE AND UPDATED) ---

import os.path
import pickle
import json
import datetime as dt
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file calendar_token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_credentials():
    """
    Handles Google Calendar authentication for both local and Streamlit Cloud.
    It reads credentials from st.secrets and manages the token.
    Returns: googleapiclient.discovery.Resource object or None if auth fails.
    """
    creds = None
    
    # Priority 1: Check for token in Streamlit's session state
    if 'google_token' in st.session_state:
        token_info = st.session_state.google_token
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)

    # Priority 2: If not in session, check for a local token file
    elif os.path.exists('calendar_token.pickle'):
        with open('calendar_token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, initiate the authentication flow.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                return None # Failed to refresh
        else:
            try:
                # Load configuration from Streamlit secrets, NOT from a file
                creds_info = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
                flow = InstalledAppFlow.from_client_config(creds_info, SCOPES)
                # Note: This will require one final local run to generate the token
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error during new authentication flow: {e}")
                return None # Auth flow failed

        # Save the credentials for the next run
        with open('calendar_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        # Also save to Streamlit session state for the current session
        st.session_state.google_token = json.loads(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building calendar service: {e}")
        return None


def get_daily_briefing(day):
    """Gets events for today or tomorrow from Google Calendar."""
    service = get_calendar_credentials()
    if not service:
        return "I'm sorry, I couldn't authenticate with Google Calendar. Please check the setup."

    if day.lower() == 'today':
        start_of_day = dt.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    elif day.lower() == 'tomorrow':
        start_of_day = (dt.datetime.utcnow() + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return "I can only check the schedule for 'today' or 'tomorrow'."

    end_of_day = start_of_day + dt.timedelta(days=1)
    
    start_of_day_iso = start_of_day.isoformat() + 'Z'  # 'Z' indicates UTC time
    end_of_day_iso = end_of_day.isoformat() + 'Z'

    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_of_day_iso,
            timeMax=end_of_day_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return f"You have no upcoming events scheduled for {day}."

        briefing = f"Here is your schedule for {day}:\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # Format time for display
            event_time = dt.datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%I:%M %p')
            summary = event['summary']
            briefing += f"- At {event_time}: {summary}\n"
        return briefing

    except Exception as e:
        return f"An error occurred while accessing the calendar: {e}"


def create_calendar_event(summary, start_time):
    """Creates a new event in the user's primary Google Calendar."""
    service = get_calendar_credentials()
    if not service:
        return "I'm sorry, I couldn't authenticate with Google Calendar. Please check the setup."

    try:
        # Assuming start_time is in 'YYYY-MM-DDTHH:MM:SS' format
        start = dt.datetime.fromisoformat(start_time)
        # Default to a 1-hour duration
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