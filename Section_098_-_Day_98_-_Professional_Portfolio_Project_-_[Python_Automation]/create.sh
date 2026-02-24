mkdir -p raise_email_automation smart_lights_automation downloads_organizer gym_booking library_renewals job_automation home_chores_automation && cd raise_email_automation && echo "smtplib
email
schedule
python-dotenv
apscheduler" > requirements.txt && echo "# Automate an Email to Your Boss for a Raise Every 3 Months

## Project Overview
This automation script sends a polite reminder/request for a raise to your boss every three months automatically.

## How It Works
- Reads email credentials and recipient address from environment variables
- Loads an email template with placeholders for personalization
- Connects to SMTP server (Gmail, Outlook, etc.) to send the email
- Uses scheduling library to run every 90 days

## Files
- main.py: Main script that sends the email
- config.py: Configuration settings and credentials
- email_template.txt: Template file for email content
- scheduler.log: Log file for tracking executions

## Setup Instructions
1. Install required packages: pip install -r requirements.txt
2. Configure email credentials in config.py or .env file
3. Customize email_template.txt with your message
4. Run the script manually or set up as a cron job

## Features
- Secure credential handling
- Email templating with personalization
- Scheduled execution every 3 months
- Logging for tracking

## Challenges Addressed
- Secure email authentication
- SMTP server restrictions
- Continuous execution management
- Spam filter avoidance" > plan.md && touch main.py config.py email_template.txt scheduler.log && cd ../smart_lights_automation && echo "ping3
scapy
requests
schedule
python-dotenv" > requirements.txt && echo "# Automate Your Lights When Phone Is Within Home Radius

## Project Overview
Automatically turns on your smart lights when your phone connects to your home Wi-Fi network, and turns them off when you leave.

## How It Works
- Periodically pings your phone's IP address to check network presence
- Detects when phone connects/disconnects from home network
- Sends API calls to smart lights (Philips Hue, TP-Link Kasa, etc.)
- Automates lighting based on your presence

## Files
- main.py: Main automation script
- config.py: Network and light configuration
- requirements.txt: Python dependencies
- README.md: Setup instructions

## Setup Instructions
1. Install requirements: pip install -r requirements.txt
2. Configure your phone's IP and light API in config.py
3. Set static IP for phone via DHCP reservation
4. Run main.py as a background service

## Features
- Presence detection via ping/ARP scanning
- Multi-brand smart light support
- Configurable check intervals
- Manual override options

## Challenges Addressed
- Dynamic IP changes (solved via DHCP reservation)
- Ping blocking on phones
- Different smart light APIs
- False triggers from brief disconnections" > plan.md && touch main.py config.py README.md && cd ../downloads_organizer && echo "# No external dependencies needed - uses os, shutil, pathlib" > requirements.txt && echo "# Automatically Organise Downloads Folder by File Type

## Project Overview
Scans your Downloads folder and automatically organizes files into categorized subfolders based on file extensions.

## How It Works
- Defines mapping of file extensions to folder categories
- Monitors Downloads folder for new files
- Moves files to appropriate subfolders (Images, Documents, Archives, etc.)
- Handles duplicate filenames and file conflicts

## Files
- organizer.py: Main organization script
- config.json: File type mapping configuration
- requirements.txt: Dependencies (standard library only)
- README.md: Usage instructions

## Setup Instructions
1. No external packages needed (uses Python standard library)
2. Customize config.json with your preferred categories
3. Run organizer.py manually or set up scheduled execution
4. Optionally install watchdog for real-time monitoring

## Features
- Customizable file type categories
- Duplicate filename handling
- Logging of all file movements
- Safe file moving with error handling

## Challenges Addressed
- Files in use/permission errors
- Unknown file extensions
- Partially downloaded files
- Cross-platform compatibility" > plan.md && touch organizer.py config.json README.md && cd ../gym_booking && echo "selenium
webdriver-manager
schedule
python-dotenv
datetime
requests" > requirements.txt && echo "# Automate Gym Class Bookings

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
- AJAX-loaded content" > plan.md && mkdir logs && touch booking.py credentials.py config.py && cd ../library_renewals && echo "selenium
webdriver-manager
beautifulsoup4
datetime
schedule
python-dotenv" > requirements.txt && echo "# Automate Library Book Renewals

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
- Renewal failure handling" > plan.md && mkdir logs && touch renew.py credentials.py config.py && cd ../job_automation && echo "selenium
pandas
openpyxl
requests
beautifulsoup4
pyautogui
schedule
python-dotenv
pyyaml" > requirements.txt && echo "# Automate Your Job Tasks

## Project Overview
Automates repetitive work tasks such as data entry, report generation, web form filling, and email processing.

## How It Works
- Identifies repetitive workflow patterns in your job
- Uses Selenium for web automation
- Processes data with pandas for spreadsheets
- Generates reports and sends emails automatically
- Handles file operations and data transformations

## Files
- automate_task.py: Main automation script
- config.yaml: Configuration settings
- input_data/: Directory for input files
- output_reports/: Directory for generated reports
- requirements.txt: Python dependencies
- README.md: Setup and usage guide

## Setup Instructions
1. Install requirements: pip install -r requirements.txt
2. Configure task parameters in config.yaml
3. Place input data in input_data folder
4. Run script manually or schedule with cron

## Features
- Web form automation with Selenium
- Excel/CSV data processing
- Report generation
- Email automation
- Error handling and logging
- Configurable workflows

## Challenges Addressed
- Company IT policies
- Anti-bot measures
- Changing data formats
- Secure credential storage" > plan.md && mkdir input_data output_reports && touch automate_task.py config.yaml README.md && cd ../home_chores_automation && echo "schedule
twilio
plyer
python-dotenv
requests
pyyaml
datetime" > requirements.txt && echo "# Automate Home Chores and Reminders

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
- Time zone handling" > plan.md && touch chores.py chores_list.json config.py reminders.log && cd ..