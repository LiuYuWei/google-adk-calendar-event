import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def delete_calendar_event(event_id: str):
    """
    Deletes a Google Calendar event.

    Args:
        event_id: The ID of the event to delete.

    Returns:
        A string confirming the deletion or an error message.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "calendar_agent/client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        service.events().delete(calendarId="primary", eventId=event_id).execute()

        return f"Event with ID {event_id} deleted successfully."

    except HttpError as error:
        return f"An error occurred: {error}"
