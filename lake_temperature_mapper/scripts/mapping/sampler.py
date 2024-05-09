class Sampler:
    def __init__(
            from: float,
            to: float,
            samples: int
    ):
        self.from = from
        self.to = to
        self.samples = samples

    def _linear_interpolate(self, time: float):
        return self.from * (1 - time) + self.to * time

    def get_input_samples(self) -> list[float]:
        input_samples = []

        for sample_index in range(samples):
            time = sample_index / (samples - 1)
            input_samples.append(_linear_interpolate(time))

        return input_samples



