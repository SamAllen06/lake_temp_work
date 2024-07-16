from sampling_libs.ranges import BoundTranslator
from .box_order import BoxOrder
from .line_order import LineOrder
from .order import Order


class OrderFactory:
    def __init__(self, bound_translator: BoundTranslator):
        self._bound_translator = bound_translator

    def construct_order(self, order_data) -> Order:
        if "samples" in order_data:
            return LineOrder(order_data, self._bound_translator)

        return BoxOrder(order_data, self._bound_translator)
