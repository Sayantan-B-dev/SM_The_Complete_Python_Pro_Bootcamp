# Automate Gym Class Bookings

## Project Overview
Automatically logs into your gym's booking system and reserves spots in your preferred classes when they become available.

## How It Works
- Uses Selenium to automate web browser interactions
- Logs into gym website with your credentials
- Navigates to class schedule and finds preferred classes
- Automatically clicks book button at the right time
- Handles confirmation dialogs and errors

## Files
- booking.py: Main booking automation script
- credentials.py: Login credentials (gitignored)
- config.py: Class preferences and timing
- requirements.txt: Python dependencies
- logs/: Directory for execution logs

## Setup Instructions
1. Install requirements: pip install -r requirements.txt
2. Install Chrome/Firefox and WebDriver
3. Configure gym URL, credentials, and class preferences
4. Schedule script to run at class release time

## Features
- Automatic login and navigation
- Precise timing for class release
- Multiple class preferences
- Error handling and retry logic
- Booking confirmation logging

## Challenges Addressed
- Dynamic website structure
- CAPTCHA and 2FA handling
- Precise timing requirements
- AJAX-loaded content
