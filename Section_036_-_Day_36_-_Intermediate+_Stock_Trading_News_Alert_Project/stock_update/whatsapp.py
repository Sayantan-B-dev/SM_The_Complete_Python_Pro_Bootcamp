import os
import time
from pathlib import Path
from twilio.rest import Client

LOCK_FILE = Path("whatsapp_last_sent.txt")
COOLDOWN_SECONDS = 12 * 60 * 60  # 12 hours


def _can_send() -> bool:
    if not LOCK_FILE.exists():
        return True

    try:
        last_sent = float(LOCK_FILE.read_text().strip())
        return (time.time() - last_sent) >= COOLDOWN_SECONDS
    except Exception:
        return True


def _mark_sent():
    LOCK_FILE.write_text(str(time.time()))


def send_whatsapp_alert(message: str) -> bool:
    if not _can_send():
        return False

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_number = os.getenv("MY_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number, to_number]):
        return False

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=f"whatsapp:{from_number}",
            to=f"whatsapp:{to_number}",
        )
        _mark_sent()
        return True
    except Exception:
        return False
