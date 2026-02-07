import os
from pathlib import Path
import dotenv
from rich.console import Console

BASE_DIR = Path(__file__).resolve().parent
dotenv.load_dotenv(BASE_DIR / ".env")

console = Console()

STOCK_ENDPOINT = os.getenv("ALPHAVANTAGE_STOCK_ENDPOINT")
NEWS_ENDPOINT = os.getenv("NEWS_ENDPOINT")

STOCK_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
