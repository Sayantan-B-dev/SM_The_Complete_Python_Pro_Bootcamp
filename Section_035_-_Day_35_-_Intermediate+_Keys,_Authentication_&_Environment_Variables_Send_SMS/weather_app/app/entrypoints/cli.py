from app.services.weather_api import get_weather_data
from app.core.weather_analysis import analyze_weather
from app.presentation.weather_cli import print_weather_summary


def main():
    weather_data = get_weather_data("Kolkata")
    summary = analyze_weather(weather_data)
    print_weather_summary(summary)


if __name__ == "__main__":
    main()
