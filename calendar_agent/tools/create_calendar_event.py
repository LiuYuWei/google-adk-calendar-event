import datetime
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendar_agent.tools.utils.credentials import get_credentials


def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    attendees: Optional[list[str]] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    add_google_meet: bool = False,
):
    """Creates a Google Calendar event, optionally with a Google Meet conference.

    Args:
        summary: The summary or title of the event.
        start_time: The start time of the event in ISO 8601 format
          (e.g., "2025-11-22T10:00:00+08:00").
        end_time: The end time of the event in ISO 8601 format
          (e.g., "2025-11-22T11:00:00+08:00").
        attendees: A list of email addresses of the attendees.
        description: A description of the event.
        location: The location of the event.
        add_google_meet: If True, a Google Meet conference will be added.

    Returns:
        A string containing the link to the event and/or Google Meet, or an error.
    """
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)

        # Prepare the description
        attendee_list_str = "\n".join([f"- {email}" for email in attendees]) if attendees else "None"
        
        description_header = (
            f"--- Meeting Details ---\n"
            f"Objective: {description or 'Not specified'}\n\n"
            f"Attendees:\n{attendee_list_str}\n"
            f"--------------------------"
        )

        event_body = {
            "summary": summary,
            "location": location,
            "description": description_header,
            "start": {"dateTime": start_time, "timeZone": "Asia/Taipei"},
            "end": {"dateTime": end_time, "timeZone": "Asia/Taipei"},
            "attendees": [{"email": email} for email in attendees] if attendees else [],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        if add_google_meet:
            conference_request = {
                "createRequest": {
                    "requestId": f"meet-{datetime.datetime.now().isoformat()}"
                }
            }
            event_body["conferenceData"] = conference_request

        event = (
            service.events()
            .insert(
                calendarId="primary",
                body=event_body,
                conferenceDataVersion=1 if add_google_meet else 0,
            )
            .execute()
        )

        event_link = event.get("htmlLink")
        meet_link = None
        if conference_data := event.get("conferenceData"):
            if entry_points := conference_data.get("entryPoints"):
                for entry_point in entry_points:
                    if entry_point.get("entryPointType") == "video":
                        meet_link = entry_point.get("uri")
                        break
        
        response_message = f"Event created: {event_link}"
        if meet_link:
            response_message += f" | Google Meet link: {meet_link}"

        return response_message

    except HttpError as error:
        return f"An error occurred: {error}"
