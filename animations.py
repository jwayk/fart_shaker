import numpy as np
import matplotlib.pyplot as plot


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
        x = np.arange(0, self.duration, self.duration / self.resolution)
        self.function = (
            self.amplitude
            * np.sin(x * self.frequency)
            * np.exp(-np.log(2) * self.damping_factor * x)
        )

    def plot(self):
        plot.plot(
            np.arange(0, self.duration, self.duration / self.resolution), self.function
        )
        plot.show()


if __name__ == "__main__":
    animation = FartShake(400, 60, 1, 3)
    animation.plot()
