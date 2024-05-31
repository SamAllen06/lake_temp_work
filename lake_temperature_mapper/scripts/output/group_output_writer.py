from typing import Mapping

from sample_generation.order import Order
from analysis.output_difference import OutputDifference
from output.output_writer import OutputWriter


class GroupOutputWriter(OutputWriter):
    def __init__(self):
        self._writers = []

    def add_writer(self, writer: OutputWriter) -> None:
        self._writers.append(writer)

    def write_order_header(self, order_name: str, order: Order) -> None:
        for writer in self._writers:
            writer.write_order_header(order_name, order)

    def write_sample(self, value_map: Mapping[str, float]) -> None:
        for writer in self._writers:
            writer.write_sample(value_map)

    def write_binary_exit(self, exit_code: int) -> None:
        for writer in self._writers:
            writer.write_binary_exit(exit_code)

    def write_difference_map(
            self,
            difference_map: Mapping[str, OutputDifference]
    ) -> None:
        for writer in self._writers:
            writer.write_difference_map(difference_map)

    def finish(self) -> None:
        for writer in self._writers:
            writer.finish()
