from sample_generation.bound_translator import BoundTranslator
from sample_generation.box_order import BoxOrder
from sample_generation.line_order import LineOrder
from sample_generation.order import Order


class OrderFactory:
    def __init__(self, bound_translator: BoundTranslator):
        self._bound_translator = bound_translator

    def construct_order(self, order_data) -> Order:
        try:
            if "samples" in order_data:
                return LineOrder(order_data, self._bound_translator)
            
            return BoxOrder(order_data, self._bound_translator)
        except KeyError:
            raise KeyError(f"Invalid order format in order {order_name}")
