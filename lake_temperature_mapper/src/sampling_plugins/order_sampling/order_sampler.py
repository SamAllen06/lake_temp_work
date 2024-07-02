from configparser import ConfigParser
import json
from pathlib import Path
from typing import Mapping

from root import APP_ROOT, SAMPLING_PLUGIN_CONFIG_DIRECTORY
from sampling.sampler import Sampler

from .bound_translator import BoundTranslator
from .order import Order
from .order_factory import OrderFactory
from .range_reader import RangeReader


CONFIG_FILE = SAMPLING_PLUGIN_CONFIG_DIRECTORY / "order_sampling.ini"


class OrderSampler(Sampler):
    def __init__(self):
        config_parser = ConfigParser()
        config_parser.read(CONFIG_FILE)
        bound_translator = BoundTranslator(
            RangeReader(APP_ROOT / config_parser["Paths"]["range_path"])
        )
        self._order_factory = OrderFactory(bound_translator)
        self._order_directory = APP_ROOT / config_parser["Paths"]["order_directory"]

    def get_sample_groups(self) -> Mapping[str, Order]:
        order_paths = list(self._order_directory.glob("*.json"))

        orders = {}

        for path in order_paths:
            order_name = path.name.removesuffix(".json")
            order_data = self._read_order_data(path)

            try:
                orders[order_name] = self._order_factory.construct_order(order_data)
            except KeyError:
                raise KeyError(f"Invalid order format in order {order_name}")

        return orders

    def _read_order_data(self, order_path: Path) -> Order:
        with open(order_path) as order_file:
            try:
                order_data = json.loads(order_file.read())
            except json.JSONDecodeError as error:
                raise RuntimeError(f"Invalid json in order {str(order_path)}", error)

        return order_data
