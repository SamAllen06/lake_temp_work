from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Mapping, Sized


class SampleGroupIterator(ABC, Iterator):
    @abstractmethod
    def __next__(self) -> Mapping[str, float]:
        pass


class SampleGroup(ABC, Iterable, Sized):
    @abstractmethod
    def get_sample_count(self) -> int:
        pass

    @abstractmethod
    def __iter__(self) -> SampleGroupIterator:
        pass

    def __len__(self) -> int:
        return self.get_sample_count()
