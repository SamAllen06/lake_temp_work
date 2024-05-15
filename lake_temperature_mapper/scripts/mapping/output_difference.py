import math

class OutputDifference:
    def __init__(self, index: int, ref: float, test: float):
        self._index = index
        self._ref = ref
        self._test = test
        self._difference = test - ref

    def is_nonzero_difference(self) -> bool:
        if math.isnan(self._ref) and math.isnan(self._test):
            return False
        return not self._difference == 0.0

    def get_index(self) -> int:
        return self._index

    def get_reference(self) -> float:
        return self._ref

    def get_test(self) -> float:
        return self._test

    def get_difference(self) -> float:
        return self._difference
