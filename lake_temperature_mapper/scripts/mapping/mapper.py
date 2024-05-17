from pathlib import Path

from config.config_reader import ConfigReader
from mapping.binary_runner import BinaryRunner
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

        # TODO: Reset the input file to defaults
        
        self._execute_orders(orders)

    def _read_orders(self) -> list[Order]:
        order_reader = OrderReader(
            self._config_reader.get_path("order_directory"),
            self._config_reader.get_path("range_path")
        )

        return order_reader.read_orders()

    def _execute_orders(self, orders: list[Order]) -> None:
        for order in orders:
            self._execute_order(order)

        self._defaults_writer.write_defaults()
        self._output_writer.finish()

    def _execute_order(self, order: Order) -> None:
        self._defaults_writer.write_defaults()
        sampler = Sampler(order.start, order.end, order.sample_count)
        self._output_writer.write_order_header(order)
        for sample_value in sampler.get_samples():
            self._output_writer.write_parameter_sample(
                order.parameter,
                sample_value
            )
            self._param_editor.modify_parameter(order.parameter, sample_value)
            self._binary_runner.run_binary()
            difference_map = self._difference_analyzer.compare_outputs()
            self._output_writer.write_difference_map(difference_map)
