from pathlib import Path
from typing import Mapping


class DefaultsWriter:
    def __init__(self, defaults_path: Path, param_path: Path):
        self._defaults = self._read_defaults(defaults_path)
        self._param_path = param_path

    def write_defaults(self) -> None:
        lines = []

        for key in self._defaults:
            lines.append(key + "\n")
            value = self._defaults[key]
            lines.append(str(value) + "\n")

        with open(self._param_path, "w") as param_file:
            param_file.writelines(lines)

    def _read_defaults(self, defaults_path: Path) -> Mapping[str, float]:
        defaults = {}

        with open(defaults_path, "r") as defaults_file:
            lines = defaults_file.readlines()

        keys = [lines[index].strip() for index in range(0, len(lines), 2)]
        values = [float(lines[index]) for index in range(1, len(lines), 2)]

        for key, value in zip(keys, values):
            defaults[key] = value

        return defaults

