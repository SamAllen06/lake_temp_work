from mapping.parameter_range import ParameterRange


class Order:
    def __init__(
            self,
            name: str,
            ranges: list[ParameterRange],
            sample_count: int
    ):
        self.name = name
        self.ranges = ranges
        self.sample_count = sample_count
