from pathlib import Path

from mapping.binary_runner import BinaryRunner
from mapping.config_reader import ConfigReader
from mapping.difference_analyzer import DifferenceAnalyzer
from mapping.order import Order
from mapping.order_reader import OrderReader
from mapping.param_editor import ParamEditor
from mapping.sampler import Sampler


class Mapper:
    def __init__(self, config_path: Path):
        self.config_reader = ConfigReader(config_path)
        self.param_editor = ParamEditor(
            self.config_reader.get_path_of("params_path")
        )
        self.binary_runner = BinaryRunner(
            self.config_reader.get_path_of("binary_path")
        )
        self.difference_analyzer = DifferenceAnalyzer(
            self.config_reader.get_path_of("ref_output"),
            self.config_reader.get_path_of("test_output")
        )

    def map(self):
        orders = self._read_orders()

        # TODO: Reset the input file to defaults
        
        self._execute_orders(orders)

    def _read_orders(self) -> list[Order]:
        order_reader = OrderReader(
            self.config_reader.get_path_of("order_directory"),
            self.config_reader.get_path_of("range_path")
        )

        return order_reader.read_orders()

    def _execute_orders(self, orders: list[Order]) -> None:
        for order in orders:
            self._execute_order(order)

    def _execute_order(self, order: Order) -> None:
        sampler = Sampler(order.start, order.end, order.sample_count)
        for sample_value in sampler.get_samples():
            self.param_editor.modify_parameter(order.parameter, sample_value)
            self.binary_runner.run()
            diffs = self.difference_analyzer.compare_outputs()
            print(diffs)








