import json
from pathlib import Path
import re

from mapping.order import Order
from mapping.range_reader import RangeReader


class OrderReader:
    def __init__(self, order_directory: Path, range_path: Path):
        self.order_directory = order_directory
        self._range_reader = RangeReader(range_path)

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
        try:
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
        except KeyError:
            raise KeyError(f"Invalid order format in order {order_name}")

    def _translate_bound_value(self, parameter: str, value: str) -> float:
        expression_string = self._translate_shorthand(parameter, value)
        numbers = [float(number) for number in re.findall(
            r"(?<!\d)-?[\d.]+", expression_string
        )]
        operators = re.findall(r"[+\*\/]|(?<=\s)-(?=\s)|(?<=\d)-(?=\d)", expression_string)

        for index, operator in reversed(list(enumerate(operators))):
            match operator:
                case "*":
                    numbers[index] = numbers[index] * numbers[index + 1]
                case "/":
                    numbers[index] = numbers[index] / numbers[index + 1]
                case other:
                    continue
            numbers.pop(index + 1)
            operators.pop(index)

        for index, operator in reversed(list(enumerate(operators))):
            match operator:
                case "+":
                    numbers[index] = numbers[index] + numbers[index + 1]
                case "-":
                    numbers[index] = numbers[index] - numbers[index + 1]
            numbers.pop(index + 1)
            operators.pop(index)

        return numbers[0]


    def _translate_shorthand(self, parameter: str, value: str) -> str:
        range_strings = set(re.findall(r"r\(-?[\d.]+\)", value))

        final_string = value

        for range_string in range_strings:
            time = float(range_string[2:-1])
            translated_value = str(
                self._linear_interpolate_range(parameter, time)
            )
            final_string = final_string.replace(range_string, translated_value)

        return final_string

    def _linear_interpolate_range(self, parameter: str, time: float) -> float:
        min = self._range_reader.get_min(parameter)
        max = self._range_reader.get_max(parameter)

        return min * (1.0 - time) + max * time



