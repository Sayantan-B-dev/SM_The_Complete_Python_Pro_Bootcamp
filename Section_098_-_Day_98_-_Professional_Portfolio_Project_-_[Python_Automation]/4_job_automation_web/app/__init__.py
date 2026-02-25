from flask import Flask
from app.config import Config
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.data import data_bp
    from app.routes.reports import reports_bp
    from app.routes.automation import automation_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(data_bp, url_prefix='/data')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(automation_bp, url_prefix='/automation')

    return app