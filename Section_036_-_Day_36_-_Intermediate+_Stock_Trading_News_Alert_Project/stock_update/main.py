from news import get_news_data
from ui import show_available_assets
from stocks import get_stock_percentage_change
from assets import resolve_asset
from config import console, STOCK_API_KEY, NEWS_API_KEY
from whatsapp import send_whatsapp_alert
import sys


def get_news_topic():
    for arg in sys.argv[1:]:
        if arg.startswith("news_about="):
            return arg.split("=", 1)[1]
    return "apple"


topic = get_news_topic()
asset_type, symbol = resolve_asset(topic)

if not asset_type:
    console.print("[red]Unknown asset keyword.[/red]")
    show_available_assets()
    sys.exit(1)


# --------------------------------
# FUNCTION + PARAMETER SELECTION
# --------------------------------
if asset_type == "STOCK":
    function = "TIME_SERIES_DAILY"
    stock_params = {
        "function": function,
        "symbol": symbol,
        "apikey": STOCK_API_KEY,
    }

elif asset_type == "CRYPTO":
    function = "DIGITAL_CURRENCY_DAILY"
    stock_params = {
        "function": function,
        "symbol": symbol.replace("-USD", ""),
        "market": "USD",
        "apikey": STOCK_API_KEY,
    }

elif asset_type == "FOREX":
    function = "FX_DAILY"
    base, quote = symbol[:3], symbol[3:]
    stock_params = {
        "function": function,
        "from_symbol": base,
        "to_symbol": quote,
        "apikey": STOCK_API_KEY,
    }


news_params = {
    "q": topic,
    "apiKey": NEWS_API_KEY,
    "country": "us",
    "pageSize": 3,
}

change = get_stock_percentage_change(stock_params)

if change is None:
    console.print("[red]Unable to retrieve market data.[/red]")

elif change > 5:
    console.print(f"[bold green]📈 {symbol} moved {change}% — showing news[/bold green]")
    get_news_data(news_params, render=True)

    send_whatsapp_alert(
        f"📈 {symbol} moved {change}%.\nCheck latest market news."
    )

else:
    console.print(f"[bold yellow]📊 {symbol} change: {change}%[/bold yellow]")
    show_available_assets()
