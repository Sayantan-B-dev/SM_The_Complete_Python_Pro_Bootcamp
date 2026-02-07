from rich.console import Console
from rich.panel import Panel

console = Console()


def print_weather_summary(summary):
    # format weather summary for terminal output
    text = (
        f"{summary['location']}, {summary['region']} ({summary['country']})\n"
        f"{summary['date']}\n\n"
        f"Condition : {summary['current_condition']}\n"
        f"Vibe      : {summary['vibe']}\n"
        f"Temp      : {summary['temp_min']}°C → {summary['temp_max']}°C\n"
        f"Feels     : {summary['feels_like_now']}°C\n"
        f"Rain      : {summary['rain_message']} ({summary['rain_chance']}%)\n"
        f"Wind      : {summary['max_wind_kph']} kph {summary['wind_dir']}\n"
        f"UV        : {summary['uv_index']} ({summary['uv_risk']})\n\n"
        f"Sunrise   : {summary['sunrise']}\n"
        f"Sunset    : {summary['sunset']}\n"
        f"Moon      : {summary['moon_phase']} ({summary['moon_illumination']}%)"
    )

    console.print(Panel(text, title="Weather Summary", border_style="cyan"))
