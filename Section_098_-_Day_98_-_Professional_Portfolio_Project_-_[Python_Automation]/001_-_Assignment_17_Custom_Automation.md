## 1. Automate an Email to Your Boss for a Raise Every 3 Months

### Folder Structure
```
raise_email_automation/
│
├── main.py
├── config.py
├── email_template.txt
├── requirements.txt
└── scheduler.log
```

### Needs
- Python 3.x
- Libraries: `smtplib`, `email`, `schedule` (or `APScheduler`), `python-dotenv` (optional)
- Access to an email account (Gmail, Outlook, etc.) with SMTP settings
- A text file containing the email template

### What It Does
Automatically sends a polite reminder/request for a raise to your boss every three months. The email content can be personalized with your name, date, and achievements.

### How It Does
1. Reads email credentials and recipient address from environment variables or a config file.
2. Loads the email template from `email_template.txt` and replaces placeholders (e.g., `{name}`, `{date}`) with actual values.
3. Uses `smtplib` to connect to the SMTP server (e.g., Gmail's `smtp.gmail.com`) and send the email.
4. Uses a scheduling library like `schedule` to run the job every 90 days. The script can be kept running in the background or triggered via a cron job.

### Challenges
- Handling email authentication securely (avoid hardcoding passwords).
- SMTP server restrictions (e.g., Gmail may require an "App Password" if 2FA is enabled).
- Ensuring the script runs continuously or is scheduled correctly.
- Avoiding spam filters by crafting a natural email.

### Simplified Version
- Use a plain text email without HTML formatting.
- Run the script manually every three months (no scheduler).
- Store credentials in a separate file ignored by Git.

### Advanced Version
- Integrate with a calendar API to check for holidays or your boss's availability.
- Use a more sophisticated email template with HTML and attachments (e.g., a list of achievements).
- Add logging and error notifications (e.g., send an SMS if the email fails).
- Use a cloud scheduler (e.g., AWS Lambda with CloudWatch Events) for reliability.

---

## 2. Automate Your Lights So They Switch On When Your Phone Is Within the Radius of Your House

### Folder Structure
```
smart_lights_automation/
│
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

### Needs
- Python 3.x
- Libraries: `ping3` or `scapy` (for network presence), `requests` (for controlling smart devices via API)
- Smart lights with a local API (e.g., Philips Hue, TP-Link Kasa) or a web interface
- Your phone's IP address (static or reserved via DHCP)

### What It Does
Turns on your lights automatically when your phone connects to your home Wi-Fi (i.e., when it's within range). Conversely, turns them off when you leave.

### How It Does
1. Periodically pings your phone's IP address to check if it's on the network.
2. If the phone becomes reachable and lights are off, it sends an API call to turn them on.
3. If the phone becomes unreachable and lights are on, it sends an API call to turn them off.
4. The script runs continuously, checking every minute or so.

### Challenges
- Phone IP may change (use DHCP reservation or hostname).
- Ping may be blocked by some phones (use ARP scanning instead).
- Different smart light brands have different APIs; some may require authentication.
- Handling edge cases (e.g., phone briefly disconnects due to sleep mode).

### Simplified Version
- Use a simple script that runs once when you log into your computer (e.g., via cron at boot) and checks presence, then controls a smart plug via a web interface using Selenium.
- Or use IFTTT with location triggers (less code, but not pure Python).

### Advanced Version
- Use Bluetooth proximity instead of Wi-Fi (e.g., with `pybluez`).
- Integrate with multiple users (family members) and set rules (e.g., only turn on if after sunset).
- Use machine learning to learn your arrival patterns and pre-heat/cool the house.
- Add a mobile app with a manual override.

---

## 3. Automatically Organise the Files in Your Downloads Folder Based on File Type

### Folder Structure
```
downloads_organizer/
│
├── organizer.py
├── config.json
├── requirements.txt
└── README.md
```

### Needs
- Python 3.x
- Libraries: `os`, `shutil`, `pathlib` (standard library)
- Optionally `watchdog` for real-time monitoring

### What It Does
Scans your Downloads folder (or any specified folder) and moves files into subfolders based on their extensions (e.g., Images, Documents, Archives, etc.). It can also clean up old files.

### How It Does
1. Defines a mapping of file extensions to folder names (e.g., `.jpg`, `.png` → "Images").
2. Iterates over all files in the source directory.
3. For each file, checks its extension, determines the target subfolder, creates the folder if it doesn't exist, and moves the file.
4. Optionally logs actions and handles duplicate filenames by renaming.

### Challenges
- Handling files that are in use (permission errors).
- Deciding what to do with unknown extensions (e.g., put in "Others").
- Avoiding moving files that are still being downloaded (use a delay or check if file size is stable).
- Cross-platform path handling.

### Simplified Version
- Hardcode the folder mapping and run the script manually.
- Skip files that are less than a minute old to avoid moving incomplete downloads.

### Advanced Version
- Use `watchdog` to monitor the folder in real-time and move files as soon as they appear.
- Add a GUI (e.g., with Tkinter) to configure rules.
- Integrate with cloud storage (e.g., move photos to Google Photos).
- Categorize by file content (e.g., using `python-magic` to detect MIME types).

---

## 4. Automate Your Gym Class Bookings

### Folder Structure
```
gym_booking/
│
├── booking.py
├── credentials.py
├── config.py
├── requirements.txt
└── logs/
```

### Needs
- Python 3.x
- Libraries: `selenium`, `webdriver-manager`, `datetime`, `time`
- Chrome/Firefox browser and corresponding WebDriver
- Gym website login credentials

### What It Does
Logs into your gym's booking system at a specified time (e.g., when classes become available) and automatically reserves a spot in your preferred class.

### How It Does
1. Uses Selenium to open the gym's login page and enter credentials.
2. Navigates to the class schedule page.
3. Finds the desired class (by date, time, or name) and clicks the "Book" button.
4. Handles any confirmation dialogs.
5. Optionally sends you a confirmation email or notification.

### Challenges
- Website structure may change (requires updating selectors).
- Handling CAPTCHA or two-factor authentication.
- Timing: you may need to run the script at a specific minute when bookings open.
- Dealing with dynamic content (AJAX) – use explicit waits.

### Simplified Version
- Hardcode the class details and run the script manually at the right time.
- Use a simple scheduler (e.g., `schedule` or cron) to trigger the script.

### Advanced Version
- Use headless browser mode for silent operation.
- Implement retry logic and error handling.
- Monitor multiple classes and book the first available.
- Use a cloud server (e.g., AWS EC2) to run the script 24/7.
- Add a web interface to configure bookings.

---

## 5. Automate Your Library Book Renewals

### Folder Structure
```
library_renewals/
│
├── renew.py
├── credentials.py
├── config.py
├── requirements.txt
└── logs/
```

### Needs
- Python 3.x
- Libraries: `selenium`, `webdriver-manager`, `datetime`
- Library website login credentials

### What It Does
Logs into your local library account, checks for borrowed books that are due soon, and automatically renews them if possible (and if renewals are allowed).

### How It Does
1. Uses Selenium to log into the library website.
2. Navigates to the "Loans" or "Checked Out" page.
3. Scrapes the list of books with their due dates.
4. For each book, if the due date is within a certain threshold (e.g., 2 days), it clicks the "Renew" button.
5. Handles any renewal limits or errors (e.g., book has holds).

### Challenges
- Library websites vary widely; need to adapt selectors.
- Some libraries may have CAPTCHA or require multi-factor authentication.
- Renewal may fail if the book is reserved by someone else.
- Due date parsing may be inconsistent.

### Simplified Version
- Manually run the script once a week to check and renew.
- Only renew books that are due today (ignore threshold).

### Advanced Version
- Send an email report of renewed items and any failures.
- Use a headless browser and run on a Raspberry Pi.
- Integrate with calendar to set reminders if renewal fails.
- Handle multiple library cards.

---

## 6. Automate Your Job (e.g., Repetitive Data Entry or Report Generation)

### Folder Structure
```
job_automation/
│
├── automate_task.py
├── config.yaml
├── input_data/
├── output_reports/
├── requirements.txt
└── README.md
```

### Needs
- Python 3.x
- Libraries: `selenium`, `pandas`, `openpyxl`, `requests`, `beautifulsoup4` (depending on task)
- Access to company systems (web apps, databases, email)

### What It Does
This project is intentionally broad – it automates a repetitive task you do at work. Examples:
- Extract data from emails and populate a spreadsheet.
- Generate weekly reports from a database and email them.
- Fill out web forms with data from a CSV file.
- Scrape information from internal websites and update a dashboard.

### How It Does
The implementation depends on the specific task. Typically:
1. Identify a repetitive workflow (e.g., logging into a web app, copying data from one place to another).
2. Break it down into steps that can be automated with Selenium (for web interactions) or other libraries (for file/data processing).
3. Write a script that performs each step, with error handling and logging.
4. Schedule the script to run at appropriate times (e.g., daily using cron).

### Challenges
- Company IT policies may block automation tools.
- Web apps may have anti-bot measures.
- Data formats may change.
- Need to ensure security of credentials and sensitive data.

### Simplified Version
- Start with a small, well-defined task (e.g., downloading a daily report from a website).
- Use simple file-based inputs/outputs.

### Advanced Version
- Build a full-fledged automation suite with a GUI or CLI.
- Integrate with multiple systems via APIs.
- Use machine learning to handle exceptions (e.g., classify emails).
- Implement robust logging and alerting.

---

## 7. Automate Your Home Chores (e.g., Reminders or Smart Appliance Control)

### Folder Structure
```
home_chores_automation/
│
├── chores.py
├── chores_list.json
├── config.py
├── requirements.txt
└── reminders.log
```

### Needs
- Python 3.x
- Libraries: `schedule`, `smtplib` (for email), `twilio` (for SMS), or `plyer` (for desktop notifications)
- Optional: smart home APIs (e.g., for controlling a robot vacuum)

### What It Does
Automates reminders for household chores (e.g., take out trash, water plants) or directly controls smart appliances (e.g., start the dishwasher at a specific time). It can send notifications via email, SMS, or desktop pop-ups.

### How It Does
1. Reads a list of chores with frequencies (e.g., "water plants: every 2 days") from a JSON file.
2. Uses a scheduler to trigger reminders at the appropriate times.
3. Sends a notification using the chosen method (e.g., email via SMTP, SMS via Twilio, or desktop notification via `plyer`).
4. Optionally logs when chores were last done and updates the schedule.

### Challenges
- Keeping track of completion (need a way to reset the timer).
- Avoiding notification fatigue.
- Integrating with smart devices (different APIs).
- Handling time zones and daylight saving.

### Simplified Version
- Use desktop notifications only.
- Manually reset the schedule after completing a chore.

### Advanced Version
- Use a database to track completion history.
- Integrate with smart home devices (e.g., turn on a smart plug for the coffee maker at 7 AM).
- Add voice notifications via a smart speaker.
- Create a mobile app to mark chores as done and sync with the server.
- Use a Raspberry Pi with sensors to detect when a chore is actually done (e.g., trash can lid opened).

---

Now that you have the details for all seven projects, choose one that resonates with you and start building! Remember to start simple and gradually add features. Happy automating!