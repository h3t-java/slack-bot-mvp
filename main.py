from fastapi import FastAPI, Request, BackgroundTasks
import requests
import os
from dotenv import load_dotenv
from app.rag_pipeline import run_rag

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

app = FastAPI()

# Track processed events to prevent duplicates
processed_events = set()


def process_message(channel, user_text):
    """Run RAG and send message back to Slack."""

    print("Processing message:", user_text)

    answer = run_rag(user_text)

    print("Bot answer:", answer)

    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "channel": channel,
            "text": answer
        }
    )


@app.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks):

    data = await request.json()

    # Slack URL verification
    if data.get("type") == "url_verification":
        return {"challenge": data["challenge"]}

    event = data.get("event", {})
    event_id = data.get("event_id")

    print("Received event:", event)

    # Prevent duplicate processing
    if event_id in processed_events:
        print("Duplicate event ignored:", event_id)
        return {"status": "ignored"}

    processed_events.add(event_id)

    # Ignore bot messages
    if event.get("bot_id"):
        return {"status": "ignored"}

    # Only respond to mentions
    if event.get("type") == "app_mention":

        user_text = event.get("text")
        channel = event.get("channel")

        print("User asked:", user_text)

        # Process message in background
        background_tasks.add_task(
            process_message,
            channel,
            user_text
        )

    # Return immediately so Slack doesn't retry
    return {"status": "ok"}