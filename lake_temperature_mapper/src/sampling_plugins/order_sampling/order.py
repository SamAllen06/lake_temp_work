from abc import abstractmethod
from typing import Mapping

from sampling import SampleGroup

from sampling_libs.range_interpolation import BoundTranslator


class Order(SampleGroup):
    @abstractmethod
    def __init__(self, order_data, bound_translator: BoundTranslator):
        pass
