"""
Sheety persistence layer
Schema:
Date | Time | Exercise | Duration | Calories
"""

from typing import Dict, List
import requests


class WorkoutSheet:
    def __init__(self, base_url: str, bearer_token: str):
        self.endpoint = (
            f"{base_url}/myWorkouts(sayantan)/workouts"
        )
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }

    def add(self, workout: Dict) -> Dict:
        payload = {"workout": workout}
        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["workout"]

    def get_all(self) -> List[Dict]:
        response = requests.get(
            self.endpoint,
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["workouts"]
