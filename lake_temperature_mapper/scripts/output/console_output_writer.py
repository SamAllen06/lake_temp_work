from output.output_writer import OutputWriter
from typing import Mapping

from mapping.order import Order
from mapping.output_difference import OutputDifference
from output.ansi_code import AnsiCode


class ConsoleOutputWriter(OutputWriter):
    def write_order_header(self, order: Order) -> None:
        name_line = f"Executing order: {order.name}\n"
        samples_line = f"{order.sample_count} linear samples using ranges:\n"
        info_lines = []

        for parameter in order.ranges.keys():
            parameter_range = order.ranges[parameter]
            info_lines.append(
                f"{parameter}: {parameter_range.start} -> {parameter_range.end}"
            )

        text = name_line + samples_line + "\n".join(info_lines) + "\n"

        self._ansi_print(text, AnsiCode.BRIGHT_MAGENTA)

    def write_sample(self, sample: Mapping[str, float]) -> None:
        lines = []

        for parameter in sample:
            lines.append(f"Set {parameter} to {sample[parameter]}")

        text = "\n".join(lines)

        self._ansi_print(text, AnsiCode.BRIGHT_CYAN)

    def write_binary_exit(self, exit_code: int) -> None:
        text = f"Binary exited with code {exit_code}\n"

        self._ansi_print(text, AnsiCode.BRIGHT_RED)

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
            self._write_difference_header()
            for difference in difference_map[key]:
                self._write_difference(difference)

        if empty_flag:
            self._ansi_print("No differences", AnsiCode.BRIGHT_YELLOW)

        print("")

    def finish(self) -> None:
        # Could put a summary here later.
        pass

    def _write_output_variable_header(self, name: str):
        self._ansi_print(name, AnsiCode.BRIGHT_BLUE)

    def _write_difference(self, difference: OutputDifference):
        print(
            f"{difference.get_reference():<25} -> {difference.get_test():<25} "
            f"by {difference.get_difference():<25} at {difference.get_indices()}"
        )

    def _write_difference_header(self):
        self._ansi_print(
            (
                f"{'reference_value':<25} -> {'test_value':<25} "
                f"by {'difference':<25} at indecies"
            ),
            AnsiCode.UNDERLINE
        )

    def _ansi_print(self, text: str, ansi_code: AnsiCode):
        print(f"\033[{ansi_code.value}m{text}\033[0m")
