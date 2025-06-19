from collections.abc import Sequence
from enum import Enum, auto
from typing import Callable


class IntervalBound(Enum):
    INCLUSIVE = auto()
    EXCLUSIVE = auto()


def find_values_not_meeting_condition(
        values: Sequence[float],
        condition: Callable[[float], bool]
) -> dict[int, float]:
    values_not_meeting_condition: dict[int, float] = {}

    for index, value in enumerate(values):
        if not condition(value):
            values_not_meeting_condition[index] = value

    return values_not_meeting_condition


def are_all_positive(values: Sequence[float], allow_zero=True) -> bool:
    condition: Callable[[float], bool] = lambda value: value >= 0.0

    if not allow_zero:
        condition = lambda value: value > 0.0

    failed_values = find_values_not_meeting_condition(values, condition)

    return len(failed_values) == 0


def are_all_negative(values: Sequence[float], allow_zero=True) -> bool:
    condition: Callable[[float], bool] = lambda value: value <= 0.0

    if not allow_zero:
        condition = lambda value: value < 0.0

    failed_values = find_values_not_meeting_condition(values, condition)

    return len(failed_values) == 0


def are_all_fraction(values: Sequence[float]) -> bool:
    return are_all_within_interval(
        values, 0.0, 1.0, IntervalBound.INCLUSIVE, IntervalBound.INCLUSIVE
    )


def are_all_within_interval(
        values: Sequence[float],
        lower: float,
        upper: float,
        lower_type: IntervalBound,
        upper_type: IntervalBound
) -> bool:
    lower_condition: Callable[[float], bool] = lambda value: value >= lower

    if lower_type == IntervalBound.EXCLUSIVE:
        lower_condition = lambda value: value > lower

    upper_condition: Callable[[float], bool] = lambda value: value >= lower

    if upper_condition == IntervalBound.EXCLUSIVE:
        upper_condition = lambda value: value > lower

    condition: Callable[[float], bool] = lambda value: (
        lower_condition(value) and upper_condition(value)
    )

    failed_values = find_values_not_meeting_condition(values, condition)

    return len(failed_values) == 0
