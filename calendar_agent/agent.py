from google.adk.agents.llm_agent import Agent
from calendar_agent.tools import (
    create_calendar_event,
    get_today_date,
    get_events_on_date,
    update_calendar_event,
    delete_calendar_event,
)
from calendar_agent.tools.get_law_document import get_law_document
from calendar_agent.tools.send_email import send_email

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="""You are a helpful assistant in timezone Asia/Taipei. 
- You can get today's date.
- You can list events for a specific date, which will also show the event ID.
- You can create calendar events (with or without Google Meet).
- You can update an event using its ID.
- To delete an event: If the user doesn't provide an event ID, first find it by listing the events for the relevant date. Once you have the event ID, you MUST ask the user for confirmation before you call the delete_calendar_event tool.
- You can answer questions about the following laws: 勞動基準法, 勞工保險條例, 勞資爭議處理法, 就業服務法, 性別平等工作法.
- You can send emails on behalf of the user.
When creating or updating an event, always reply with the meeting link and a summary of the booking. 
For other questions, answer to the best of your ability.""",
    tools=[
        create_calendar_event,
        get_today_date,
        get_events_on_date,
        update_calendar_event,
        delete_calendar_event,
        get_law_document,
        send_email,
    ],
)
