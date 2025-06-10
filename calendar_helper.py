# --- UPDATED FILE: tasks/calendar_helper.py (with Write-Access Scope) ---

import datetime
import os.path
import pickle
from dateutil import parser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- THIS IS THE CRITICAL CHANGE ---
# We are changing the scope to allow reading AND writing to the calendar.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
# --- END OF CHANGE ---

CREDENTIALS_FILE = 'credentials.json' 
TOKEN_FILE = 'calendar_token.pickle'

def _get_calendar_service():
    """Authenticates with Google and returns a service object to interact with the API."""
    # (The rest of this function remains the same, but is included for completeness)
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("INFO: Refreshing expired Google Calendar token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"CRITICAL ERROR: '{CREDENTIALS_FILE}' not found. Please follow Google API setup.")
            
            print(f"INFO: No valid token found. Initiating Google Calendar authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
            print("INFO: Google Calendar token saved.")
            
    return build("calendar", "v3", credentials=creds)

def get_daily_briefing(day="today"):
    """Fetches events for a given day ('today' or 'tomorrow') and returns a formatted string."""
    # (This function remains the same)
    try:
        service = _get_calendar_service()
        
        now = datetime.datetime.utcnow()
        if day == "tomorrow":
            start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(days=1)
        else:
            start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)

        end_of_day = start_of_day + datetime.timedelta(days=1)

        time_min = start_of_day.isoformat() + "Z"
        time_max = end_of_day.isoformat() + "Z"

        print(f"INFO: Fetching calendar events for {day}...")
        events_result = service.events().list(
            calendarId="primary", 
            timeMin=time_min,
            timeMax=time_max,
            maxResults=20,
            singleEvents=True, 
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        
        if not events:
            return f"You have no upcoming events on your calendar for {day}."
        
        briefing = f"Here is your schedule for {day}:\n"
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            start_time = parser.isoparse(start)
            
            if 'date' in event['start']:
                formatted_time = "All day"
            else:
                formatted_time = start_time.strftime("%I:%M %p")

            briefing += f"- {formatted_time}: {event['summary']}\n"
            
        return briefing.strip()

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred while accessing Google Calendar: {e}"

# --- NEW FUNCTION TO CREATE EVENTS ---
def create_calendar_event(event_details):
    """Creates a new event in the primary Google Calendar."""
    try:
        service = _get_calendar_service()
        
        # We need start and end times, and a summary (title)
        start_time_str = event_details.get("start_time")
        summary = event_details.get("summary")

        if not start_time_str or not summary:
            return "To create an event, I need at least a title and a start time."

        # Convert the string time to a datetime object
        start_time = parser.isoparse(start_time_str)
        # Default to a 1-hour duration if no end time is given
        end_time = event_details.get("end_time")
        if end_time:
            end_time = parser.isoparse(end_time)
        else:
            end_time = start_time + datetime.timedelta(hours=1)

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kolkata', # You can change this to your local timezone
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
        }

        # Add attendees if they exist
        attendees = event_details.get("attendees")
        if attendees:
            event['attendees'] = [{'email': email.strip()} for email in attendees]

        print(f"INFO: Creating event: '{summary}'")
        created_event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
        
        return f"Successfully created the event: '{created_event.get('summary')}'."

    except Exception as e:
        return f"An error occurred while creating the calendar event: {e}"