import json
from pathlib import Path
from typing import Mapping

from config import ConfigReader
from sample_generation.order_sampler.bound_translator import BoundTranslator
from sample_generation.order_sampler.config import FILE_PATH
from sample_generation.order_sampler.order import Order
from sample_generation.order_sampler.order_factory import OrderFactory
from sample_generation.order_sampler.range_reader import RangeReader
from sample_generation.sampler import Sampler


class OrderSampler(Sampler):
    def __init__(self):
        config_reader = ConfigReader(FILE_PATH)
        bound_translator = BoundTranslator(
            RangeReader(config_reader.get_path("range_path"))
        )
        self._order_factory = OrderFactory(bound_translator)
        self._order_directory = config_reader.get_path("order_directory")

    def get_sample_groups(self) -> Mapping[str, Order]:
        order_paths = list(self._order_directory.glob("*.json"))

        orders = {}

        for path in order_paths:
            order_name = path.name.removesuffix(".json")
            order_data = self._read_order_data(path)

            try:
                orders[order_name] = self._order_factory.construct_order(
                    order_data
                )
            except KeyError:
                raise KeyError(f"Invalid order format in order {order_name}")

        return orders

    def _read_order_data(self, order_path: Path) -> Order:
        with open(order_path) as order_file:
            try:
                order_data = json.loads(order_file.read())
            except json.JSONDecodeError as error:
                raise RuntimeError(
                    f"Invalid json in order {str(order_path)}", error
                )

        return order_data
