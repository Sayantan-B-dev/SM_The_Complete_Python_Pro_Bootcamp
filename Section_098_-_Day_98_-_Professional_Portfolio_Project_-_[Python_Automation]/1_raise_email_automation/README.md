# Comprehensive Documentation: Automate Raise Request Email

## 1. Overview
This project automates the process of sending a quarterly raise request email to your boss. It uses Python to send a professionally formatted HTML email every 90 days. The script reads configuration from environment variables for security, loads an email template, and schedules itself to run continuously. It also sends a test email on startup to verify that everything is working correctly.

## 2. Folder Structure
```
raise_email_automation/
│
├── main.py              # Main automation script
├── config.py            # Configuration and environment variable loader
├── email_template.txt   # HTML email template with placeholders
├── requirements.txt     # Python dependencies
├── .env                 # (not committed) Environment variables file
├── scheduler.log        # Log file (created automatically)
└── README.md            # (optional) Project documentation
```

## 3. Prerequisites and Installation

### 3.1 Prerequisites
- Python 3.7 or higher installed on your system.
- An email account with SMTP access (Gmail, Outlook, Yahoo, etc.).
- For Gmail, you may need to generate an "App Password" if two-factor authentication is enabled.

### 3.2 Installation Steps
1. **Clone or create the project folder** and navigate into it.
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` file includes:
   - `schedule` – for periodic job scheduling
   - `python-dotenv` – for loading environment variables from a `.env` file
   - `APScheduler` – (optional, not used in the current script but listed)

## 4. Environment Variables Setup

Create a file named `.env` in the project root. This file will hold sensitive information and should never be committed to version control. Add the following variables:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password_or_regular_password
RECIPIENT_EMAIL=boss.email@company.com
YOUR_EMAIL=your.email@gmail.com
YOUR_NAME=Your Full Name
BOSS_NAME=Dr. Smith
```

### Explanation of each variable:

| Variable | Description | Example / Notes |
|----------|-------------|------------------|
| `SMTP_SERVER` | SMTP server address of your email provider. | Gmail: `smtp.gmail.com`, Outlook: `smtp-mail.outlook.com`, Yahoo: `smtp.mail.yahoo.com` |
| `SMTP_PORT` | Port for SMTP with TLS. Usually 587. | 587 for TLS, 465 for SSL (not used here) |
| `EMAIL_ADDRESS` | Your email address used to send the emails. | your.email@gmail.com |
| `EMAIL_PASSWORD` | Your email password or app-specific password. | For Gmail with 2FA, create an App Password. |
| `RECIPIENT_EMAIL` | Your boss's email address. | boss@company.com |
| `YOUR_EMAIL` | Your email for test messages. Defaults to `EMAIL_ADDRESS` if not set. | your.email@gmail.com |
| `YOUR_NAME` | Your full name, used in the email signature. | John Doe |
| `BOSS_NAME` | Your boss's name, used in the greeting. | Jane Smith |

### Obtaining credentials for common providers:

- **Gmail**:
  - If you have 2-step verification enabled, go to your Google Account → Security → App passwords. Generate an app password for "Mail" and use that in `EMAIL_PASSWORD`.
  - If 2-step verification is off, you may need to enable "Less secure app access" (not recommended) or use an app password anyway.

- **Outlook/Hotmail**:
  - Use `smtp-mail.outlook.com` and port 587. Your regular password should work, but consider enabling two-factor and using an app password if available.

- **Yahoo**:
  - Use `smtp.mail.yahoo.com` and port 587. Generate an app password from Yahoo account security settings.

## 5. Configuration Files

### 5.1 config.py
This file loads environment variables and sets default values. It also defines paths and the test flag.

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Email settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

YOUR_EMAIL = os.getenv("YOUR_EMAIL", EMAIL_ADDRESS)
YOUR_NAME = os.getenv("YOUR_NAME", "Your Name")
BOSS_NAME = os.getenv("BOSS_NAME", "Boss's Name")

