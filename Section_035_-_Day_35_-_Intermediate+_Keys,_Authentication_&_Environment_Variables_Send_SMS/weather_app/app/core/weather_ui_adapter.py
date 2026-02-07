def get_weather_ui_data(summary):
    # adapt analysis summary for GUI-friendly values
    return {
        "title": f"{summary['location']}, {summary['region']}",
        "date": summary["date"],
        "condition": summary["current_condition"],
        "vibe": summary["vibe"],

        "temp_range": f"{summary['temp_min']}°C – {summary['temp_max']}°C",
        "feels_like": f"{summary['feels_like_now']}°C",

        "comfort_text": (
            "Pleasant"
            if summary["comfortable_temp"]
            else "Hot"
            if summary["heat_stress"]
            else "Cold"
            if summary["cold_stress"]
            else "Mixed"
        ),

        "comfort_color": (
            "#4CAF50"
            if summary["comfortable_temp"]
            else "#F44336"
            if summary["heat_stress"]
            else "#2196F3"
            if summary["cold_stress"]
            else "#FFC107"
        ),

        "rain": f"{summary['rain_message']} ({summary['rain_chance']}%)",
        "wind": f"{summary['max_wind_kph']} kph {summary['wind_dir']}",
        "uv": f"{summary['uv_index']} ({summary['uv_risk']})",

        "outdoor": (
            "Good day to go out"
            if summary["good_outdoor_day"]
            else "Caution advised"
        ),

        "sun": f"🌅 {summary['sunrise']}   🌇 {summary['sunset']}",
        "moon": f"{summary['moon_phase']} ({summary['moon_illumination']}%)",
    }
