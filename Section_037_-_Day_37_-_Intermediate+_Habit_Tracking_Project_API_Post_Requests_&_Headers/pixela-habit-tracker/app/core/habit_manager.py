from datetime import datetime
from app.utils.exceptions import PixelaAPIError


class HabitManager:
    def __init__(self, client, graph_id: str):
        self.client = client
        self.graph_id = graph_id

    def _today(self) -> str:
        return datetime.now().strftime("%Y%m%d")

    def setup_user_and_graph(self):
        try:
            self.client.create_user()
        except PixelaAPIError:
            pass

        try:
            self.client.create_graph(
                graph_id=self.graph_id,
                name="Daily Habit",
                unit="count",
                graph_type="int",
                color="shibafu",
            )
        except PixelaAPIError:
            pass

    def add_habit(self, quantity: str):
        self.client.add_pixel(self.graph_id, self._today(), quantity)

    def update_habit(self, quantity: str):
        self.client.update_pixel(self.graph_id, self._today(), quantity)

    def delete_habit(self):
        self.client.delete_pixel(self.graph_id, self._today())

    