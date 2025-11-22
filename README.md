# Google ADK Calendar Agent

This project is a conversational agent built with the Google Agent Development Kit (ADK). It allows you to manage your Google Calendar through a chat interface.

## Features

- **Create Events**: Schedule new meetings, optionally with a Google Meet link.
- **Read Events**: List events for a specific date.
- **Update Events**: Modify existing meetings.
- **Delete Events**: Remove meetings from your calendar.
- **Get Today's Date**: A simple utility to get the current date.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LiuYuWei/google-adk-calendar-event.git
    cd google-adk-calendar-event
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r calendar_agent/requirements.txt
    ```

3.  **Google Calendar API Credentials:**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
    - Enable the "Google Calendar API".
    - Go to "APIs & Services" -> "OAuth consent screen".
        - Choose "External" and create an app.
        - Add your Google account email to the list of "Test users".
    - Go to "APIs & Services" -> "Credentials".
        - Click "+ CREATE CREDENTIALS" -> "OAuth client ID".
        - Choose "Desktop app" as the application type.
        - Download the JSON file and rename it to `client_secret.json`.
    - **Place the `client_secret.json` file inside the `calendar_agent/` directory.**

## Usage

You can interact with the agent by running the `main.py` script (which you can create) or by using the ADK's web interface.

1.  **Run the ADK Web Server:**
    ```bash
    adk web
    ```
    This will start a local server, usually at `http://127.0.0.1:8000`. You can interact with your agent through this web UI.

2.  **First-time Authentication:**
    The first time you use a calendar tool, your browser will open a new tab asking you to authorize the application. Log in with the Google account you added as a test user. A `token.json` file will be created to store your credentials for future sessions.

### Example Prompts

- "今天是什麼日子？"
- "明天有什麼會議？"
- "幫我預約一個會議，時間是明天早上 10 點到 11 點，主題是「專案狀態討論」，並且幫我建立 google meet。"
- "幫我更新 ID 為 `xxx` 的會議，把時間改到下午三點。"
- "幫我刪除關於「專案狀態討論」的會議。" (The agent will ask for confirmation)

---
*This agent was co-developed with an AI assistant.*
