from sampling import SampleGroupIterator

from .bound_translator import BoundTranslator
from .order import Order


class LineOrder(Order):
    def __init__(self, order_data, bound_translator: BoundTranslator):
        self._bound_translator = bound_translator
        self._samples = order_data["samples"]
        self._ranges = self._read_ranges(order_data["ranges"])

    def get_sample_count(self) -> int:
        return self._samples

    def __iter__(self):
        return LineOrderIterator(self._samples, self._ranges)

    def _read_ranges(self, ranges_data) -> dict[str, tuple[float, float]]:
        ranges = {}

        for parameter in ranges_data.keys():
            range_data = ranges_data[parameter]
            ranges[parameter] = (
                self._bound_translator.translate_bound(parameter, range_data[0]),
                self._bound_translator.translate_bound(parameter, range_data[1]),
            )

        return ranges


class LineOrderIterator(SampleGroupIterator):
    def __init__(self, sample_count: int, ranges: dict[str, tuple[float, float]]):
        self._sample_count = sample_count
        self._ranges = ranges
        self._index = 0

    def __next__(self) -> dict[str, float]:
        if self._index >= self._sample_count:
            raise StopIteration

        sample = {}
        for parameter in self._ranges.keys():
            sample[parameter] = self._sample_parameter_range(
                self._ranges[parameter][0], self._ranges[parameter][1]
            )

        self._index += 1

        return sample

    def _sample_parameter_range(self, min: float, max: float) -> float:
        if self._sample_count == 1:
            return max

        time = self._index / (self._sample_count - 1)

        return min * (1.0 - time) + max * time
