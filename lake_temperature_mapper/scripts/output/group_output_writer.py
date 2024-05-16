from typing import Mapping

from mapping.order import Order
from mapping.output_difference import OutputDifference
from output.output_writer import OutputWriter


class GroupOutputWriter(OutputWriter):
    def __init__(self):
        self._writers = []

    def add_writer(self, writer: OutputWriter) -> None:
        self._writers.append(writer)

    def write_order_header(self, order: Order) -> None:
        for writer in self._writers:
            writer.write_order_header(order)

    def write_parameter_sample(self, parameter_name: str, value: float) -> None:
        for writer in self._writers:
            writer.write_parameter_sample(parameter_name, value)

    def write_difference_map(
            self,
            difference_map: Mapping[str, OutputDifference]
    ) -> None:
        for writer in self._writers:
            writer.write_difference_map(difference_map)

    def finish(self) -> None:
        for writer in self._writers:
            writer.finish()
