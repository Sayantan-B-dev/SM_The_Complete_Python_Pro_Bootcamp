# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Network range to scan (adjust to your network)
NETWORK_RANGE = os.getenv("NETWORK_RANGE", "192.168.1.0/24")

# Scan interval in seconds
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", 5))

# Flask settings
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"