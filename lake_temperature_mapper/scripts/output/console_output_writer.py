from output.output_writer import OutputWriter
from typing import Mapping

from mapping.order import Order
from mapping.output_difference import OutputDifference
from output.ansi_code import AnsiCode


class ConsoleOutputWriter(OutputWriter):
    def write_order_header(self, order: Order) -> None:
        name_line = f"Executing order: {order.name}"
        info_line = (
            f"{order.parameter}: {order.start} -> {order.end}"
            f", {order.sample_count} samples\n"
        )

        self._color_print(name_line, AnsiCode.BRIGHT_MAGENTA)
        self._color_print(info_line, AnsiCode.BRIGHT_MAGENTA)

    def write_parameter_sample(self, parameter_name: str, value: float) -> None:
        text = f"Set {parameter_name} to {value}"

        self._color_print(text, AnsiCode.BRIGHT_CYAN)

    def write_difference_map(
            self,
            difference_map: Mapping[str, list[OutputDifference]]
    ) -> None:
        empty_flag = True

        for key in difference_map.keys():
            if not difference_map[key]:
                continue

            empty_flag = False
            self._write_output_variable_header(key)
            for difference in difference_map[key]:
                self._write_difference(difference)

        if empty_flag:
            self._color_print("No differences", AnsiCode.BRIGHT_YELLOW)

        print("")

    def finish(self) -> None:
        # Could put a summary here later.
        pass

    def _write_output_variable_header(self, name: str):
        self._color_print(name, AnsiCode.BRIGHT_BLUE)

    def _write_difference(self, difference: OutputDifference):
        print(
            f"{difference.get_reference():<25} -> {difference.get_test():<25} "
            f"by {difference.get_difference():<25} at {difference.get_indices()}"
        )


    def _color_print(self, text: str, ansi_code: AnsiCode):
        print(f"\033[{ansi_code.value}m{text}\033[0m")
