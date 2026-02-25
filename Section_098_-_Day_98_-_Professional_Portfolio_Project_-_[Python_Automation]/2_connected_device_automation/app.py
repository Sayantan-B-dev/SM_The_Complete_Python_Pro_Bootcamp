# app.py
from flask import Flask, render_template, jsonify
from scanner import NetworkScanner
import config

app = Flask(__name__)
scanner = NetworkScanner()

# Start scanning in background
scanner.start_scanning()

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

@app.route('/api/devices')
def get_devices():
    """API endpoint to get all devices"""
    devices = scanner.get_all_devices()
    # Sort: connected first, then by last seen
    devices.sort(key=lambda x: (x['status'] != 'connected', x['last_seen']), reverse=True)
    return jsonify({
        'devices': devices,
        'stats': scanner.get_stats()
    })

@app.route('/api/connected')
def get_connected():
    """API endpoint to get only connected devices"""
    return jsonify(scanner.get_connected_devices())

@app.route('/api/stats')
def get_stats():
    """API endpoint to get scanner statistics"""
    return jsonify(scanner.get_stats())

if __name__ == '__main__':
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG,
        threaded=True
    )