from pathlib import Path
from typing import Mapping

from config.config_reader import ConfigReader
from testing.binary_runner import BinaryRunner
from testing.defaults_writer import DefaultsWriter
from analysis.difference_analyzer import DifferenceAnalyzer
from sample_generation.order import Order
from sample_generation.order_reader import OrderReader
from testing.param_editor import ParamEditor
from output.output_writer import OutputWriter


class Mapper:
    def __init__(
            self,
            config_reader: ConfigReader,
            output_writer: OutputWriter
    ):
        self._config_reader = config_reader
        self._output_writer = output_writer
        self._defaults_writer = DefaultsWriter(
            self._config_reader.get_path("defaults_path"),
            self._config_reader.get_path("params_path")
        )
        self._param_editor = ParamEditor(
            self._config_reader.get_path("params_path")
        )
        self._binary_runner = BinaryRunner(
            self._config_reader.get_path("binary_path"),
            self._config_reader.get("binary_args")
        )
        self._difference_analyzer = DifferenceAnalyzer(
            self._config_reader.get_path("ref_output"),
            self._config_reader.get_path("test_output")
        )

    def map(self):
        orders = self._read_orders()
        self._execute_orders(orders)

    def _read_orders(self) -> Mapping[str, Order]:
        order_reader = OrderReader(
            self._config_reader.get_path("order_directory"),
            self._config_reader.get_path("range_path")
        )

        return order_reader.read_orders()

    def _execute_orders(self, orders: Mapping[str, Order]) -> None:
        for order_name in orders.keys():
            order = orders[order_name]
            self._output_writer.write_order_header(order_name, order)
            self._execute_order(order)

        self._defaults_writer.write_defaults()
        self._output_writer.finish()

    def _execute_order(self, order: Order) -> None:
        self._defaults_writer.write_defaults()
        for sample in order:
            self._output_writer.write_sample(
                sample
            )
            self._param_editor.modify_parameters(sample)

            exit_code = self._binary_runner.run_binary()
            if exit_code:
                self._output_writer.write_binary_exit(exit_code)
                continue

            difference_map = self._difference_analyzer.compare_outputs()
            self._output_writer.write_difference_map(difference_map)
