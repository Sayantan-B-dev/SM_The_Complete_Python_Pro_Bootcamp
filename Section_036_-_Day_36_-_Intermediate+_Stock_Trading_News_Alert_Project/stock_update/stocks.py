import requests
from config import STOCK_ENDPOINT, console


TIME_SERIES_MAP = {
    "TIME_SERIES_DAILY": {
        "series": "Time Series (Daily)",
        "close": "4. close",
    },
    "FX_DAILY": {
        "series": "Time Series FX (Daily)",
        "close": "4. close",
    },
    "DIGITAL_CURRENCY_DAILY": {
        "series": "Time Series (Digital Currency Daily)",
        "close": "4a. close (USD)",
    },
}


def get_stock_percentage_change(stock_params):
    try:
        response = requests.get(STOCK_ENDPOINT, params=stock_params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"[red]Network error:[/red] {e}")
        return None

    data = response.json()

    # ----------------------------------
    # EXPLICIT ALPHA VANTAGE STATES
    # ----------------------------------
    if "Information" in data:
        console.print(
            "[bold yellow]⚠ Alpha Vantage INFORMATION response[/bold yellow]\n"
            f"{data['Information']}\n\n"
            "This means the request was NOT executed.\n"
            "Common reasons:\n"
            "• API key in demo / restricted mode\n"
            "• backend throttling\n"
            "• temporary key cooldown"
        )
        return None

    if "Note" in data:
        console.print(
            "[bold yellow]⚠ Alpha Vantage RATE LIMIT[/bold yellow]\n"
            f"{data['Note']}"
        )
        return None

    if "Error Message" in data:
        console.print(
            "[bold red]❌ Alpha Vantage API ERROR[/bold red]\n"
            f"{data['Error Message']}"
        )
        return None

    # ----------------------------------
    # NORMAL PARSING
    # ----------------------------------
    function = stock_params.get("function")
    schema = TIME_SERIES_MAP.get(function)

    if not schema:
        console.print("[red]Unsupported Alpha Vantage function.[/red]")
        return None

    series_key = schema["series"]
    close_key = schema["close"]

    if series_key not in data:
        console.print(
            "[red]Unexpected Alpha Vantage payload.[/red]\n"
            f"Expected key: {series_key}\n"
            f"Actual keys: {list(data.keys())}"
        )
        return None

    series = data[series_key]
    dates = list(series.keys())

    if len(dates) < 2:
        console.print("[yellow]Not enough data points.[/yellow]")
        return None

    try:
        latest = float(series[dates[0]][close_key])
        previous = float(series[dates[1]][close_key])
    except (KeyError, ValueError):
        console.print(
            "[red]Price field mismatch.[/red]\n"
            f"Expected close key: {close_key}\n"
            f"Available keys: {list(series[dates[0]].keys())}"
        )
        return None

    return round(((latest - previous) / previous) * 100, 2)
