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