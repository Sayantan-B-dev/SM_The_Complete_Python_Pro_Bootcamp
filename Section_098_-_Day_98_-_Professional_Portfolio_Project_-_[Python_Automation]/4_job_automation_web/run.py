from app import create_app
from app.services.scheduler import scheduler
import atexit

app = create_app()

# Start scheduler automatically when app runs (optional)
# You may want to start it only if enabled in config.
# For now, we'll leave it off; user can start via web.
# scheduler.start()

# Ensure scheduler stops on app exit
atexit.register(scheduler.stop)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)