LOG_FILE = "scheduler.log"
TEMPLATE_FILE = "email_template.txt"
RAISE_INTERVAL_DAYS = 90
SEND_TEST_ON_START = True
```

### 5.2 email_template.txt
This file contains the HTML email template with placeholders that will be replaced dynamically. The first line must start with `Subject:` to define the email subject. Placeholders:

- `{name}` – replaced with `YOUR_NAME`
- `{boss_name}` – replaced with `BOSS_NAME` (or a test placeholder)
- `{current_date}` – current date (e.g., "March 15, 2025")
- `{current_year}` – current year (e.g., "2025")
- `{email}` – replaced with `EMAIL_ADDRESS`

The template includes a professional design with a header, highlight box, achievements section, call-to-action button, and signature. Customize the achievements and other placeholders as needed.

## 6. Code Explanation

### 6.1 Imports and Logging
```python
import smtplib
import logging
import schedule
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
```
- `smtplib`: for sending emails via SMTP.
- `logging`: to record events and errors to a log file.
- `schedule`: for scheduling recurring jobs.
- `time`: for sleep intervals in the scheduler loop.
- `datetime`: to get current date and year.
- `email.mime`: to construct multipart emails (HTML + plain text).
- `config`: our local configuration module.

Logging is configured to write to `scheduler.log` with timestamps and log levels.

### 6.2 Function: `load_template`
```python
def load_template(name, boss_name, current_date, current_year, email):
    """Load email template and replace all placeholders."""
    with open(config.TEMPLATE_FILE, 'r', encoding='utf-8') as file:
        template = file.read()
    replacements = {
        '{name}': name,
        '{boss_name}': boss_name,
        '{current_date}': current_date,
        '{current_year}': current_year,
        '{email}': email
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template
```
This function reads the HTML template and replaces all placeholders with actual values. It raises an exception if the file cannot be read.

### 6.3 Function: `send_email`
This is the core function that constructs and sends the email.

- **Parameters**:
  - `recipient`: email address to send to.
  - `subject_prefix`: optional prefix to add to the subject (e.g., "[TEST] ").
  - `is_test`: boolean indicating if this is a test email; if True, uses a placeholder for boss name to avoid confusion.

- **Steps**:
  1. Get current date, year, name, boss name, and email from config.
  2. Call `load_template` to generate the HTML content.
  3. Extract the subject line from the template (looks for a line starting with "Subject:"). Remove that line from the HTML.
  4. Apply the subject prefix if provided.
  5. Create a `MIMEMultipart` message of type 'alternative' to include both plain text and HTML versions.
  6. Create a simple plain text fallback.
  7. Attach both parts to the message.
  8. Connect to the SMTP server using credentials, send the message, and log success/failure.

### 6.4 Function: `job`
```python
def job():
    print("Sending scheduled raise request to {config.BOSS_NAME}...")
    send_email(config.RECIPIENT_EMAIL, is_test=False)
```
This wrapper function is called by the scheduler. It sends the real email to your boss.

### 6.5 Function: `main`
The main function orchestrates the startup and scheduling.

- Prints a header.
- If `SEND_TEST_ON_START` is True, calls `send_email` to send a test email to `YOUR_EMAIL` with a subject prefix `[TEST] `.
- Schedules the `job` function to run every `RAISE_INTERVAL_DAYS` days.
- Prints scheduler status.
- Enters an infinite loop that checks for pending scheduled jobs every minute. The loop continues until interrupted by Ctrl+C, at which point it logs the stop and exits gracefully.

## 7. Running the Script

### 7.1 Test the script immediately
1. Ensure your `.env` file is correctly configured.
2. Run the script:
   ```bash
   python main.py
   ```
3. You will see output indicating that a test email is being sent to your own address. Check your inbox (and possibly spam folder) for the test email. It should be nicely formatted.
4. After the test, the scheduler starts and will wait 90 days before sending the real email.

### 7.2 Keep the script running continuously
The scheduler runs in a loop and must remain active. You can:
- Run it in a terminal session (will stop when you log out).
- Use a process manager like `systemd` (Linux) or `nssm` (Windows) to run it as a service.
- Use a cloud server or a Raspberry Pi to host the script 24/7.

Alternatively, you can use a cron job (Linux/macOS) or Task Scheduler (Windows) to run `send_email` directly every 90 days, bypassing the scheduler loop. To do that, you would modify `main.py` to call `send_email()` once and then exit, and schedule that script execution.

### 7.3 Stopping the script
Press `Ctrl+C` in the terminal to stop the scheduler gracefully. The script will log the interruption.

## 8. Logging and Monitoring
All significant events are logged to `scheduler.log`. This includes:
- Successful email sends (with recipient and type)
- Failures (with error messages)
- Scheduler start and stop

You can monitor the log file to ensure the script is working correctly.

## 9. Future Improvements
The current implementation is functional but can be extended in many ways:

1. **Better error handling and retries**: Automatically retry failed email sends after a delay.
2. **HTML template improvements**: Allow more dynamic content, such as including recent achievements from a CSV or database.
3. **Multiple recipients**: Send to HR or other stakeholders as needed.
4. **Calendar integration**: Check your boss's calendar to suggest meeting times automatically.
5. **Attachment support**: Attach a performance review document or resume.
6. **Alternative scheduling**: Use `APScheduler` for more robust scheduling (already listed in requirements but not used).
7. **Web interface**: Build a simple Flask app to configure settings and monitor logs.
8. **Multi-account support**: Handle multiple bosses or different email templates for different occasions.
9. **Analytics**: Track open rates (via read receipts or tracking pixels) – though this may be blocked by email clients.
10. **Cloud deployment**: Deploy as an AWS Lambda function with CloudWatch Events to avoid running a continuous script.

## 10. Conclusion
This automation project demonstrates how Python can be used to streamline a recurring professional task. By leveraging environment variables for security, HTML templates for professional presentation, and the schedule library for periodic execution, you have a robust system that requires minimal maintenance. Customize the template and settings to fit your personal style, and enjoy the peace of mind that your quarterly raise request will never be forgotten.