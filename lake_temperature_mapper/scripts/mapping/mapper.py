from pathlib import Path

from mapping.binary_runner import BinaryRunner
from mapping.config_reader import ConfigReader
from mapping.defaults_writer import DefaultsWriter
from mapping.difference_analyzer import DifferenceAnalyzer
from mapping.order import Order
from mapping.order_reader import OrderReader
from mapping.param_editor import ParamEditor
from mapping.sampler import Sampler
from output.output_writer import OutputWriter


class Mapper:
    def __init__(
            self,
            config_reader: ConfigReader,
            output_writer: OutputWriter
    ):
        self.config_reader = config_reader
        self.output_writer = output_writer
        self.defaults_writer = DefaultsWriter(
            self.config_reader.get_path("defaults_path"),
            self.config_reader.get_path("params_path")
        )
        self.param_editor = ParamEditor(
            self.config_reader.get_path("params_path")
        )
        self.binary_runner = BinaryRunner(
            self.config_reader.get_path("binary_path"),
            self.config_reader.get("binary_args")
        )
        self.difference_analyzer = DifferenceAnalyzer(
            self.config_reader.get_path("ref_output"),
            self.config_reader.get_path("test_output")
        )

    def map(self):
        orders = self._read_orders()

        # TODO: Reset the input file to defaults
        
        self._execute_orders(orders)

    def _read_orders(self) -> list[Order]:
        order_reader = OrderReader(
            self.config_reader.get_path("order_directory"),
            self.config_reader.get_path("range_path")
        )

        return order_reader.read_orders()

    def _execute_orders(self, orders: list[Order]) -> None:
        for order in orders:
            self._execute_order(order)

        self.defaults_writer.write_defaults()

    def _execute_order(self, order: Order) -> None:
        self.defaults_writer.write_defaults()
        sampler = Sampler(order.start, order.end, order.sample_count)
        self.output_writer.write_order_header(order)
        for sample_value in sampler.get_samples():
            self.output_writer.write_parameter_sample(
                order.parameter,
                sample_value
            )
            self.param_editor.modify_parameter(order.parameter, sample_value)
            self.binary_runner.run_binary()
            difference_map = self.difference_analyzer.compare_outputs()
            self.output_writer.write_difference_map(difference_map)
