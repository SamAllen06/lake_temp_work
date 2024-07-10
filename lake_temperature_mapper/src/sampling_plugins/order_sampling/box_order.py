from sampling import SampleGroupIterator

from .bound_translator import BoundTranslator
from .order import Order


class BoxOrder(Order):
    def __init__(self, order_data, bound_translator: BoundTranslator):
        self._bound_translator = bound_translator
        self._ranges = self._read_ranges(order_data["ranges"])

    def get_sample_count(self) -> int:
        sample_count = 1

        for parameter in self._ranges.keys():
            subsample_count = self._ranges[parameter][2]
            sample_count *= subsample_count

        return sample_count

    def __iter__(self):
        return BoxOrderIterator(self._ranges)

    def _read_ranges(self, ranges_data) -> dict[str, tuple[float, float, int]]:
        ranges = {}

        for parameter in ranges_data.keys():
            range_data = ranges_data[parameter]
            ranges[parameter] = (
                self._bound_translator.translate_bound(parameter, range_data[0]),
                self._bound_translator.translate_bound(parameter, range_data[1]),
                range_data[2],
            )

        return ranges


class BoxOrderIterator(SampleGroupIterator):
    def __init__(self, ranges: dict[str, tuple[float, float, int]]):
        self._ranges = ranges
        self._parameter_order = [parameter for parameter in self._ranges.keys()]
        self._indices = {parameter: 0 for parameter in self._ranges.keys()}
        self._last_changed_index = len(self._ranges) - 1
        self._current_sample: dict[str, float] = {}
        self._update_sample()

    def __next__(self) -> dict[str, float]:
        last_parameter = self._parameter_order[-1]
        if self._indices[last_parameter] >= self._ranges[last_parameter][2]:
            raise StopIteration

        self._update_sample()

        partial_sample = {
            parameter: self._current_sample[parameter]
            for parameter in self._parameter_order[0 : self._last_changed_index + 1]
        }

        self._increment_indices()

        return partial_sample

    def _update_sample(self) -> None:
        for parameter in self._parameter_order[0 : self._last_changed_index + 1]:
            self._current_sample[parameter] = self._sample_parameter_range(parameter)

    def _sample_parameter_range(self, parameter: str) -> float:
        parameter_range = self._ranges[parameter]

        index = self._indices[parameter]
        sample_count = parameter_range[2]

        time = index / (sample_count - 1)

        min = parameter_range[0]
        max = parameter_range[1]

        return min * (1.0 - time) + max * time

    def _increment_indices(self) -> None:
        for parameter_index, parameter in enumerate(self._parameter_order):
            sample_index = self._indices[parameter]
            sample_count = self._ranges[parameter][2]

            if (
                sample_index < sample_count - 1
                or parameter_index == len(self._parameter_order) - 1
            ):
                self._indices[parameter] += 1
                self._last_changed_index = parameter_index
                break

            self._indices[parameter] = 0
