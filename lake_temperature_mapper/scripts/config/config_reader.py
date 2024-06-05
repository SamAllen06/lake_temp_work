import importlib
from pathlib import Path

from config.root import APP_ROOT


class ConfigReader:
    def __init__(self, config_path: Path):
        self._config_path = config_path
        self._config_map = self._read_config()
    
    def get_class(self, config_key: str) -> type:
        split_line = self.get(config_key).split(":")

        module = importlib.import_module(split_line[0])
        return getattr(module, split_line[1])

    def get_path(self, config_key: str) -> Path:
        return APP_ROOT / self.get(config_key)

    def get(self, config_key: str) -> str:
        return self._config_map[config_key]

    def _read_config(self):
        with open(self._config_path, "r") as config_file:
            lines = config_file.readlines()

        selections = {}

        for line in lines:
            split_line = line.strip("\n").split(": ")
            config_key = split_line[0]
            config_value = split_line[1]
            selections[config_key] = config_value

        return selections
