import smtplib
import logging
import schedule
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

# Configure logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_template(name, boss_name, current_date, current_year, email):
    """Load email template and replace all placeholders."""
    try:
        with open(config.TEMPLATE_FILE, 'r', encoding='utf-8') as file:
            template = file.read()
        # Replace all placeholders
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
    except Exception as e:
        logging.error(f"Failed to load template: {e}")
        raise

def send_email(recipient, subject_prefix="", is_test=False):
    """Send HTML formatted email to specified recipient."""
    # Prepare email content
    current_date = datetime.now().strftime("%B %d, %Y")
    current_year = datetime.now().strftime("%Y")
    name = config.YOUR_NAME
    boss_name = config.BOSS_NAME if not is_test else "Test (Boss Name Placeholder)"
    email = config.EMAIL_ADDRESS
    
    # Load and process template
    html_content = load_template(name, boss_name, current_date, current_year, email)
    
    # Extract subject from HTML (looking for Subject: line at the top)
    lines = html_content.split('\n')
    subject = "Request for Salary Review"
    for line in lines:
        if line.startswith("Subject:"):
            subject = line.replace("Subject:", "").strip()
            html_content = html_content.replace(line, "", 1)  # Remove subject line from HTML
            break
    
    # Add prefix to subject if provided
    if subject_prefix:
        subject = subject_prefix + subject

    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = config.EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Create plain text version as fallback
    plain_text = f"""
    Dear {boss_name},

    I hope this email finds you well. I'm writing to request a discussion regarding my compensation.

    This email is best viewed in an HTML-compatible email client.

    Best regards,
    {name}
    """
    
    # Attach both plain text and HTML versions
    part1 = MIMEText(plain_text, 'plain')
    part2 = MIMEText(html_content, 'html')
    msg.attach(part1)
    msg.attach(part2)

    try:
        # Connect to SMTP server and send
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            server.send_message(msg)
        
        recipient_type = "📧 Test (self)" if is_test else "👔 Boss"
        log_msg = f"Email sent successfully to {recipient_type}: {recipient}"
        logging.info(log_msg)
        print(f"✅ {log_msg}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {e}")
        print(f"❌ Error sending email: {e}")
        return False

def job():
    """Wrapper for regular scheduled email to boss."""
    print(f"📨 Sending scheduled raise request to {config.BOSS_NAME}...")
    send_email(config.RECIPIENT_EMAIL, is_test=False)

def main():
    print("🚀 RAISE REQUEST EMAIL AUTOMATION")
    
    # Send test email to yourself on start if enabled
    if config.SEND_TEST_ON_START:
        print("\n📨 Sending test email to yourself...")
        success = send_email(
            recipient=config.YOUR_EMAIL, 
            subject_prefix="🔧 [TEST] ", 
            is_test=True
        )
        if success:
            print(f"✨ Test email sent to {config.YOUR_EMAIL}")
            print("💡 Check your inbox for the beautifully formatted HTML email!")
        else:
            print("❌ Test email failed. Check:")
            print("   - Email credentials in .env file")
            print("   - Internet connection")
            print("   - SMTP server settings")

    # Schedule the job
    schedule.every(config.RAISE_INTERVAL_DAYS).days.do(job)
    logging.info("Scheduler started. Will run every {} days to send emails to boss at: {}".format(
        config.RAISE_INTERVAL_DAYS, config.RECIPIENT_EMAIL))
    
    print(f"\n⏰ Scheduler Status:")
    print(f"   • Recipient: {config.BOSS_NAME} ({config.RECIPIENT_EMAIL})")
    print(f"   • Frequency: Every {config.RAISE_INTERVAL_DAYS} days")
    print(f"   • Next email: In {config.RAISE_INTERVAL_DAYS} days")
    print("\n⚠️  Press Ctrl+C to stop the scheduler")
    print("=" * 60)

    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # check every minute
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
        print("\n👋 Scheduler stopped. See you next time!")

if __name__ == "__main__":
    main()