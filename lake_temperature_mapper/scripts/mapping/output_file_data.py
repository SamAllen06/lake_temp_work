from pathlib import Path
from typing import Mapping

from mapping.output_difference import OutputDifference


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
            
            if not len(self._data[key]) == len(output_file_data._data[key]):
                return False

        return True

    def compare_to(self, test_file_data) -> Mapping[str, list[OutputDifference]]:
        output_differences = {}

        for parameter in self._data.keys():
            output_differences[parameter] = []
            for index, (ref_output, test_output) in enumerate(
                zip(self._data[parameter], test_file_data._data[parameter])
            ):
                output_difference = OutputDifference(
                    index,
                    ref_output,
                    test_output,
                )

                if not output_difference.is_nonzero_difference():
                    continue

                output_differences[parameter].append(output_difference)

        return output_differences

    def _read_data(self) -> Mapping[str, list[float]]:
        with open(self._file_path, "r") as file:
            lines = file.readlines()

        data = {}

        for line in lines:
            stripped_line = line.strip()
            if "%" in stripped_line:
                parameter_name = stripped_line
                data[parameter_name] = []
                continue

            data[parameter_name] += [
                float(value) for value in stripped_line.split()
            ]

        return data
