import json
from pathlib import Path
from typing import Mapping

from mapping.bound_translator import BoundTranslator
from mapping.order import Order
from mapping.order_factory import OrderFactory
from mapping.range_reader import RangeReader


class OrderReader:
    def __init__(self, order_directory: Path, range_path: Path):
        bound_translator = BoundTranslator(RangeReader(range_path))
        self._order_factory = OrderFactory(bound_translator)
        self._order_directory = order_directory

    def read_orders(self) -> Mapping[str, Order]:
        order_paths = list(self._order_directory.glob("*.json"))

        orders = {}

        for path in order_paths:
            order_name = path.name.removesuffix(".json")
            order_data = self._read_order_data(path)

            orders[order_name] = self._order_factory.construct_order(order_data)

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
