from pathlib import Path
from typing import Mapping

import numpy as np
import numpy.typing as npt

from analysis.output_difference import OutputDifference


class OutputFileData:
    def __init__(self, file_path: Path):
        self._file_path = file_path
        self._data = self._read_data()

    def is_same_format_as(self, output_file_data) -> bool:
        if not len(self._data.keys()) == len(output_file_data._data.keys()):
            return False

        for key in self._data.keys():
            if not key in output_file_data._data:
                return False
            
            if not self._data[key].shape == output_file_data._data[key].shape:
                return False

        return True

    def compare_to(self, test_file_data) -> dict[str, list[OutputDifference]]:
        output_differences: dict[str, list[OutputDifference]] = {}

        for parameter in self._data.keys():
            output_differences[parameter] = []
            for indecies in np.ndindex(self._data[parameter].shape):
                output_difference = OutputDifference(
                    indecies,
                    self._data[parameter][indecies],
                    test_file_data._data[parameter][indecies]
                )

                if not output_difference.is_nonzero_difference():
                    continue

                output_differences[parameter].append(output_difference)

        return output_differences

    def _read_data(self) -> dict[str, npt.NDArray[np.float64]]:
        with open(self._file_path, "r") as file:
            lines = file.readlines()

        data: dict[str, list[npt.NDArray[np.float64]]] = {}

        for line in lines:
            stripped_line = line.strip()
            if "%" in stripped_line:
                parameter_name = stripped_line
                data[parameter_name] = []
                continue

            data[parameter_name].append(np.fromstring(line, sep=" "))

        combined_data: dict[str, npt.NDArray[np.float64]] = {}
        for parameter in data.keys():
            combined_data[parameter] = np.concatenate(data[parameter])

        return combined_data
