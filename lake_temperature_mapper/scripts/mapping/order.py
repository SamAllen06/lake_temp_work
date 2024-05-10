class Order:
    def __init__(
            self,
            name: str,
            parameter: str,
            sample_count: int,
            start: float,
            end: float
    ):
        self.name = name
        self.parameter = parameter
        self.sample_count = sample_count
        self.start = start
        self.end = end

