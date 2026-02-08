import requests
from config import AVIATIONSTACK_API_KEY
from notification import log, warn, error

AVIATIONSTACK_BASE_URL = "https://api.aviationstack.com/v1/flights"

def fetch_live_flights(limit: int = 20) -> list[dict]:
    log(f"Requesting up to {limit} flight records from Aviationstack API")

    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "limit": limit
    }

    try:
        response = requests.get(
            AVIATIONSTACK_BASE_URL,
            params=params,
            timeout=15
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        error(f"Aviationstack request failed: {exc}")
        return []

    payload = response.json()

    if "error" in payload:
        error(f"Aviationstack API error: {payload['error']}")
        return []

    raw_records = payload.get("data", [])
    log(f"Aviationstack returned {len(raw_records)} raw flight records")

    flights = []

    for index, item in enumerate(raw_records, start=1):
        live_data = item.get("live") or {}

        if not live_data:
            warn(f"Flight record {index} contains no live telemetry data")

        flights.append({
            "airline_name": (item.get("airline") or {}).get("name"),
            "flight_iata": (item.get("flight") or {}).get("iata"),
            "departure_airport": (item.get("departure") or {}).get("airport"),
            "departure_iata": (item.get("departure") or {}).get("iata"),
            "arrival_airport": (item.get("arrival") or {}).get("airport"),
            "arrival_iata": (item.get("arrival") or {}).get("iata"),
            "aircraft_model": (item.get("aircraft") or {}).get("icao"),
            "flight_status": item.get("flight_status"),
            "altitude": live_data.get("altitude"),
            "speed": live_data.get("speed_horizontal")
        })

    log(f"Normalized {len(flights)} flight records successfully")
    return flights
