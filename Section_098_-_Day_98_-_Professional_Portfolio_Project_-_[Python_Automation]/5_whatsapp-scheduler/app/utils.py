import pywhatkit
from flask import current_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_whatsapp_message(phone, message):
    try:
        wait_time = current_app.config.get('WHATSAPP_WAIT_TIME', 5)
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=wait_time,
            tab_close=True
        )
        logger.info(f"Message sent to {phone}")
        return True, "Message sent successfully."
    except Exception as e:
        logger.error(f"Failed to send to {phone}: {e}")
        return False, str(e)

def format_whatsapp_text(text):
    return text