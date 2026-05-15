"""Shared event and geometry models for the Jetson prototype."""

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Timestamped:
    """Base value object for hardware events measured on the Jetson."""

    timestamp_ns: int


class BallEventType(str, Enum):
    """Ball sensor events used by the first incremental prototype."""

    PRESENT = "present"
    IMPACT = "impact"
    DEPARTURE = "departure"


@dataclass(frozen=True)
class BallEvent(Timestamped):
    """A timestamped ball sensor event."""

    event_type: BallEventType
    sensor_id: str


@dataclass(frozen=True)
class BallPosition:
    """A 2D ball position in image coordinates."""

    x_px: float
    y_px: float

