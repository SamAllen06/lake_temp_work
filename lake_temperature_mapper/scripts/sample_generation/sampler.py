from abc import ABC, abstractmethod
from typing import Mapping

from sample_generation.sample_group import SampleGroup


class Sampler(ABC):
    @abstractmethod
    def get_sample_groups(self) -> Mapping[str, SampleGroup]:
        pass

