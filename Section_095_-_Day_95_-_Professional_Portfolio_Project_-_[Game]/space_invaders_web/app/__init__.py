from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Needed for SocketIO

    from . import routes
    app.register_blueprint(routes.bp)

    # Use threading mode (compatible with Python 3.13)
    socketio.init_app(app, async_mode='threading')
    return app