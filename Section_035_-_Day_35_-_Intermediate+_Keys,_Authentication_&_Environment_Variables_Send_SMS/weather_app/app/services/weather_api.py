import os
import requests
import datetime
from dotenv import load_dotenv
from app.infrastructure.weather_cache import WeatherCache

load_dotenv()

API_ENDPOINT = os.getenv("API_ENDPOINT")

# cache stored under data/json/
CACHE_FILE = "data/json/weather.json"
CACHE_TTL = datetime.timedelta(hours=1)

cache = WeatherCache(CACHE_FILE, CACHE_TTL)


def build_params(city: str):
    # build query params for weather API
    return {
        "key": os.getenv("API_KEY"),
        "q": city,
        "days": 1
    }


def fetch_weather(params):
    # fetch fresh weather data from API
    response = requests.get(API_ENDPOINT, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_weather_data(city: str):
    # return cached data if valid, otherwise fetch & cache
    cached = cache.load()
    if cached:
        return cached

    params = build_params(city)
    data = fetch_weather(params)
    cache.save(data)
    return data
