import numpy as np
import matplotlib.pyplot as plot

import settings


DEFAULT_RESOLUTION = 600


class FartShake:
    def __init__(
        self,
        amplitude: float,
        frequency: float,
        duration: float,
        damping_factor: float,
        resolution: int = DEFAULT_RESOLUTION,
    ) -> None:
        self.amplitude = amplitude
        self.frequency = frequency
        self.duration = duration
        self.damping_factor = damping_factor
        self.resolution = resolution
        self.time = np.arange(0, self.duration, self.duration / self.resolution)
        self.function = (
            self.amplitude
            * np.sin(self.time * self.frequency)
            * np.exp(-np.log(2) * self.damping_factor * self.time)
        )

    def plot(self):
        plot.plot(self.time, self.function)
        plot.show()


if __name__ == "__main__":
    animation = FartShake(
        amplitude=settings.DEFAULT_AMPLITUDE,
        frequency=settings.DEFAULT_FREQUENCY,
        duration=settings.DEFAULT_DURATION,
        damping_factor=settings.DEFAULT_DAMPING_FACTOR,
    )
    animation.plot()
