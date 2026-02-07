from app.utils.config import Config
from app.services.pixela_client import PixelaClient
from app.core.habit_manager import HabitManager
from app.ui.app_window import AppWindow


def main():
    config = Config()

    client = PixelaClient(
        username=config.pixela_username,
        token=config.pixela_token,
        base_url=config.pixela_base_url,
    )

    manager = HabitManager(client, config.pixela_graph_id)
    manager.setup_user_and_graph()

    AppWindow(manager).run()


if __name__ == "__main__":
    main()
