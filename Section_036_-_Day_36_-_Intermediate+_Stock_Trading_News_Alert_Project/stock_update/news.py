
import requests
from rich.panel import Panel
from config import NEWS_ENDPOINT, console
from article import render_article


def get_news_data(news_params, render=True, limit=3):
    try:
        response = requests.get(NEWS_ENDPOINT, params=news_params, timeout=10)
    except requests.RequestException as e:
        console.print(
            Panel(str(e), title="Network Error", border_style="red")
        )
        return []

    if response.status_code != 200:
        console.print(
            Panel(
                f"Status: {response.status_code}\n\n{response.text}",
                title="News API Error",
                border_style="red",
            )
        )
        return []

    data = response.json()
    articles = data.get("articles", [])[:limit]

    if not articles:
        console.print(
            Panel(
                "No articles returned.\n\n"
                "If using top-headlines, make sure 'country' or 'sources' is set.",
                title="No News Data",
                border_style="yellow",
            )
        )
        return []

    if render:
        for idx, article in enumerate(articles, start=1):
            render_article(article, idx)

    return articles
