"""Camera capture interfaces for the Jetson prototype."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol

from .events import BallEvent


@dataclass(frozen=True)
class CameraFrame:
    """A camera frame captured around a ball event."""

    camera_id: str
    timestamp_ns: int
    width: int
    height: int
    payload: bytes = b""


class FrameCapture(Protocol):
    """Captures frames around a trigger event."""

    def capture_around(self, trigger: BallEvent) -> Sequence[CameraFrame]:
        """Return frames associated with a ball trigger."""


class SyntheticFrameCapture:
    """Deterministic frame capture for the first non-hardware pipeline."""

    def __init__(self, frames: Iterable[CameraFrame]) -> None:
        self._frames = tuple(frames)

    def capture_around(self, trigger: BallEvent) -> Sequence[CameraFrame]:
        return tuple(frame for frame in self._frames if frame.timestamp_ns >= trigger.timestamp_ns)

