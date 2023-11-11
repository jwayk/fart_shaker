import random

import numpy as np
import matplotlib.pyplot as plot
from scipy.signal import savgol_filter

import settings


DEFAULT_RESOLUTION = 300


class Animation:
    samples_per_second = DEFAULT_RESOLUTION

    def __init__(self, duration_seconds: float, samples_per_second: int = None):
        self.duration_seconds = duration_seconds
        self.samples_per_second = samples_per_second or self.samples_per_second
        self.time = np.arange(0, self.duration_seconds, 1 / self.samples_per_second)
        self.base_function = self.calculate()

    @property
    def transform_function(self):
        return self.get_transform()

    def get_transform(self):
        return self.base_function

    def calculate(self):
        return np.zeros(self.time.shape)

    def plot(self):
        plot.plot(self.time, self.transform_function)
        plot.show()


class Wobble(Animation):
    def __init__(
        self,
        amplitude: float,
        frequency: float,
        damping_factor: float,
        duration_seconds: float,
        phase_degrees: float = 0,
    ) -> None:
        self.amplitude = amplitude
        self.frequency = frequency
        self.damping_factor = damping_factor
        self.phase = phase_degrees
        super().__init__(duration_seconds)

    def calculate(self):
        return (
            self.amplitude
            * np.sin(self.frequency * self.time + np.radians(self.phase))
            * np.exp(-np.log(2) * self.damping_factor * self.time)
        )


class Bulge(Animation):
    def __init__(
        self, amplitude: float, damping_factor: float, duration_seconds: float
    ):
        self.amplitude = amplitude
        self.damping_factor = damping_factor
        super().__init__(duration_seconds)

    def calculate(self):
        return self.amplitude * np.exp(-np.log(2) * self.damping_factor * self.time)


class NoisyRattle(Wobble):
    recalculate = True
    noisy_transform = []

    def __init__(
        self,
        amplitude: float,
        frequency: float,
        damping_factor: float,
        duration_seconds: float,
    ) -> None:
        super().__init__(
            amplitude,
            frequency,
            damping_factor,
            duration_seconds,
        )

    def calculate(self):
        self.phase = random.randint(0, 360)
        return savgol_filter(
            super().calculate() * np.random.normal(size=self.time.shape), 20, 10
        )

    def get_transform(self):
        if self.recalculate:
            self.noisy_transform = self.calculate()
            self.recalculate = False
        return self.noisy_transform

    def randomize(self):
        self.recalculate = True


class PlanarShake:
    def __init__(
        self,
        amplitude: float,
        frequency: float,
        damping_factor: float,
        duration_seconds: float,
    ):
        self.x = NoisyRattle(amplitude, frequency, damping_factor, duration_seconds)
        self.y = NoisyRattle(amplitude, frequency, damping_factor, duration_seconds)

    def randomize(self):
        self.x.randomize()
        self.y.randomize()


if __name__ == "__main__":
    # animation = Wobble(
    #     amplitude=settings.DEFAULT_AMPLITUDE,
    #     frequency=settings.DEFAULT_FREQUENCY,
    #     damping_factor=settings.DEFAULT_DAMPING_FACTOR,
    #     duration_seconds=settings.DEFAULT_DURATION,
    # )
    # animation.plot()

    # bulge = Bulge(10, 5, 5)
    # bulge.plot()

    animation = NoisyRattle(
        amplitude=settings.DEFAULT_AMPLITUDE,
        frequency=settings.DEFAULT_FREQUENCY,
        damping_factor=settings.DEFAULT_DAMPING_FACTOR,
        duration_seconds=settings.DEFAULT_DURATION,
    )
    plot.plot(animation.time, animation.transform_function)
    animation.randomize()
    plot.plot(animation.time, animation.transform_function)
    plot.show()
    # animation.plot()
