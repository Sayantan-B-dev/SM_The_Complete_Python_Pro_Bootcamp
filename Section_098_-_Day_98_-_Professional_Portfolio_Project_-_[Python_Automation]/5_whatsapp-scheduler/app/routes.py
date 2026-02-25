from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import ScheduledMessage
from app.forms import MessageForm
from app.utils import send_whatsapp_message
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        to_number = form.to_number.data
        message = form.message.data
        schedule_type = form.schedule_type.data
        now = datetime.utcnow()

        if schedule_type == 'once':
            time_str = form.time.data
            if not time_str:
                flash('Time is required for one-time schedule.', 'danger')
                return redirect(url_for('main.index'))
            hour, minute = map(int, time_str.split(':'))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
            scheduled = ScheduledMessage(
                to_number=to_number,
                message=message,
                schedule_type='once',
                time_of_day=time_str,
                next_run=next_run,
                active=True
            )
        elif schedule_type == 'daily':
            time_str = form.time.data
            if not time_str:
                flash('Time is required for daily schedule.', 'danger')
                return redirect(url_for('main.index'))
            hour, minute = map(int, time_str.split(':'))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
            scheduled = ScheduledMessage(
                to_number=to_number,
                message=message,
                schedule_type='daily',
                time_of_day=time_str,
                next_run=next_run,
                active=True
            )
        elif schedule_type == 'interval':
            interval_seconds = form.interval_seconds.data
            if not interval_seconds:
                flash('Interval is required.', 'danger')
                return redirect(url_for('main.index'))
            next_run = now + timedelta(seconds=interval_seconds)
            scheduled = ScheduledMessage(
                to_number=to_number,
                message=message,
                schedule_type='interval',
                interval_seconds=interval_seconds,
                next_run=next_run,
                active=True
            )
        else:
            flash('Invalid schedule type.', 'danger')
            return redirect(url_for('main.index'))

        db.session.add(scheduled)
        db.session.commit()
        flash('Message scheduled successfully!', 'success')
        return redirect(url_for('main.index'))

    messages = ScheduledMessage.query.order_by(ScheduledMessage.next_run).all()
    return render_template('index.html', form=form, messages=messages)

@bp.route('/send_now', methods=['POST'])
def send_now():
    form = MessageForm()
    if form.validate_on_submit():
        to_number = form.to_number.data
        message = form.message.data
        success, result = send_whatsapp_message(to_number, message)
        if success:
            flash('Message sent instantly!', 'success')
        else:
            flash(f'Failed to send: {result}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:msg_id>', methods=['GET', 'POST'])
def edit_message(msg_id):
    msg = ScheduledMessage.query.get_or_404(msg_id)
    form = MessageForm(obj=msg)  # pre-populate

    if form.validate_on_submit():
        msg.to_number = form.to_number.data
        msg.message = form.message.data
        msg.schedule_type = form.schedule_type.data

        now = datetime.utcnow()
        if msg.schedule_type == 'once':
            time_str = form.time.data
            if not time_str:
                flash('Time is required for one-time schedule.', 'danger')
                return redirect(url_for('main.edit_message', msg_id=msg_id))
            hour, minute = map(int, time_str.split(':'))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
            msg.time_of_day = time_str
            msg.interval_seconds = None
            msg.next_run = next_run
        elif msg.schedule_type == 'daily':
            time_str = form.time.data
            if not time_str:
                flash('Time is required for daily schedule.', 'danger')
                return redirect(url_for('main.edit_message', msg_id=msg_id))
            hour, minute = map(int, time_str.split(':'))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
            msg.time_of_day = time_str
            msg.interval_seconds = None
            msg.next_run = next_run
        elif msg.schedule_type == 'interval':
            interval_seconds = form.interval_seconds.data
            if not interval_seconds:
                flash('Interval is required.', 'danger')
                return redirect(url_for('main.edit_message', msg_id=msg_id))
            msg.time_of_day = None
            msg.interval_seconds = interval_seconds
            msg.next_run = now + timedelta(seconds=interval_seconds)
        else:
            flash('Invalid schedule type.', 'danger')
            return redirect(url_for('main.edit_message', msg_id=msg_id))

        db.session.commit()
        flash('Message updated successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('edit.html', form=form, msg=msg)

@bp.route('/delete/<int:msg_id>')
def delete_message(msg_id):
    msg = ScheduledMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/deactivate/<int:msg_id>')
def deactivate_message(msg_id):
    msg = ScheduledMessage.query.get_or_404(msg_id)
    msg.active = not msg.active
    db.session.commit()
    flash(f"Message {'activated' if msg.active else 'deactivated'}.", 'success')
    return redirect(url_for('main.index'))