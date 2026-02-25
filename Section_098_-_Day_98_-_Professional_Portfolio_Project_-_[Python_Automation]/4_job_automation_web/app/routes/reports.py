from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import report_manager
from app.config import Config
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging

logger = logging.getLogger(__name__)
reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
def view_report():
    df = report_manager.read_report()
    if not df.empty:
        df = df.reset_index()
        df.rename(columns={'index': 'Statistic'}, inplace=True)
        for col in df.select_dtypes(include='number').columns:
            df[col] = df[col].round(2)
    records = df.to_dict('records')
    columns = df.columns.tolist()
    return render_template('reports.html', records=records, columns=columns)

@reports_bp.route('/send', methods=['POST'])
def send_report():
    recipient = request.form.get('recipient', '').strip()
    if not recipient:
        flash('Please provide a recipient email address.', 'warning')
        return redirect(url_for('reports.view_report'))

    # Check if report exists
    report_path = os.path.join(Config.OUTPUT_DIR, 'report.csv')
    if not os.path.exists(report_path):
        flash('No report file found. Run automation first.', 'danger')
        return redirect(url_for('reports.view_report'))

    # Load email config (SMTP settings only)
    email_config = Config.automation_config.get('email', {})
    smtp_server = email_config.get('smtp_server')
    smtp_port = email_config.get('smtp_port')
    sender = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')
    subject = email_config.get('subject', 'Automation Report')
    body = email_config.get('body', 'Please find attached the latest report.')

    # Validate SMTP settings
    if not smtp_server or not smtp_port:
        flash('SMTP server not configured in config.yaml', 'danger')
        return redirect(url_for('reports.view_report'))
    if not sender or not password:
        flash('Email sender credentials not set in .env', 'danger')
        return redirect(url_for('reports.view_report'))

    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(report_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename=report.csv'
            )
            msg.attach(part)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        flash(f'Report sent successfully to {recipient}', 'success')
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        flash(f'Failed to send email: {str(e)}', 'danger')

    return redirect(url_for('reports.view_report'))