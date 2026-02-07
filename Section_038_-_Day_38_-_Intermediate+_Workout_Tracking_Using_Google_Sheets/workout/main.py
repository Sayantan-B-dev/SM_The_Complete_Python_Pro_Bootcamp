import os
from dotenv import load_dotenv

from engine import NutritionEngine
from sheet import WorkoutSheet
from ui import TerminalUI


def main():
    load_dotenv()
    ui = TerminalUI()

    try:
        sheet = WorkoutSheet(
            os.getenv("SHEETY_BASE_URL"),
            os.getenv("SHEETY_BEARER_TOKEN"),
        )

        engine = NutritionEngine(
            os.getenv("NUTRITION_APP_ID"),
            os.getenv("NUTRITION_API_KEY"),
            sheet,
        )

        ui.info("Checking API health...")
        engine.health_check()
        ui.success("API online")

        user_data = ui.get_user_input()

        ui.info("Calculating workout...")
        results = engine.calculate_exercise(**user_data)
        ui.render_results(results)

        for r in results:
            ui.info(f"Saving {r.exercise} to sheet...")
            engine.log_to_sheet(r)
            ui.success("Saved")

    except Exception as e:
        ui.error(str(e))


if __name__ == "__main__":
    main()
