import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Your boss's email

# Your email for testing
YOUR_EMAIL = os.getenv("YOUR_EMAIL", EMAIL_ADDRESS)  # Default to your own email if not specified

# Names
YOUR_NAME = os.getenv("YOUR_NAME", "Your Name")
BOSS_NAME = os.getenv("BOSS_NAME", "Boss's Name")

# Log file
LOG_FILE = "scheduler.log"

# Template file
TEMPLATE_FILE = "email_template.txt"

# Raise interval in days (90 days ≈ 3 months)
RAISE_INTERVAL_DAYS = 90

# Send a test email to yourself when the script starts
SEND_TEST_ON_START = True