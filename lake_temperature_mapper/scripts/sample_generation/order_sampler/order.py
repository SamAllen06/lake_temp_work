from abc import abstractmethod
from typing import Mapping

from sample_generation.order_sampler.bound_translator import BoundTranslator
from sample_generation.sample_group import SampleGroup


class Order(SampleGroup):
    @abstractmethod
    def __init__(
            self,
            order_data,
            bound_translator: BoundTranslator
    ):
        pass
