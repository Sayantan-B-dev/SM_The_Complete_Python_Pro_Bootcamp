from app import db
from datetime import datetime

class ScheduledMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    schedule_type = db.Column(db.String(10), nullable=False)  # 'once', 'daily', 'interval'
    time_of_day = db.Column(db.String(5), nullable=True)      # for once/daily
    interval_seconds = db.Column(db.Integer, nullable=True)   # for interval (in seconds)
    next_run = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ScheduledMessage {self.to_number} - {self.next_run}>'