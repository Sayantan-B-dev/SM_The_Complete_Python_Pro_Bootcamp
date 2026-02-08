from aviation_client import fetch_live_flights
from fun_facts import random_aviation_fact
from sheet_writer import write_flight_record
from notification import log, warn

def main() -> None:
    log("Application startup initiated")

    flights = fetch_live_flights(limit=15)

    if not flights:
        warn("No flight data retrieved, aborting write operations")
        return

    for index, flight in enumerate(flights, start=1):
        flight["fun_fact"] = random_aviation_fact()
        log(f"Processing flight {index} with IATA code {flight.get('flight_iata')}")
        write_flight_record(flight)

    log("Application execution completed successfully")

if __name__ == "__main__":
    main()
