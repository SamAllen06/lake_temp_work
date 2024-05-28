import json
from pathlib import Path
from typing import Mapping

from mapping.bound_translator import BoundTranslator
from mapping.order import Order
from mapping.parameter_range import ParameterRange
from mapping.range_reader import RangeReader


class OrderReader:
    def __init__(self, order_directory: Path, range_path: Path):
        self._bound_translator = BoundTranslator(RangeReader(range_path))
        self._order_directory = order_directory

    def read_orders(self) -> list[Order]:
        order_paths = list(self._order_directory.glob("*.json"))

        orders = []

        for path in order_paths:
            orders.append(self._read_order(path))

        return orders

    def _read_order(self, order_path: Path) -> Order:
        with open(order_path) as order_file:
            try:
                order_data = json.loads(order_file.read())
            except json.JSONDecodeError as error:
                raise RuntimeError(f"Invalid json in order {str(order_path)}", error)

        order_name = order_path.name.removesuffix(".json")

        return self._construct_order(order_name, order_data)

    def _construct_order(self, order_name: str, order_data) -> Order:
        try:
            ranges = self._construct_order_ranges(order_data)
            sample_count = order_data["samples"]

            return Order(
                order_name,
                ranges,
                sample_count
            )
        except KeyError:
            raise KeyError(f"Invalid order format in order {order_name}")

    def _construct_order_ranges(self, order_data) -> Mapping[str, ParameterRange]:
        ranges = {}
        for range_data in order_data["ranges"]:
            ranges[range_data["param"]] = ParameterRange(
                self._bound_translator.translate_bound(
                    range_data["param"], range_data["start"]
                ),
                self._bound_translator.translate_bound(
                    range_data["param"], range_data["end"]
                )
            )

        return ranges
