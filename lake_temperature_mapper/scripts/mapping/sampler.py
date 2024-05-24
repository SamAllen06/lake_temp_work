from mapping.parameter_range import ParameterRange
from typing import Mapping


class Sampler:
    def __init__(
            self,
            ranges: Mapping[str, ParameterRange],
            samples: int
    ):
        self.ranges = ranges
        self.samples = samples

    def __iter__(self):
        return SamplerIterable(self)


class SamplerIterable:
    def __init__(self, sampler: Sampler):
        self._sampler = sampler
        self._index = 0

    def __next__(self) -> Mapping[str, float]:
        if self._index >= self._sampler.samples:
            raise StopIteration

        sample = {}
        for parameter in self._sampler.ranges.keys():
            sample[parameter] = self._sample_parameter_range(parameter)

        self._index += 1

        return sample

    def _sample_parameter_range(self, parameter: str) -> float:
        if self._sampler.samples == 1:
            return self._sampler.ranges[parameter].end

        time = self._index / (self._sampler.samples - 1)

        return (
            self._sampler.ranges[parameter].start * (1.0 - time)
            + self._sampler.ranges[parameter].end * time
        )
