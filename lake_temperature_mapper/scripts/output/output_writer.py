from abc import ABC, abstractmethod
from typing import Mapping

from sample_generation import SampleGroup
from analysis.output_difference import OutputDifference


class OutputWriter(ABC):
    @abstractmethod
    def write_sample_group_header(
            self, sample_group_name: str, sample_group: SampleGroup 
    ) -> None:
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
            difference_map: Mapping[str, list[OutputDifference]]
    ) -> None:
        pass

    @abstractmethod
    def finish(self) -> None:
        pass
