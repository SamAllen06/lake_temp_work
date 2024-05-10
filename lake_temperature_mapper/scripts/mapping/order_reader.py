import json
from pathlib import Path

from mapping.config_reader import ConfigReader
from mapping.order import Order
from mapping.range_reader import RangeReader


class OrderReader:
    def __init__(self, order_directory: Path, range_path: Path):
        self.order_directory = order_directory
        self.range_reader = RangeReader(range_path)

    def read_orders(self) -> list[Order]:
        order_paths = list(self.order_directory.glob("*.json"))

        orders = []

        for path in order_paths:
            orders.append(self._read_order(path))

        return orders

    def _read_order(self, order_path: Path) -> Order:
        with open(order_path) as order_file:
            order_data = json.loads(order_file.read())

        order_name = order_path.name.removesuffix(".json")

        return self._construct_order(order_name, order_data)

    def _construct_order(self, order_name: str, order_data) -> Order:
        return Order(
            order_name,
            order_data["param"],
            order_data["samples"],
            self._translate_bound_value(
                order_data["param"],
                order_data["start"]
            ),
            self._translate_bound_value(
                order_data["param"],
                order_data["end"]
            )
        )

    def _translate_bound_value(self, parameter: str, value: str) -> float:
        match (value):
            case "m":
                return self.range_reader.get_min(parameter)
            case "M":
                return self.range_reader.get_max(parameter)
            case other:
                return float(value)

