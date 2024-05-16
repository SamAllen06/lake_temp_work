from abc import ABC, abstractmethod
from typing import Mapping

from mapping.order import Order
from mapping.output_difference import OutputDifference


class OutputWriter(ABC):
    @abstractmethod
    def write_order_header(self, order: Order) -> None:
        pass

    @abstractmethod
    def write_parameter_sample(self, parameter_name: str, value: float) -> None:
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
