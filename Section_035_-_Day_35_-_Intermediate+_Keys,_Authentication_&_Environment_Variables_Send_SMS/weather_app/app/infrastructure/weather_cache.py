import os
import json
import datetime


class WeatherCache:
    def __init__(self, cache_file: str, ttl: datetime.timedelta):
        self.cache_file = cache_file
        self.ttl = ttl

    def _is_valid(self, timestamp: str) -> bool:
        # check if cached timestamp is within TTL
        ts = datetime.datetime.fromisoformat(timestamp)
        return datetime.datetime.now() - ts < self.ttl

    def load(self):
        # load cached weather data if present and valid
        if not os.path.exists(self.cache_file):
            return None

        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)

            if self._is_valid(data["timestamp"]):
                return data["weather_data"]

        except (json.JSONDecodeError, KeyError, ValueError):
            pass

        return None

    def save(self, weather_data):
        # save weather data with timestamp
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

        payload = {
            "weather_data": weather_data,
            "timestamp": datetime.datetime.now().isoformat()
        }

        with open(self.cache_file, "w") as f:
            json.dump(payload, f, indent=4)
