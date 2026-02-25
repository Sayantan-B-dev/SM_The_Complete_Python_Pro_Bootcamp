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
                time.sleep(2)  # ⬅️ reduced from 30s to 2s
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