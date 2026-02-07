import tkinter as tk
from app.services.weather_api import get_weather_data
from app.core.weather_analysis import analyze_weather
from app.core.weather_ui_adapter import get_weather_ui_data


def main():
    root = tk.Tk()
    root.title("Weather App")
    root.geometry("400x450")

    weather_data = get_weather_data("Kolkata")
    summary = analyze_weather(weather_data)
    ui = get_weather_ui_data(summary)

    tk.Label(root, text=ui["title"], font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(root, text=ui["date"]).pack()

    tk.Label(root, text=ui["condition"], font=("Arial", 12)).pack(pady=5)
    tk.Label(root, text=ui["temp_range"], font=("Arial", 14)).pack(pady=5)
    tk.Label(root, text=f"Feels like {ui['feels_like']}").pack()

    tk.Label(
        root,
        text=ui["comfort_text"],
        fg=ui["comfort_color"],
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    tk.Label(root, text=f"Rain: {ui['rain']}").pack()
    tk.Label(root, text=f"Wind: {ui['wind']}").pack()
    tk.Label(root, text=f"UV: {ui['uv']}").pack()

    tk.Label(root, text=ui["outdoor"], font=("Arial", 11, "italic")).pack(pady=10)
    tk.Label(root, text=ui["sun"]).pack()
    tk.Label(root, text=ui["moon"]).pack()

    root.mainloop()


if __name__ == "__main__":
    main()
