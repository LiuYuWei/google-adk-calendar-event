from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendar_agent.tools.utils.credentials import get_credentials


def delete_calendar_event(event_id: str):
    """
    Deletes a Google Calendar event.

    Args:
        event_id: The ID of the event to delete.

    Returns:
        A string confirming the deletion or an error message.
    """
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)

        service.events().delete(calendarId="primary", eventId=event_id).execute()

        return f"Event with ID {event_id} deleted successfully."

    except HttpError as error:
        return f"An error occurred: {error}"
