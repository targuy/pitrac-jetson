"""Minimal Jetson prototype orchestration pipeline."""

from dataclasses import dataclass

from .calibration import CalibrationProfile
from .capture import FrameCapture
from .output import ShotPublisher
from .sensors import BallSensor
from .tracking import Basic2DTracker, TrackEstimate
from .vision import BallDetector


@dataclass
class JetsonPrototypePipeline:
    """Connect the first incremental Jetson components end to end."""

    sensor: BallSensor
    capture: FrameCapture
    detector: BallDetector
    tracker: Basic2DTracker
    calibration: CalibrationProfile
    publisher: ShotPublisher

    def run_once(self) -> TrackEstimate | None:
        """Process the first sensor event that produces a usable track."""

        for event in self.sensor.events():
            frames = self.capture.capture_around(event)
            detections = self.detector.detect(frames)
            estimate = self.tracker.estimate(detections, self.calibration)
            if estimate is not None:
                self.publisher.publish(estimate)
                return estimate
        return None

