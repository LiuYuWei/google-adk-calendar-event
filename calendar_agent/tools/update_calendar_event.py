from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendar_agent.tools.utils.credentials import get_credentials


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
    creds = get_credentials()

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
