"""Incremental Jetson prototype interfaces for PiTrac."""

from .calibration import CalibrationProfile
from .capture import CameraFrame, FrameCapture, SyntheticFrameCapture
from .events import BallEvent, BallEventType, BallPosition, Timestamped
from .output import MemoryShotPublisher, ShotPublisher
from .pipeline import JetsonPrototypePipeline
from .sensors import BallSensor, ScriptedBallSensor
from .tracking import Basic2DTracker, TrackEstimate
from .vision import BallDetector, DetectionSample, ScriptedBallDetector

__all__ = [
    "BallDetector",
    "BallEvent",
    "BallEventType",
    "BallPosition",
    "BallSensor",
    "Basic2DTracker",
    "CalibrationProfile",
    "CameraFrame",
    "DetectionSample",
    "FrameCapture",
    "JetsonPrototypePipeline",
    "MemoryShotPublisher",
    "ScriptedBallDetector",
    "ScriptedBallSensor",
    "ShotPublisher",
    "SyntheticFrameCapture",
    "Timestamped",
    "TrackEstimate",
]

