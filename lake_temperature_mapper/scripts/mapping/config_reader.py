from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


class ConfigReader:
    def __init__(self, config_path: Path):
        self._config_path = config_path
        self._config_map = self._read_config()
    
    def config_exists(self):
        return self._config_path.exists() and self._config_path.is_file()

    def get_path_of(self, key: str) -> Path:
        return PROJECT_ROOT / self._config_map[key]

    def _read_config(self):
        if not self.config_exists():
            return {}
        
        with open(self._config_path, "r") as config_file:
            lines = config_file.readlines()

        selections = {}

        for line in lines:
            split_line = line.strip().split(": ")
            selections[split_line[0]] = Path(split_line[1])

        return selections



