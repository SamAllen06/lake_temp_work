from pathlib import Path
from collections.abc import Mapping

from util import Table, TransparentLayerList


class OutputFileReader:
    def __init__(self, reference_file_path: Path, test_file_path: Path):
        self._reference_data = self._read_data(reference_file_path)
        self._test_file_path = test_file_path
        self._current_group_data = self._generate_empty_group_data()

    def get_reference_data(self) -> dict[str, list[float]]:
        return self._reference_data

    def read_sample_data(self) -> dict[str, list[float]]:
        sample_data = self._read_data(self._test_file_path)
        current_group_data_sequence = self._current_group_data.as_sequence()
        current_group_data_sequence.append(sample_data)
        return sample_data

    def read_group_data(self) -> Table[dict, TransparentLayerList]:
        group_data = self._current_group_data
        self._current_group_data = self._generate_empty_group_data()
        return group_data

    def group_data_exists(self) -> bool:
        return self._current_group_data.get_row_count() > 1

    def _generate_empty_group_data(self) -> Table[dict, TransparentLayerList]:
        data: Table[dict, TransparentLayerList] = Table({}, TransparentLayerList())
        data_sequence = data.as_sequence()
        data_sequence.initialize_keys(self._reference_data.keys())
        data_sequence.append(self._reference_data)
        return data

    def _read_data(self, file_path: Path) -> dict[str, list[float]]:
        with open(file_path, "r") as file:
            lines = file.readlines()

        data: dict[str, list[float]] = {}

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
