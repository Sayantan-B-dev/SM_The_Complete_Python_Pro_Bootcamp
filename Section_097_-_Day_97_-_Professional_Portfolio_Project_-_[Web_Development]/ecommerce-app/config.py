import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-dev-key')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
    SQLITECLOUD_CONNECTION_STRING = os.getenv('SQLITECLOUD_CONNECTION_STRING')
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')