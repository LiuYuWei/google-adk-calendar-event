import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendar_agent.tools.utils.credentials import get_credentials


def send_email(to: str, subject: str, body: str):
    """
    Sends an email using the user's Gmail account.

    Args:
        to: The recipient's email address.
        subject: The subject of the email.
        body: The content of the email.

    Returns:
        A string confirming that the email was sent, or an error message.
    """
    creds = get_credentials()

    try:
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["Subject"] = subject

        # Encode the message in base64
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )

        return f'Email sent successfully. Message ID: {send_message["id"]}'

    except HttpError as error:
        return f"An error occurred: {error}"
