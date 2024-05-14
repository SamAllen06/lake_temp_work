from pathlib import Path

from mapping.binary_runner import BinaryRunner
from mapping.config_reader import ConfigReader
from mapping.defaults_writer import DefaultsWriter
from mapping.difference_analyzer import DifferenceAnalyzer
from mapping.order import Order
from mapping.order_reader import OrderReader
from mapping.param_editor import ParamEditor
from mapping.sampler import Sampler


class Mapper:
    def __init__(self, config_path: Path):
        self.config_reader = ConfigReader(config_path)
        self.defaults_writer = DefaultsWriter(
            self.config_reader.get("defaults_path"),
            self.config_reader.get("params_path")
        )
        self.param_editor = ParamEditor(
            self.config_reader.get("params_path")
        )
        self.binary_runner = BinaryRunner(
            self.config_reader.get("binary_path")
        )
        self.difference_analyzer = DifferenceAnalyzer(
            self.config_reader.get("ref_output"),
            self.config_reader.get("test_output")
        )

    def map(self):
        orders = self._read_orders()

        # TODO: Reset the input file to defaults
        
        self._execute_orders(orders)

    def _read_orders(self) -> list[Order]:
        order_reader = OrderReader(
            self.config_reader.get("order_directory"),
            self.config_reader.get("range_path")
        )

        return order_reader.read_orders()

    def _execute_orders(self, orders: list[Order]) -> None:
        for order in orders:
            self._execute_order(order)

        self.defaults_writer.write_defaults()

    def _execute_order(self, order: Order) -> None:
        self.defaults_writer.write_defaults()
        sampler = Sampler(order.start, order.end, order.sample_count)
        self._print_order_header(order)
        for sample_value in sampler.get_samples():
            self._print_input_sample(order.parameter, sample_value)
            self.param_editor.modify_parameter(order.parameter, sample_value)
            self.binary_runner.run_binary()
            diffs = self.difference_analyzer.compare_outputs()
            self._print_diffs(diffs)

    def _print_order_header(self, order: Order) -> None:
        print("\033[95m" + f"Executing order: {order.name}")
        print(
            f"{order.parameter}: {order.start} -> {order.end}, "
            f"{order.sample_count} samples" + "\033[0m\n"
        )

    def _print_input_sample(self, parameter: str, value: float) -> None:
        print("\033[96m" + f"{parameter}:{str(value)}" + "\033[0m")

    def _print_diffs(self, diffs) -> None:
        for key in diffs.keys():
            print("\033[94m" + key + "\033[0m")
            for difference in diffs[key]:
                print(str(difference))
        print("")








