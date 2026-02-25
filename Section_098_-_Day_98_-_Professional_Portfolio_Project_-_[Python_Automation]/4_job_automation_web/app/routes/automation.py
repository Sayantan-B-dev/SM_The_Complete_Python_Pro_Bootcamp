from flask import Blueprint, render_template, jsonify, request
from app.services.scheduler import scheduler
from app.config import Config

automation_bp = Blueprint('automation', __name__)

@automation_bp.route('/')
def status():
    return render_template('automation.html',
                           running=scheduler._running,
                           interval=scheduler.interval)

@automation_bp.route('/start', methods=['POST'])
def start():
    scheduler.start()
    return jsonify({'status': 'started'})

@automation_bp.route('/stop', methods=['POST'])
def stop():
    scheduler.stop()
    return jsonify({'status': 'stopped'})

@automation_bp.route('/run_once', methods=['POST'])
def run_once():
    # Run automation in a separate thread to avoid blocking
    import threading
    def _run():
        from app.services.automation_engine import run_automation_once
        run_automation_once()
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return jsonify({'status': 'triggered'})