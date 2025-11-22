import datetime
import os.path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def update_calendar_event(
    event_id: str,
    summary: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    attendees: Optional[list[str]] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
):
    """
    Updates an existing Google Calendar event.

    Args:
        event_id: The ID of the event to update.
        summary: The new summary or title of the event.
        start_time: The new start time in ISO 8601 format.
        end_time: The new end time in ISO 8601 format.
        attendees: A new list of email addresses for the attendees.
        description: The new description of the event.
        location: The new location of the event.

    Returns:
        A string confirming the update with a link to the event, or an error message.
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

        # First, get the existing event
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        # Update the fields if new values are provided
        if summary:
            event["summary"] = summary
        if location:
            event["location"] = location
        if description:
            event["description"] = description
        if start_time:
            event["start"]["dateTime"] = start_time
        if end_time:
            event["end"]["dateTime"] = end_time
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        updated_event = (
            service.events()
            .update(calendarId="primary", eventId=event["id"], body=event)
            .execute()
        )

        return f"Event updated: {updated_event.get('htmlLink')}"

    except HttpError as error:
        return f"An error occurred: {error}"
