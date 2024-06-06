from sample_generation.order_sampler.bound_translator import BoundTranslator
from sample_generation.order_sampler.box_order import BoxOrder
from sample_generation.order_sampler.line_order import LineOrder
from sample_generation.order_sampler.order import Order


class OrderFactory:
    def __init__(self, bound_translator: BoundTranslator):
        self._bound_translator = bound_translator

    def construct_order(self, order_data) -> Order:
        if "samples" in order_data:
            return LineOrder(order_data, self._bound_translator)
        
        return BoxOrder(order_data, self._bound_translator)
