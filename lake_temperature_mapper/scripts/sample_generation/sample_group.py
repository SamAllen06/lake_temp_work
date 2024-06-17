from abc import ABC, abstractmethod


class SampleGroupIterable(ABC):
    @abstractmethod
    def __next__(self) -> dict[str, float]:
        pass


class SampleGroup(ABC):
    @abstractmethod
    def get_sample_count(self) -> int:
        pass

    @abstractmethod
    def get_ranges(self) -> dict[str, tuple[float, float]]:
        pass

    @abstractmethod
    def __iter__(self) -> SampleGroupIterable:
        pass
