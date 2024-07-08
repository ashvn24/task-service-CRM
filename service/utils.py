import os.path
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from task_service.settings import CLIENT_SECRET_FILE_PATH
from datetime import timedelta
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

# If modifying these SCOPES, delete the file token.json.
CLIENT_SECRETS_FILE = CLIENT_SECRET_FILE_PATH
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=80)
        # Save the credentials for the next run
        with open('./token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def add_event_to_google_calendar(appointment):
    service = get_calendar_service()

    event = {
        'summary': 'Appointment for '+appointment.name,
        'location': 'St street, 789',
        'description': 'booked for an Appointment ',
        'start': {
            'dateTime': appointment.time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (appointment.time + timedelta(hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': appointment.email},
            {'email': 'ashwinvk77@gmail.com'}
        ],
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f"Google Calendar event created: {event}")
        return event.get('htmlLink')
    except Exception as e:
        logger.error(f"Failed to create Google Calendar event: {e}")
        return None
    
    finally:
        # Attempt to delete the temporary file
        try:
            os.remove("./token.json")
        except Exception as e:
            print(f"Error deleting temporary file: {e}")

