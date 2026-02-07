def analyze_weather(weather_data):
    location = weather_data["location"]["name"]
    region = weather_data["location"]["region"]
    country = weather_data["location"]["country"]

    current = weather_data["current"]
    forecast_day = weather_data["forecast"]["forecastday"][0]

    day = forecast_day["day"]
    astro = forecast_day["astro"]

    # -----------------------------
    # TEMPERATURE COMFORT LOGIC
    # -----------------------------
    comfortable_temp = 18 <= day["avgtemp_c"] <= 28
    heat_stress = day["maxtemp_c"] >= 32
    cold_stress = day["mintemp_c"] <= 10

    # -----------------------------
    # OUTDOOR USABILITY
    # -----------------------------
    good_outdoor_day = (
        not day["daily_will_it_rain"]
        and day["maxwind_kph"] < 25
        and day["avgvis_km"] >= 8
    )

    # -----------------------------
    # RAIN MESSAGE
    # -----------------------------
    rain_message = (
        "No rain expected"
        if day["daily_chance_of_rain"] == 0
        else "Slight chance of rain"
        if day["daily_chance_of_rain"] < 30
        else "Rain likely"
    )

    # -----------------------------
    # VISIBILITY MESSAGE
    # -----------------------------
    visibility_message = (
        "Fog / mist possible"
        if current["vis_km"] < 5
        else "Clear visibility"
    )

    # -----------------------------
    # WEATHER VIBE
    # -----------------------------
    vibe = (
        "Bright & cheerful"
        if day["condition"]["code"] == 1000
        else "Calm & muted"
        if "Mist" in current["condition"]["text"]
        else "Unsettled"
    )

    # -----------------------------
    # FINAL SUMMARY OBJECT
    # -----------------------------
    return {
        # Location
        "location": location,
        "region": region,
        "country": country,
        "date": forecast_day["date"],

        # Conditions
        "condition": day["condition"]["text"],
        "current_condition": current["condition"]["text"],
        "vibe": vibe,

        # Rain
        "will_rain": bool(day["daily_will_it_rain"]),
        "rain_chance": day["daily_chance_of_rain"],
        "rain_message": rain_message,

        # Temperature
        "temp_min": day["mintemp_c"],
        "temp_max": day["maxtemp_c"],
        "temp_avg": day["avgtemp_c"],
        "feels_like_now": current["feelslike_c"],

        # Comfort flags
        "comfortable_temp": comfortable_temp,
        "heat_stress": heat_stress,
        "cold_stress": cold_stress,

        # Wind & visibility
        "max_wind_kph": day["maxwind_kph"],
        "wind_dir": current["wind_dir"],
        "visibility_km": day["avgvis_km"],
        "visibility_message": visibility_message,

        # UV
        "uv_index": day["uv"],
        "uv_risk": (
            "High" if day["uv"] >= 6
            else "Moderate" if day["uv"] >= 3
            else "Low"
        ),

        # Outdoor
        "good_outdoor_day": good_outdoor_day,

        # Astronomy
        "sunrise": astro["sunrise"],
        "sunset": astro["sunset"],
        "moon_phase": astro["moon_phase"],
        "moon_illumination": astro["moon_illumination"],
    }
