class Sampler:
    def __init__(
            self,
            start_value: float,
            end_value: float,
            samples: int
    ):
        self.start_value = start_value
        self.end_value = end_value
        self.samples = samples

    def _linear_interpolate(self, time: float):
        return self.start_value * (1 - time) + self.end_value * time

    def get_samples(self) -> list[float]:
        input_samples = []

        for sample_index in range(self.samples):
            time = sample_index / (self.samples - 1)
            input_samples.append(self._linear_interpolate(time))

        return input_samples



