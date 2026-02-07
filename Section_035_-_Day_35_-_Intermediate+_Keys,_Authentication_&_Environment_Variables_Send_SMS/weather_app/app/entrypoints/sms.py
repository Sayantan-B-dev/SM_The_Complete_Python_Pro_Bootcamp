from app.services.weather_api import get_weather_data
from app.core.weather_analysis import analyze_weather
from app.services.reminder import (
    send_daily_weather_status,
    send_daily_weather_status_whatsapp,
)

import os
import dotenv
dotenv.load_dotenv()

SMS_MODE = os.getenv("SMS_MODE", "whatsapp")

def weather_status_to_phone(summary):
    sent = send_daily_weather_status(summary)
    print("SMS sent" if sent else "Already sent today")


def weather_status_to_whatsapp(summary):
    sent = send_daily_weather_status_whatsapp(summary)
    print("WhatsApp sent" if sent else "Already sent today")


def main():
    weather_data = get_weather_data("Kolkata")
    summary = analyze_weather(weather_data)

    if SMS_MODE == "whatsapp":
        weather_status_to_whatsapp(summary)
    elif SMS_MODE == "sms":
        weather_status_to_phone(summary)
    else:
        raise ValueError("Invalid SMS_MODE")


if __name__ == "__main__":
    main()
