import requests
from datetime import datetime
from config import SHEETY_BASE_URL, SHEETY_BEARER_TOKEN, SHEETY_SHEET_NAME
from notification import log, error

HEADERS = {
    "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}",
    "Content-Type": "application/json"
}

def write_flight_record(record: dict) -> None:
    payload = {
        SHEETY_SHEET_NAME: {
            "recorded_at_utc": datetime.utcnow().isoformat(),
            "airline_name": record.get("airline_name"),
            "flight_iata_code": record.get("flight_iata"),
            "departure_airport_name": record.get("departure_airport"),
            "departure_iata_code": record.get("departure_iata"),
            "arrival_airport_name": record.get("arrival_airport"),
            "arrival_iata_code": record.get("arrival_iata"),
            "aircraft_model": record.get("aircraft_model"),
            "flight_status": record.get("flight_status"),
            "altitude_feet": record.get("altitude"),
            "ground_speed_kmh": record.get("speed"),
            "fun_fact": record.get("fun_fact")
        }
    }

    try:
        response = requests.post(
            SHEETY_BASE_URL,
            json=payload,
            headers=HEADERS,
            timeout=10
        )
    except requests.RequestException as exc:
        error(f"Sheety network failure: {exc}")
        return

    if 200 <= response.status_code < 300:
        log(
            f"Row inserted successfully | "
            f"flight={record.get('flight_iata')} | "
            f"status={response.status_code}"
        )
        return

    error(
        f"Sheety request failed | "
        f"status={response.status_code} | "
        f"body={response.text}"
    )
