import os
import datetime
from dotenv import load_dotenv
from twilio.rest import Client

# file used to prevent duplicate daily messages
LAST_SENT_FILE = "data/txt/last_sms.txt"

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def already_sent_today() -> bool:
    # check if message was already sent today
    if not os.path.exists(LAST_SENT_FILE):
        return False

    with open(LAST_SENT_FILE, "r") as f:
        last_date = f.read().strip()

    return last_date == datetime.date.today().isoformat()


def mark_sent_today():
    # mark current date as sent
    os.makedirs(os.path.dirname(LAST_SENT_FILE), exist_ok=True)
    with open(LAST_SENT_FILE, "w") as f:
        f.write(datetime.date.today().isoformat())


def send_daily_weather_status(summary) -> bool:
    # send SMS once per day
    if already_sent_today():
        return False

    message_body = (
        f"Weather {summary['location']} {summary['date']}\n"
        f"Cond: {summary['current_condition']}\n"
        f"Temp: {summary['temp_min']}-{summary['temp_max']} C\n"
        f"Rain: {summary['rain_chance']}%\n"
        f"UV: {summary['uv_index']} {summary['uv_risk']}\n"
        f"Outdoor: {'Good' if summary['good_outdoor_day'] else 'Careful'}"
    )

    client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=MY_PHONE_NUMBER
    )

    mark_sent_today()
    return True


def send_daily_weather_status_whatsapp(summary) -> bool:
    # send WhatsApp message once per day
    if already_sent_today():
        return False

    message_body = (
        f"🌤 *Today's Weather – {summary['location']} ({summary['date']})*\n\n"
        f"*Condition:* {summary['current_condition']}\n"
        f"*Vibe:* {summary['vibe']}\n"
        f"*Temp:* {summary['temp_min']}°C → {summary['temp_max']}°C\n"
        f"*Feels like:* {summary['feels_like_now']}°C\n"
        f"*Rain chance:* {summary['rain_chance']}%\n"
        f"*UV Index:* {summary['uv_index']} ({summary['uv_risk']})\n"
        f"*Outdoor:* {'Good to go 👍' if summary['good_outdoor_day'] else 'Be careful ⚠️'}\n\n"
        f"🌅 Sunrise: {summary['sunrise']} | 🌇 Sunset: {summary['sunset']}"
    )

    client.messages.create(
        body=message_body,
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        to=f"whatsapp:{MY_PHONE_NUMBER}"
    )

    mark_sent_today()
    return True
