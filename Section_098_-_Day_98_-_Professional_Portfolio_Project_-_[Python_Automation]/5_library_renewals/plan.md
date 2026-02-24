# Automate Library Book Renewals

## Project Overview
Automatically logs into your library account, checks for books due soon, and renews them if possible.

## How It Works
- Logs into library website using Selenium
- Navigates to loans/checked out page
- Scrapes book titles and due dates
- Automatically renews books within threshold
- Handles renewal limits and errors

## Files
- renew.py: Main renewal script
- credentials.py: Library login credentials
- config.py: Due date threshold and settings
- requirements.txt: Python dependencies
- logs/: Execution logs directory

## Setup Instructions
1. Install requirements: pip install -r requirements.txt
2. Configure library URL and credentials
3. Set due date threshold in config.py
4. Schedule script to run weekly

## Features
- Automatic login to library account
- Due date monitoring with threshold
- One-click renewal automation
- Renewal limit checking
- Email/SMS notifications for failures

## Challenges Addressed
- Different library website structures
- CAPTCHA and authentication
- Due date parsing inconsistencies
- Renewal failure handling
