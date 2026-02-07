"""
Business logic:
- Nutrition API
- Sheet logging
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import requests

from sheet import WorkoutSheet


API_BASE_URL = "https://app.100daysofpython.dev"
EXERCISE_ENDPOINT = f"{API_BASE_URL}/v1/nutrition/natural/exercise"
HEALTH_ENDPOINT = f"{API_BASE_URL}/healthz"


@dataclass
class ExerciseResult:
    exercise: str
    duration: int
    calories: float


class NutritionEngine:
    def __init__(self, app_id: str, api_key: str, sheet: WorkoutSheet):
        self.sheet = sheet
        self.headers = {
            "Content-Type": "application/json",
            "x-app-id": app_id,
            "x-app-key": api_key,
        }

    def health_check(self) -> None:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        response.raise_for_status()

    def calculate_exercise(
        self,
        query: str,
        weight_kg: Optional[int] = None,
        height_cm: Optional[int] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
    ) -> List[ExerciseResult]:

        payload = {"query": query}
        if weight_kg:
            payload["weight_kg"] = weight_kg
        if height_cm:
            payload["height_cm"] = height_cm
        if age:
            payload["age"] = age
        if gender:
            payload["gender"] = gender

        response = requests.post(
            EXERCISE_ENDPOINT,
            headers=self.headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

        results = []
        for item in response.json()["exercises"]:
            results.append(
                ExerciseResult(
                    exercise=item["name"].title(),
                    duration=item["duration_min"],
                    calories=item["nf_calories"],
                )
            )

        return results

    def log_to_sheet(self, result: ExerciseResult) -> dict:
        now = datetime.now()

        workout_row = {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S"),
            "exercise": result.exercise,
            "duration": result.duration,
            "calories": round(result.calories),
        }

        return self.sheet.add(workout_row)
