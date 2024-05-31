from pathlib import Path
from typing import Mapping

class ParamEditor:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def modify_parameters(self, value_map: Mapping[str, float]) -> None:
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        found_map = {parameter: False for parameter in value_map.keys()}

        for index, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line in value_map:
                lines[index + 1] = str(value_map[stripped_line]) + "\n"
                found_map[stripped_line] = True

        for parameter in found_map.keys():
            if not found_map[parameter]:
                raise KeyError(
                    f"Could not find parameter \"{parameter}\" "
                    f"in {self.file_path}."
                )

        with open(self.file_path, "w") as file:
            file.writelines(lines)
