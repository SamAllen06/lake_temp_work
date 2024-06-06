import csv
from pathlib import Path
from typing import Mapping

from sample_generation import SampleGroup
from analysis.output_difference import OutputDifference
from output.output_writer import OutputWriter


class CSVOutputWriter(OutputWriter):
    FILENAME_FORMAT = "{sample_group_name}.csv"

    def __init__(self, output_directory: Path):
        self._output_directory = output_directory
        self._sample_group_data: list[tuple] = []
        self._sample_group_name = ""

    def write_sample_group_header(
            self, sample_group_name: str, sample_group: SampleGroup
    ) -> None:
        if self._sample_group_name:
            self._write_sample_group_to_file()

        self._sample_group_data = []
        self._sample_group_name = sample_group_name

    def write_sample(self, value_map: Mapping[str, float]) -> None:
        for parameter in value_map.keys():
            self._sample_group_data.append((parameter, value_map[parameter]))

    def write_binary_exit(self, exit_code: int) -> None:
        self._sample_group_data.append(("EXIT", exit_code))

    def write_difference_map(
            self,
            difference_map: Mapping[str, list[OutputDifference]]
    ) -> None:
        for output_name in difference_map.keys():
            if not difference_map[output_name]:
                continue

            self._sample_group_data.append((output_name,))
            for difference in difference_map[output_name]:
                self._sample_group_data.append((
                    difference.get_reference(),
                    difference.get_test(),
                    difference.get_difference(),
                    difference.get_indices(),
                ))

    def finish(self) -> None:
        if self._sample_group_name:
            self._write_sample_group_to_file()

    def _write_sample_group_to_file(self):
        filename = self.FILENAME_FORMAT.format(
            sample_group_name=self._sample_group_name
        )
        filepath = self._output_directory / filename

        with open(filepath, "w", newline="") as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerows(self._sample_group_data)


