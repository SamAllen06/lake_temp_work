import os
from typing import TextIO, Mapping


class RangeReader:
    RANGE_DELIMITER = " - "

    def __init__(self, file_path: os.PathLike):
        self.file_path = file_path
        self.ranges = self._read_ranges()

    def get_min(self, parameter: str) -> float:
        return self.ranges[parameter][0]

    def get_max(self, parameter: str) -> float:
        return self.ranges[parameter][1]

    def _read_ranges(self) -> Mapping[str, tuple[float, float]]:
        ranges = {}

        with open(self.file_path, "r") as file:
            lines = file.readlines()

        for parameter_index in range(len(lines) // 2):
            line_index = parameter_index * 2

            parameter_name = lines[line_index].strip()
            range_strings = lines[line_index + 1].split(self.RANGE_DELIMITER)

            min = float(range_strings[0])
            max = float(range_strings[1])

            ranges[parameter_name] = (min, max)

        return ranges
