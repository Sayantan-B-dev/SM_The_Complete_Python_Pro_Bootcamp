from rich.table import Table
from rich.panel import Panel
from rich import box
from assets import ASSET_MAP
from config import console


def show_available_assets():
    console.print(
        Panel(
            "Use with:\n[bold cyan]python main.py news_about=<keyword>[/bold cyan]",
            title="Available Asset Keywords",
            border_style="green",
        )
    )

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )

    table.add_column("Keyword", style="cyan")
    table.add_column("Symbol", style="yellow")

    for k, v in sorted(ASSET_MAP.items()):
        table.add_row(k, v)

    console.print(table)
