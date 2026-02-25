import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Load config.yaml
    with open('config.yaml', 'r') as f:
        automation_config = yaml.safe_load(f)

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', True)

    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    INPUT_DIR = os.path.join(DATA_DIR, 'input_data')
    OUTPUT_DIR = os.path.join(DATA_DIR, 'output_reports')

    # Ensure directories exist
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)