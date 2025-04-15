# google_calendar.py
import os
import datetime
import json
import pytz
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Get environment variables
service_account_json_value = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
TIMEZONE = os.getenv("TIMEZONE", "America/Mexico_City")

# Better handling of service account JSON
SERVICE_ACCOUNT_INFO = None
try:
    # First try to parse as JSON string
    SERVICE_ACCOUNT_INFO = json.loads(service_account_json_value)
except (json.JSONDecodeError, TypeError):
    try:
        # If that fails, try as a file path
        with open(service_account_json_value, "r") as f:
            SERVICE_ACCOUNT_INFO = json.load(f)
    except Exception as e:
        print(f"Error loading Google Service Account: {e}")
        # Provide fallback implementation or raise error
        raise RuntimeError("Could not load Google Service Account credentials")

# Create credentials and service
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)


def create_event(summary, description, start_time, duration_minutes=30):
    """Create an event in Google Calendar"""
    # Ensure timezone is applied
    local_tz = pytz.timezone(TIMEZONE)
    if start_time.tzinfo is None:
        start_time = local_tz.localize(start_time)

    end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": TIMEZONE,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": TIMEZONE,
        },
    }

    try:
        created_event = (
            service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        )
        print(f"Event created: {created_event.get('htmlLink')}")
        return created_event["id"]
    except HttpError as error:
        print(f"An error occurred creating the event: {error}")
        raise


def delete_event(event_id):
    """Delete an event from Google Calendar"""
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        print(f"Event {event_id} deleted")
        return True
    except HttpError as error:
        print(f"An error occurred deleting the event: {error}")
        raise


def update_event(
    event_id, summary=None, description=None, start_time=None, duration_minutes=30
):
    """Update an existing event in Google Calendar"""
    try:
        # First get the existing event
        event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

        # Update fields if provided
        if summary:
            event["summary"] = summary
        if description:
            event["description"] = description

        if start_time:
            # Ensure timezone is applied
            local_tz = pytz.timezone(TIMEZONE)
            if start_time.tzinfo is None:
                start_time = local_tz.localize(start_time)

            end_time = start_time + datetime.timedelta(minutes=duration_minutes)

            event["start"] = {
                "dateTime": start_time.isoformat(),
                "timeZone": TIMEZONE,
            }
            event["end"] = {
                "dateTime": end_time.isoformat(),
                "timeZone": TIMEZONE,
            }

        updated_event = (
            service.events()
            .update(calendarId=CALENDAR_ID, eventId=event_id, body=event)
            .execute()
        )

        print(f"Event updated: {updated_event.get('htmlLink')}")
        return updated_event
    except HttpError as error:
        print(f"An error occurred updating the event: {error}")
        raise


def get_user_events(user_id, max_results=10):
    """Get upcoming events for a specific user"""
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

        # Get all upcoming events
        events_result = (
            service.events()
            .list(
                calendarId=CALENDAR_ID,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        # Filter events by user ID in description
        user_events = []
        for event in events:
            description = event.get("description", "")
            # Check if this event belongs to this user
            if f"user {user_id}" in description:
                user_events.append(event)

        return user_events
    except HttpError as error:
        print(f"An error occurred retrieving events: {error}")
        raise
