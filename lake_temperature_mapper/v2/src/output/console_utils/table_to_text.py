from collections.abc import Mapping, Sequence
import copy
from typing import Any

from util import Table, TableMapping, TableSequence


def _convert_data_to_strings(data: TableMapping) -> None:
    for key in data:
        for index, value in enumerate(data[key]):
            data[key][index] = str(value)


def _calculate_column_widths(data: TableMapping, seperation: int) -> dict[Any, int]:
    widths = {}

    for key in data:
        max_width = len(str(key))

        for string in data[key]:
            length = len(string)

            max_width = max(max_width, length)

        widths[key] = max_width + seperation

    return widths


def _generate_header(
        column_widths: Mapping[Any, int],
        key_order: Sequence[Any]
) -> str:
    header_values: list[str] = []

    for key in key_order:
        header_values.append(f"{str(key):{column_widths[key]}}")

    return "".join(header_values)


def _generate_rows(
        data: TableSequence,
        column_widths: Mapping[Any, int],
        key_order: Sequence[Any]
) -> list[str]:
    rows: list[str] = []

    for row in data:
        row_values: list[str] = []

        for key in key_order:
            row_values.append(f"{row[key]:<{column_widths[key]}}")

        rows.append("".join(row_values))

    return rows


def convert_to_text(data: Table, seperation: int = 3) -> str:
    data_copy = copy.deepcopy(data)
    data_mapping = data_copy.as_mapping()
    data_sequence = data_copy.as_sequence()

    _convert_data_to_strings(data_mapping)
    key_order = [key for key in data_mapping]

    column_widths = _calculate_column_widths(data_mapping, seperation)
    header = _generate_header(column_widths, key_order)
    rows = _generate_rows(data_sequence, column_widths, key_order)

    return header + "\n" + "\n".join(rows)
