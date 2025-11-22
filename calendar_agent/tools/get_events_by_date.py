import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendar_agent.tools.utils.credentials import get_credentials


def get_events_on_date(date: str):
    """
    Fetches events from the user's primary Google Calendar for a specific date.

    Args:
        date: The date to fetch events for, in 'YYYY-MM-DD' format.

    Returns:
        A formatted string listing the events for the day, or a message if no events are found.
    """
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)

        # Parse the input date and set the time range for the entire day
        start_time = datetime.datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z"
        end_time = (
            datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)
        ).isoformat() + "Z"

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return f"No events found on {date}."

        event_list = [f"Events on {date}:"]
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            # Format the start time to be more readable
            start_formatted = datetime.datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%H:%M')
            event_id = event['id']
            event_list.append(f"- {start_formatted}: {event['summary']} (ID: {event_id})")
        
        return "\n".join(event_list)

    except HttpError as error:
        return f"An error occurred: {error}"
