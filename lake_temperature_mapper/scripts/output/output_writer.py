from abc import ABC, abstractmethod
from typing import Mapping

from sample_generation.order import Order
from analysis.output_difference import OutputDifference


class OutputWriter(ABC):
    @abstractmethod
    def write_order_header(self, order_name: str, order: Order) -> None:
        pass

    @abstractmethod
    def write_sample(self, sample: Mapping[str, float]) -> None:
        pass

    @abstractmethod
    def write_binary_exit(self, exit_code: int) -> None:
        pass

    @abstractmethod
    def write_difference_map(
            self,
            difference_map: Mapping[str, OutputDifference]
    ) -> None:
        pass

    @abstractmethod
    def finish(self) -> None:
        pass
