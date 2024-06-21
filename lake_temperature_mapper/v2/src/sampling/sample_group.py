from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator


class SampleGroupIterator(ABC, Iterator):
    @abstractmethod
    def __next__(self) -> dict[str, float]:
        pass


class SampleGroup(ABC, Iterable):
    @abstractmethod
    def get_sample_count(self) -> int:
        pass

    @abstractmethod
    def get_ranges(self) -> dict[str, tuple[float, float]]:
        pass

    @abstractmethod
    def __iter__(self) -> SampleGroupIterator:
        pass
