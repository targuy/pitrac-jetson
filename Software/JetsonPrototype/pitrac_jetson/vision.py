"""Ball detection interfaces for captured Jetson frames."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol

from .capture import CameraFrame
from .events import BallPosition


@dataclass(frozen=True)
class DetectionSample:
    """A detected ball position in a specific camera frame."""

    camera_id: str
    timestamp_ns: int
    position: BallPosition
    confidence: float = 1.0


class BallDetector(Protocol):
    """Detects ball positions in camera frames."""

    def detect(self, frames: Sequence[CameraFrame]) -> Sequence[DetectionSample]:
        """Return ball detections for the supplied frames."""


class ScriptedBallDetector:
    """Deterministic detector used before camera-specific vision is available."""

    def __init__(self, samples: Iterable[DetectionSample]) -> None:
        self._samples = tuple(samples)

    def detect(self, frames: Sequence[CameraFrame]) -> Sequence[DetectionSample]:
        frame_keys = {(frame.camera_id, frame.timestamp_ns) for frame in frames}
        return tuple(
            sample for sample in self._samples if (sample.camera_id, sample.timestamp_ns) in frame_keys
        )

