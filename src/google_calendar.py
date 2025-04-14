# google_calendar.py
import os
import datetime
import json
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
# SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
# Obtener la ruta del archivo JSON desde .env
json_path = Path(__file__).parent.parent / os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_JSON"
).strip('"')

# Cargar el contenido del archivo
with open(json_path, "r") as f:
    SERVICE_ACCOUNT_INFO = json.load(f)

CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)


def create_event(summary, description, start_time, duration_minutes=30):
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)
    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/Mexico_City",
        },
        "end": {"dateTime": end_time.isoformat(), "timeZone": "America/Mexico_City"},
    }

    created_event = (
        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    )
    return created_event["id"]


def delete_event(event_id):
    service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
