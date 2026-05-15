"""Calibration values shared by prototype tracking stages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationProfile:
    """Minimal calibration profile for early 2D speed and angle estimates."""

    name: str = "uncalibrated"
    pixels_per_meter: float = 1.0

    def __post_init__(self) -> None:
        if self.pixels_per_meter <= 0:
            raise ValueError("pixels_per_meter must be greater than zero")

