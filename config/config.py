import dataclasses as _dc
import json as _json
import typing as _t


class Config:
    """Contains all configuration models"""

    def __init__(self, file_path: str = "config/config.json"):
        self.data = self._load_data(file_path)

    def _load_data(self, file_path):
        with open(file_path, "r") as file:
            return _json.load(file)
