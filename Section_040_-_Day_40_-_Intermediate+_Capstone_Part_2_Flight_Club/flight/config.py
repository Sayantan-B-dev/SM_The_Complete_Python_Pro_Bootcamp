import os
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
SHEETY_BASE_URL = os.getenv("SHEETY_BASE_URL")
SHEETY_BEARER_TOKEN = os.getenv("SHEETY_BEARER_TOKEN")
SHEETY_SHEET_NAME = os.getenv("SHEETY_SHEET_NAME", "sheet1")

missing = [
    name for name, value in {
        "AVIATIONSTACK_API_KEY": AVIATIONSTACK_API_KEY,
        "SHEETY_BASE_URL": SHEETY_BASE_URL,
        "SHEETY_BEARER_TOKEN": SHEETY_BEARER_TOKEN
    }.items() if not value
]

if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
