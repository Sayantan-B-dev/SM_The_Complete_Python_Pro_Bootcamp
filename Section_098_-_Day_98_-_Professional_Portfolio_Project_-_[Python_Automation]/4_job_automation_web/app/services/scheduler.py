import threading
import time
import logging
from app.services.automation_engine import run_automation_once

logger = logging.getLogger(__name__)

class AutomationScheduler:
    def __init__(self, interval_seconds=60):
        self.interval = interval_seconds
        self._running = False
        self._thread = None

    def start(self):
        if self._running:
            logger.warning("Scheduler already running")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("Automation scheduler started")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Automation scheduler stopped")

    def _run_loop(self):
        while self._running:
            try:
                run_automation_once()
            except Exception as e:
                logger.error(f"Error in automation cycle: {e}")
            # Wait for next interval
            for _ in range(self.interval):
                if not self._running:
                    break
                time.sleep(1)

# Global scheduler instance (to be used by routes)
scheduler = AutomationScheduler(interval_seconds=60)  # configurable