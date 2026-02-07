"""
Terminal UI
Easily replaceable with Tkinter
"""

from typing import List
from engine import ExerciseResult


class TerminalUI:
    def info(self, msg: str):
        print(f"\nℹ {msg}")

    def success(self, msg: str):
        print(f"✅ {msg}")

    def error(self, msg: str):
        print(f"\n❌ {msg}")

    def get_user_input(self) -> dict:
        print("\n" + "═" * 70)
        print("🏃 Workout Logger")
        print("═" * 70)

        return {
            "query": input("Exercise description: ").strip(),
            "weight_kg": self._opt_int("Weight (kg)"),
            "height_cm": self._opt_int("Height (cm)"),
            "age": self._opt_int("Age"),
            "gender": input("Gender (optional): ").strip() or None,
        }

    def render_results(self, results: List[ExerciseResult]):
        print("\n" + "─" * 70)
        for r in results:
            print(
                f"Exercise : {r.exercise}\n"
                f"Duration : {r.duration} min\n"
                f"Calories : {round(r.calories)} kcal"
            )
            print("─" * 70)

    def _opt_int(self, label: str):
        value = input(f"{label} (optional): ").strip()
        return int(value) if value else None
