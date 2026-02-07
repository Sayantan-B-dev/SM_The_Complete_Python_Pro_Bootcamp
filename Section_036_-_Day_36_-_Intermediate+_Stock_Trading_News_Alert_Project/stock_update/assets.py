ASSET_MAP = {
    # STOCKS
    "apple": "AAPL",
    "tesla": "TSLA",
    "google": "GOOGL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "paypal": "PYPL",
    "intel": "INTC",
    "amd": "AMD",
    "ibm": "IBM",

    # INDICES / ETFs
    "s&p500": "SPY",
    "nasdaq": "QQQ",
    "dow jones": "DIA",

    # COMMODITIES
    "gold": "GLD",
    "silver": "SLV",
    "oil": "USO",

    # CRYPTO
    "bitcoin": "BTC-USD",
    "ethereum": "ETH-USD",

    # FOREX
    "usd inr": "USDINR",
    "eur usd": "EURUSD",
    "usd jpy": "USDJPY",
}


def resolve_asset(topic: str):
    topic = topic.lower().strip()

    symbol = ASSET_MAP.get(topic)
    if not symbol:
        return None, None

    if "-" in symbol:
        return "CRYPTO", symbol
    if symbol.isalpha() and len(symbol) <= 5:
        return "STOCK", symbol
    return "FOREX", symbol
