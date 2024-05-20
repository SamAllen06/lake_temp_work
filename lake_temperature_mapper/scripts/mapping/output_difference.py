import math

import numpy as np

class OutputDifference:
    def __init__(self, index: int, ref: np.float64, test: np.float64):
        self._index = index
        self._ref = ref
        self._test = test
        self._difference = test - ref

    def is_nonzero_difference(self) -> bool:
        if np.isnan(self._ref) and np.isnan(self._test):
            return False
        return not self._difference == 0.0

    def get_index(self) -> int:
        return self._index

    def get_reference(self) -> np.float64:
        return self._ref

    def get_test(self) -> np.float64:
        return self._test

    def get_difference(self) -> np.float64:
        return self._difference
