import csv
from pathlib import Path
from typing import Mapping

from mapping.order import Order
from mapping.output_difference import OutputDifference
from output.output_writer import OutputWriter


class CSVOutputWriter(OutputWriter):
    FILENAME_FORMAT = "{order_name}.csv"

    def __init__(self, output_directory: Path):
        self._output_directory = output_directory
        self._order_data = []
        self._order_name = ""

    def write_order_header(self, order_name: str, order: Order) -> None:
        if self._order_name:
            self._write_order_to_file()

        self._order_data = []
        self._order_name = order_name

    def write_sample(self, value_map: Mapping[str, float]) -> None:
        for parameter in value_map.keys():
            self._order_data.append((parameter, value_map[parameter]))

    def write_binary_exit(self, exit_code: int) -> None:
        self._order_data.append(("EXIT", exit_code))

    def write_difference_map(
            self,
            difference_map: Mapping[str, OutputDifference]
    ) -> None:
        for output_name in difference_map.keys():
            if not difference_map[output_name]:
                continue

            self._order_data.append([output_name])
            for difference in difference_map[output_name]:
                self._order_data.append((
                    difference.get_reference(),
                    difference.get_test(),
                    difference.get_difference(),
                    difference.get_indices(),
                ))

    def finish(self) -> None:
        if self._order_name:
            self._write_order_to_file()

    def _write_order_to_file(self):
        filename = self.FILENAME_FORMAT.format(order_name=self._order_name)
        filepath = self._output_directory / filename

        with open(filepath, "w", newline="") as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerows(self._order_data)


