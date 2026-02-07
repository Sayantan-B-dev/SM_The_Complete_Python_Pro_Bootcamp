import requests
from typing import Any

from app.utils.exceptions import PixelaAPIError, NetworkError


class PixelaClient:
    def __init__(self, username: str, token: str, base_url: str):
        self.username = username
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-USER-TOKEN": token,
            "Content-Type": "application/json",
        }

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        if not response.ok:
            raise PixelaAPIError(
                f"HTTP {response.status_code}: {response.text}",
                response.status_code,
            )

        try:
            data = response.json()
            if not data.get("isSuccess", True):
                raise PixelaAPIError(
                    data.get("message", "Pixela API error"),
                    response.status_code,
                )
            return data
        except ValueError:
            return {
                "isSuccess": True,
                "raw": response.text.strip(),
            }

    def create_user(self) -> dict[str, Any]:
        payload = {
            "token": self.headers["X-USER-TOKEN"],
            "username": self.username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }

        try:
            response = requests.post(
                f"{self.base_url}/users",
                json=payload,
                timeout=10,
            )
        except requests.RequestException as exc:
            raise NetworkError(str(exc))

        return self._handle_response(response)

    def create_graph(self, graph_id: str, name: str, unit: str, graph_type: str, color: str):
        payload = {
            "id": graph_id,
            "name": name,
            "unit": unit,
            "type": graph_type,
            "color": color,
        }

        url = f"{self.base_url}/users/{self.username}/graphs"

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
        except requests.RequestException as exc:
            raise NetworkError(str(exc))

        return self._handle_response(response)

    def add_pixel(self, graph_id: str, date: str, quantity: str):
        payload = {"date": date, "quantity": quantity}
        url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}"

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
        except requests.RequestException as exc:
            raise NetworkError(str(exc))

        return self._handle_response(response)

    def update_pixel(self, graph_id: str, date: str, quantity: str):
        payload = {"quantity": quantity}
        url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}/{date}"

        try:
            response = requests.put(url, headers=self.headers, json=payload, timeout=10)
        except requests.RequestException as exc:
            raise NetworkError(str(exc))

        return self._handle_response(response)

    def delete_pixel(self, graph_id: str, date: str):
        url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}/{date}"

        try:
            response = requests.delete(url, headers=self.headers, timeout=10)
        except requests.RequestException as exc:
            raise NetworkError(str(exc))

        return self._handle_response(response)
    