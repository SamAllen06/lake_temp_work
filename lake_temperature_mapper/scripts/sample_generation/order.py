from abc import ABC, abstractmethod
from typing import Mapping

from sample_generation.bound_translator import BoundTranslator


class Order(ABC):
    @abstractmethod
    def __init__(
            self,
            order_data,
            bound_translator: BoundTranslator
    ):
        pass

    @abstractmethod
    def get_sample_count(self) -> int:
        pass

    @abstractmethod
    def get_ranges(self) -> Mapping[str, tuple]:
        pass

    @abstractmethod
    def __iter__(self):
        pass
