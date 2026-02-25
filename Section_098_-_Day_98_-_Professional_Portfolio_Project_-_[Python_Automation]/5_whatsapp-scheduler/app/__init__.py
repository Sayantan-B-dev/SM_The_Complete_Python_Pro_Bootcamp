from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models FIRST so they are registered with SQLAlchemy
    from app import models   # <-- moved before create_all

    # Now create tables (models are known)
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")  # optional confirmation

    # Register blueprints and start scheduler
    from app import routes
    app.register_blueprint(routes.bp)

    from app.scheduler import start_scheduler
    start_scheduler(app)

    return app