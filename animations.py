import numpy as np
import matplotlib.pyplot as plot

import settings


DEFAULT_RESOLUTION = 300


class Animation:

    time = []
    function = []
    samples_per_second = DEFAULT_RESOLUTION

    def __init__(self, duration_seconds: float, samples_per_second: int = None):
        self.duration_seconds = duration_seconds
        self.samples_per_second = samples_per_second or self.samples_per_second
        self.time = np.arange(0, self.duration_seconds, 1 / self.samples_per_second)

    def plot(self):
        plot.plot(self.time, self.function)
        plot.show()


class FartShake(Animation):
    def __init__(
        self,
        amplitude: float,
        frequency: float,
        damping_factor: float,
        duration_seconds: float,
    ) -> None:
        super().__init__(duration_seconds)
        self.amplitude = amplitude
        self.frequency = frequency
        self.damping_factor = damping_factor
        self.function = (
            self.amplitude
            * np.sin(self.time * self.frequency)
            * np.exp(-np.log(2) * self.damping_factor * self.time)
        )


class Bulge(Animation):
    def __init__(self, amplitude: float, damping_factor: float, duration_seconds: float):
        super().__init__(duration_seconds)
        self.amplitude = amplitude
        self.damping_factor = damping_factor
        self.function = (
            self.amplitude
            * np.exp(-np.log(2) * self.damping_factor * self.time)
        )


if __name__ == "__main__":
    animation = FartShake(
        amplitude=settings.DEFAULT_AMPLITUDE,
        frequency=settings.DEFAULT_FREQUENCY,
        damping_factor=settings.DEFAULT_DAMPING_FACTOR,
        duration_seconds=settings.DEFAULT_DURATION,
    )
    animation.plot()

    bulge = Bulge(10, 5, 5)
    bulge.plot()
