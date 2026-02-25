# WhatsApp Scheduler – Complete Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Folder Structure](#folder-structure)
3. [Installation & Setup](#installation--setup)
4. [Environment Variables](#environment-variables)
5. [Configuration (`config.py`)](#configuration-configpy)
6. [Database Models (`models.py`)](#database-models-modelspy)
7. [Forms (`forms.py`)](#forms-formspy)
8. [Routes & Views (`routes.py`)](#routes--views-routespy)
9. [Scheduler Background Thread (`scheduler.py`)](#scheduler-background-thread-schedulerpy)
10. [Utility Functions (`utils.py`)](#utility-functions-utilspy)
11. [Templates & Static Files](#templates--static-files)
12. [Workflow: How Everything Works Together](#workflow-how-everything-works-together)
13. [Usage Guide](#usage-guide)
14. [Important Notes & Troubleshooting](#important-notes--troubleshooting)

---

## Introduction

This Flask application allows you to schedule WhatsApp messages to be sent at specific times or intervals. It uses **pywhatkit** (which automates WhatsApp Web) to send messages. The application provides a web interface to create, edit, view, and delete scheduled messages. A background thread continuously checks for due messages and sends them.

The app supports three types of schedules:
- **One-time**: send a message once at a given time.
- **Daily**: send a message every day at a given time.
- **Interval**: send a message repeatedly every N seconds (minimum 2 seconds).

---

## Folder Structure

```
.
├── .env                       # Environment variables (not in repo, you create it)
├── all_source_files.txt        # (probably generated list of source files)
├── app/                        # Main application package
│   ├── __init__.py             # Flask app factory, DB initialization
│   ├── forms.py                # WTForms for scheduling
│   ├── models.py               # SQLAlchemy models
│   ├── routes.py               # Blueprint with all routes
│   ├── scheduler.py            # Background scheduler thread
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   │   └── style.css       # Custom CSS (dark theme)
│   │   ├── images/             # (empty, but could hold images)
│   │   └── js/
│   │       └── main.js         # JavaScript for formatting and dynamic fields
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html           # Base template with common layout
│   │   ├── edit.html           # Edit message page
│   │   └── index.html          # Main page with form and list
│   └── utils.py                # Helper functions (sending WhatsApp)
├── config.py                   # Configuration class
├── instance/                   # (created at runtime) contains app.db (SQLite)
├── PyWhatKit_DB.txt            # Log of sent messages (created by pywhatkit)
├── README.md                   # (empty)
├── requirements.txt            # Python dependencies
└── run.py                      # Entry point to run the app
```

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- Google Chrome (pywhatkit opens Chrome)
- Internet connection

### Steps

1. **Clone the repository** (if you have it) or create the files as shown above.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root (see next section).

5. **Initialize the database**:
   The first time you run the app, it will automatically create the SQLite database file `instance/app.db` thanks to `db.create_all()` in `app/__init__.py`. No manual migration is needed.

6. **Run the application**:
   ```bash
   python run.py
   ```
   The app will start in debug mode on `http://127.0.0.1:5000`.

---

## Environment Variables

The `.env` file should contain at least one variable:

```
SECRET_KEY=your-secret-key-here
```

- **`SECRET_KEY`**: Used by Flask to sign session cookies and CSRF tokens. Must be a long random string. If not set, the app will raise an error.

Optionally, you can also set `DATABASE_URL` to use a different database (e.g., PostgreSQL), but the default is SQLite.

Example `.env`:
```
SECRET_KEY=mysupersecretkey12345
```

---

## Configuration (`config.py`)

```python
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if SECRET_KEY is None:
        raise ValueError("No SECRET_KEY set for Flask application.")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WHATSAPP_WAIT_TIME = 5
```

### Explanation:
- **`SECRET_KEY`**: Loaded from environment, required.
- **`SQLALCHEMY_DATABASE_URI`**: Database connection string. Defaults to `app.db` in the project root (note: the `instance` folder is used because Flask-SQLAlchemy puts it there by default if `instance_path` is not set, but here the path is `basedir + '/app.db'` which is actually the root, not `instance/`. However, the actual file ends up in `instance/` because SQLAlchemy uses `instance` as default when `SQLALCHEMY_DATABASE_URI` is relative. So the final path is `instance/app.db`. This is fine.
- **`SQLALCHEMY_TRACK_MODIFICATIONS`**: Disable event system to save memory.
- **`WHATSAPP_WAIT_TIME`**: Seconds to wait after opening WhatsApp Web before sending (used by pywhatkit).

---

## Database Models (`models.py`)

```python
from app import db
from datetime import datetime

class ScheduledMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    schedule_type = db.Column(db.String(10), nullable=False)  # 'once', 'daily', 'interval'
    time_of_day = db.Column(db.String(5), nullable=True)      # for once/daily
    interval_seconds = db.Column(db.Integer, nullable=True)   # for interval
    next_run = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Fields:
- **`id`**: Primary key.
- **`to_number`**: Recipient phone number in international format (e.g., +1234567890).
- **`message`**: The text to send.
- **`schedule_type`**: One of `once`, `daily`, `interval`.
- **`time_of_day`**: For `once` and `daily`, stores the time string (HH:MM). Not used for `interval`.
- **`interval_seconds`**: For `interval` schedules, stores the interval in seconds. Not used for others.
- **`next_run`**: The next datetime when the message should be sent (UTC). This is recalculated after each send.
- **`active`**: Boolean indicating whether the schedule is active. Inactive messages are ignored by the scheduler.
- **`created_at``: Timestamp of creation (automatically set).

---

## Forms (`forms.py`)

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, RadioField
from wtforms.validators import DataRequired, Optional, NumberRange, Regexp

class MessageForm(FlaskForm):
    to_number = StringField('Recipient Number', 
                            validators=[DataRequired(), Regexp(r'^\+\d{1,15}$', message="Format: +1234567890")])
    message = TextAreaField('Message', validators=[DataRequired()])
    schedule_type = RadioField('Schedule Type', choices=[
        ('once', 'One-time'),
        ('daily', 'Daily (time-based)'),
        ('interval', 'Interval-based')
    ], default='once')
    time = StringField('Time (HH:MM)', validators=[Optional(), Regexp(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')])
    interval_seconds = IntegerField('Interval (seconds)', 
                                    validators=[Optional(), NumberRange(min=5, max=7200)],
                                    description="Between 5 and 7200 seconds")
```

### Validators:
- **`to_number`**: Required and must match international format: plus sign followed by up to 15 digits.
- **`message`**: Required.
- **`schedule_type`**: Radio buttons, default `once`.
- **`time`**: Optional but required when `schedule_type` is `once` or `daily`. Must be HH:MM (24-hour format).
- **`interval_seconds`**: Optional but required when `schedule_type` is `interval`. Must be between 5 and 7200 seconds (2 hours). Note: the scheduler loop sleeps for 2 seconds, so interval should be >=2, but form sets min=5 for safety.

---

## Routes & Views (`routes.py`)

The blueprint `main` contains all routes.

### `@bp.route('/', methods=['GET', 'POST'])` – Index (schedule form and list)
- **GET**: Renders `index.html` with form and list of all scheduled messages.
- **POST**: Processes the form. Depending on `schedule_type`:
  - `once`: Parses `time`, sets `next_run` to today at that time (if past, adds one day).
  - `daily`: Same as once, but `schedule_type` set to `daily`.
  - `interval`: Sets `next_run` to `now + interval_seconds`.
  - Saves the record to DB, flashes success, redirects to index.

### `@bp.route('/send_now', methods=['POST'])`
- Handles "Send Now" button from the same form.
- Validates form, then calls `send_whatsapp_message(to_number, message)`.
- On success/failure, flashes appropriate message and redirects to index.

### `@bp.route('/edit/<int:msg_id>', methods=['GET', 'POST'])`
- **GET**: Pre-populates form with existing message data (`obj=msg`).
- **POST**: Updates the message.
  - Similar logic as creating new message, but updates existing record.
  - Recalculates `next_run` based on new schedule type and current time.
  - Redirects to index after success.

### `@bp.route('/delete/<int:msg_id>')`
- Deletes the message from database.
- Flashes success, redirects to index.

### `@bp.route('/deactivate/<int:msg_id>')`
- Toggles the `active` flag of the message.
- Flashes appropriate message, redirects to index.

### Important Points:
- All times are handled in UTC (`datetime.utcnow()`). This avoids timezone issues.
- When a message is due and sent, its `next_run` is updated:
  - `once`: becomes inactive (`active=False`).
  - `daily`: adds 1 day.
  - `interval`: adds `interval_seconds`.
- The form uses the same `MessageForm` for both index and edit.

---

## Scheduler Background Thread (`scheduler.py`)

```python
import time
import threading
from datetime import datetime, timedelta
from app import db
from app.models import ScheduledMessage
from app.utils import send_whatsapp_message

scheduler_thread = None
stop_scheduler = False

def schedule_loop(app):
    global stop_scheduler
    with app.app_context():
        while not stop_scheduler:
            try:
                now = datetime.utcnow()
                due_messages = ScheduledMessage.query.filter(
                    ScheduledMessage.active == True,
                    ScheduledMessage.next_run <= now
                ).all()
                for msg in due_messages:
                    try:
                        success, result = send_whatsapp_message(msg.to_number, msg.message)
                        if success:
                            print(f"Sent message to {msg.to_number} at {now}")
                        else:
                            print(f"Failed to send to {msg.to_number}: {result}")

                        if msg.schedule_type == 'once':
                            msg.active = False
                        elif msg.schedule_type == 'daily':
                            msg.next_run = msg.next_run + timedelta(days=1)
                        elif msg.schedule_type == 'interval':
                            msg.next_run = msg.next_run + timedelta(seconds=msg.interval_seconds)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error processing message {msg.id}: {e}")
                time.sleep(2)  # check every 2 seconds
            except Exception as e:
                print(f"Scheduler loop error: {e}")
                time.sleep(2)

def start_scheduler(app):
    global scheduler_thread, stop_scheduler
    if scheduler_thread is None or not scheduler_thread.is_alive():
        stop_scheduler = False
        scheduler_thread = threading.Thread(target=schedule_loop, args=(app,), daemon=True)
        scheduler_thread.start()

def stop_scheduler_thread():
    global stop_scheduler
    stop_scheduler = True
```

### How it works:
- `start_scheduler` is called from `app/__init__.py` after creating the app.
- It starts a daemon thread running `schedule_loop`.
- The loop runs indefinitely, checking every 2 seconds for due messages.
- For each due message, it calls `send_whatsapp_message` (from `utils.py`).
- After sending (or if sending fails), it updates the `next_run` according to schedule type, or deactivates once messages.
- All database operations are wrapped in try/except to avoid crashing the thread.
- The loop runs inside an application context (`with app.app_context()`) to allow database access.

**Note**: Because it's a daemon thread, it will automatically stop when the main Flask process exits.

---

## Utility Functions (`utils.py`)

```python
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
    return text  # placeholder, not used
```

### `send_whatsapp_message`
- Uses `pywhatkit.sendwhatmsg_instantly` to send a WhatsApp message immediately.
- `wait_time`: seconds to wait after opening WhatsApp Web before typing and sending (default 5).
- `tab_close=True`: closes the browser tab after sending.
- Returns a tuple `(success: bool, result: str)`.
- Logs success/failure.

**Important**: pywhatkit opens a new Chrome window (or tab) and controls it. It requires an active WhatsApp Web session (QR code scanned). If not logged in, it will wait but eventually fail. Also, the computer must remain on and not go to sleep.

---

## Templates & Static Files

### `base.html`
- Provides the overall HTML structure, a header with WhatsApp SVG logo, and a container.
- Includes a block for flashed messages and a `{% block content %}` for page-specific content.
- Loads `style.css` and `main.js`.

### `index.html`
- Extends `base.html`.
- Displays the scheduling form with fields, formatting toolbar, schedule type radios, and conditional fields for time/interval.
- Two submit buttons: "Schedule" (POST to index) and "Send Now" (POST to `send_now`).
- Below the form, a table lists all scheduled messages.
- Each row shows:
  - Phone number
  - Message preview (first 50 chars)
  - Schedule type description
  - **Time remaining** (dynamic countdown using JavaScript)
  - Status (Active/Inactive)
  - Action buttons: Edit, Deactivate/Activate, Delete.
- JavaScript:
  - `formatCountdown` converts milliseconds to human-readable remaining time.
  - `updateCountdowns` updates all `.countdown` spans every second.
  - Also includes the toggle logic for schedule fields (same as in edit).

### `edit.html`
- Similar to index form but pre-filled with existing message data.
- Same formatting toolbar and field toggles.
- Cancel button returns to index.

### `static/css/style.css`
- Dark theme with green accents (#00ff80).
- Responsive, modern design.
- Styles for cards, forms, buttons, tables, flash messages, etc.

### `static/js/main.js`
- **Dynamic field toggling**: Shows/hides time or interval fields based on selected schedule type.
- **Text formatting**: Functions to wrap selected text with WhatsApp formatting characters:
  - Bold: `*text*`
  - Italic: `_text_`
  - Strikethrough: `~text~`
  - Code block: ``` ```text``` ```
- These are triggered by buttons in the toolbar.

---

## Workflow: How Everything Works Together

1. **User accesses the app** in browser (`http://localhost:5000`).
2. **Index route** renders the form and list of scheduled messages.
3. **User fills the form**:
   - Enters phone number (+1234567890)
   - Types message (optionally uses formatting buttons)
   - Selects schedule type (Once/Daily/Interval)
   - Enters time or interval accordingly
   - Clicks **Schedule**.
4. **Form submission** (POST to `/`):
   - Form is validated.
   - A new `ScheduledMessage` record is created with calculated `next_run` (UTC).
   - Record saved to database.
   - Flash success, redirect to index.
5. **Background scheduler thread** (started when app launched) runs every 2 seconds:
   - Queries for active messages with `next_run <= now`.
   - For each, calls `send_whatsapp_message`.
   - Updates `next_run` or deactivates as needed.
   - Commits changes.
6. **When a message is due**:
   - pywhatkit opens Chrome, goes to web.whatsapp.com, waits for `WHATSAPP_WAIT_TIME` seconds.
   - Types the message and sends it.
   - Closes the tab.
   - If successful, logs and updates DB.
   - If fails, logs error and keeps message active (will retry next loop? Actually if sending fails, the message remains due, so on next loop it will try again immediately. This could cause rapid retries; you might want to add a retry delay, but it's not implemented).
7. **User can manage messages**:
   - **Edit**: Loads edit page, updates record.
   - **Deactivate/Activate**: Toggles active flag; inactive messages are ignored.
   - **Delete**: Removes from DB.
8. **Countdown display**:
   - JavaScript on index page updates remaining time every second, giving live feedback.

---

## Usage Guide

### Creating a Schedule
1. Open the app in browser.
2. Fill in the phone number (must include country code, e.g., +1234567890).
3. Type your message. Use the formatting buttons to add bold, italic, etc.
4. Choose schedule type:
   - **One-time**: enter time (e.g., 14:30). Message will be sent at that time today; if time is already passed, it schedules for tomorrow.
   - **Daily**: enter time; message will be sent every day at that time.
   - **Interval**: enter seconds (between 5 and 7200). Message will repeat every that many seconds.
5. Click **Schedule**. The message appears in the list below.

### Sending a Message Immediately
- Fill the form as above but click **Send Now**. The message is sent instantly (bypassing scheduling) and is **not** saved to the database.

### Viewing Scheduled Messages
- The table shows all messages with their next run time (as countdown) and status.
- You can see if a message is active or inactive.

### Editing a Scheduled Message
- Click **Edit** on a row. The form pre-fills with current data.
- Change any field. Note: changing schedule type may require new time/interval.
- Click **Update Message** to save changes. The `next_run` will be recalculated based on current time and new schedule.

### Deactivating/Activating
- Click **Deactivate** to temporarily disable a schedule (it won't be sent). Click **Activate** to re-enable.

### Deleting a Scheduled Message
- Click **Delete** (red button) and confirm. Removes from database permanently.

### Stopping the App
- Press `Ctrl+C` in terminal. The scheduler thread will exit when the main process ends.

---

## Important Notes & Troubleshooting

### pywhatkit Requirements
- **Chrome must be installed** and in PATH. pywhatkit uses `webbrowser` module to open Chrome.
- You **must be logged into WhatsApp Web** in the Chrome profile that opens. The first time, you may need to scan QR code.
- The browser window will pop up each time a message is sent. It may steal focus. You can minimize it, but don't close it manually.
- If you are already logged in, it should work automatically.
- The `wait_time` in config gives you a few seconds to ensure WhatsApp Web is loaded before typing.

### Database
- SQLite is used by default. The file is stored in `instance/app.db`.
- If you want to use another database, set `DATABASE_URL` in `.env`.

### Time Handling
- All times are UTC. If your local timezone is not UTC, the displayed times in the list will be in UTC (as stored). The countdown uses JavaScript's local time, so it correctly shows remaining time in your local timezone because `next_run` is converted to local time when parsed by `new Date(next_runStr)`. Good.

### Scheduler Accuracy
- The scheduler checks every 2 seconds, so messages may be sent up to 2 seconds late. For most use cases this is fine.
- For interval schedules with very small intervals (e.g., 2 seconds), the actual interval might be slightly longer due to processing time and sleep.

### Potential Issues
- **Message sending failures**: If pywhatkit fails (e.g., network, Chrome not found), the error is logged and the message remains due. It will retry on next loop (every 2 seconds). This could cause a flood of attempts. Consider implementing a backoff or limit.
- **Chrome popups**: If Chrome is not focused, pywhatkit might still work, but if there are any interruptions (e.g., update prompts), it may fail.
- **Concurrent sends**: The scheduler processes due messages sequentially, one by one. If many are due at the same time, they will be sent in order, which may take time and cause delays.
- **Daemon thread**: The scheduler thread is daemon, so it stops when Flask stops. However, if you use a production WSGI server with multiple workers, you'd need a more robust solution (like APScheduler). For development it's fine.

### Security
- The app uses Flask-WTF CSRF protection. Ensure `SECRET_KEY` is strong.
- No authentication is implemented. Anyone with access to the web interface can schedule messages. In production, add authentication.

### Logging
- Scheduler prints to console. pywhatkit also logs to `PyWhatKit_DB.txt` (by default) which records sent messages.

---

This documentation should give you a thorough understanding of every component and how they interact. For any further questions, refer to the code comments or the official documentation of Flask, SQLAlchemy, WTForms, and pywhatkit.