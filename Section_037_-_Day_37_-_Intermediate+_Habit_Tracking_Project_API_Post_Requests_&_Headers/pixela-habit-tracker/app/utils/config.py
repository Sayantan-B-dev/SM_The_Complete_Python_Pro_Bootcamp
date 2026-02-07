import os
from dotenv import load_dotenv
from app.utils.exceptions import ConfigurationError


class Config:
    def __init__(self):
        load_dotenv()
        self.pixela_username = self._get("PIXELA_USERNAME")
        self.pixela_token = self._get("PIXELA_TOKEN")
        self.pixela_graph_id = self._get("PIXELA_GRAPH_ID")
        self.pixela_base_url = self._get("PIXELA_BASE_URL", "https://pixe.la/v1")

    def _get(self, key, default=None):
        val = os.getenv(key, default)
        if not val:
            raise ConfigurationError(f"Missing {key}")
        return val
