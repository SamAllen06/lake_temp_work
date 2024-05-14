import math

class OutputDifference:
    def __init__(self, index: int, ref: float, test: float):
        self._index = index
        self._ref = ref
        self._test = test
        self._difference = test - ref

    def get_difference(self) -> float:
        if math.isnan(self._ref) and math.isnan(self._test):
            return 0.0
        return self._difference

    def __str__(self):
        return (
            f"{self._ref:<20} -> {self._test:<20} "
            f"by {self._difference:<20} at {self._index}"
        )

