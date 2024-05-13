from pathlib import Path

# /.../lake_temperature_mapper/ if in the repository,
# /app/ if in the docker image.
PROJECT_ROOT = Path(__file__).parent.parent.parent


class ConfigReader:
    def __init__(self, config_path: Path):
        self._config_path = config_path
        self._config_map = self._read_config()
    
    def get(self, config_key: str) -> Path:
        return PROJECT_ROOT / self._config_map[config_key]

    def _read_config(self):
        with open(self._config_path, "r") as config_file:
            lines = config_file.readlines()

        selections = {}

        for line in lines:
            split_line = line.strip().split(": ")
            config_key = split_line[0]
            config_value = split_line[1]
            selections[config_key] = Path(config_value)

        return selections
