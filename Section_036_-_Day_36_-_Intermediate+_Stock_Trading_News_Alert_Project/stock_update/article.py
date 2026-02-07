# article.py

import datetime as dt
from rich.panel import Panel
from rich import box
from config import console


def _parse_datetime(iso_str: str) -> str:
    if not iso_str:
        return "Unknown date"

    try:
        # Handle Z → UTC offset
        if iso_str.endswith("Z"):
            iso_str = iso_str.replace("Z", "+00:00")

        dt_obj = dt.datetime.fromisoformat(iso_str)
        return dt_obj.strftime("%d %b %Y, %I:%M %p UTC")
    except Exception:
        return "Unknown date"


def render_article(article: dict, index: int | None = None):
    title = article.get("title") or "No title"
    source = article.get("source", {}).get("name") or "Unknown"
    description = article.get("description") or "No description"
    url = article.get("url") or "No URL"

    published = _parse_datetime(article.get("publishedAt"))

    panel_title = f"📰 Article {index}" if index else "📰 Article"

    console.print(
        Panel(
            f"[bold]Title:[/bold] {title}\n\n"
            f"[bold]Source:[/bold] {source}\n"
            f"[bold]Published:[/bold] {published}\n\n"
            f"[bold]Summary:[/bold]\n{description}\n\n"
            f"[bold]Link:[/bold] {url}",
            title=panel_title,
            border_style="cyan",
            box=box.ROUNDED,
        )
    )
