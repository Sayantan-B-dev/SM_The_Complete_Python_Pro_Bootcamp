# Automate Home Chores and Reminders

## Project Overview
Automates household chore reminders and can control smart home appliances for routine tasks.

## How It Works
- Reads chore list with frequencies from JSON/YAML
- Schedules reminders via desktop, email, or SMS
- Tracks when chores were last completed
- Optionally controls smart appliances via APIs
- Sends notifications through multiple channels

## Files
- chores.py: Main automation script
- chores_list.json: Chores with frequencies
- config.py: Notification and smart device config
- requirements.txt: Python dependencies
- reminders.log: Log of sent reminders

## Setup Instructions
1. Install requirements: pip install -r requirements.txt
2. Define your chores in chores_list.json
3. Configure notification methods in config.py
4. Run chores.py as a background service

## Features
- Multi-channel notifications (desktop, email, SMS)
- Smart home device integration
- Chore completion tracking
- Customizable schedules
- Logging and history

## Challenges Addressed
- Completion tracking
- Notification fatigue
- Smart device API integration
- Time zone handling
