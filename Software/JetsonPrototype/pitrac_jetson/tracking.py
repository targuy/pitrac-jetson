"""Trajectory estimation interfaces for the Jetson prototype."""

from collections.abc import Sequence
from dataclasses import dataclass
from math import atan2, hypot, pi

from .calibration import CalibrationProfile
from .vision import DetectionSample


@dataclass(frozen=True)
class TrackEstimate:
    """Basic 2D launch estimate derived from image-space detections."""

    speed_mps: float
    angle_deg: float
    sample_count: int


class Basic2DTracker:
    """Compute a first-pass 2D speed and angle from ordered detections."""

    def estimate(
        self, detections: Sequence[DetectionSample], calibration: CalibrationProfile
    ) -> TrackEstimate | None:
        if len(detections) < 2:
            return None

        ordered = sorted(detections, key=lambda sample: sample.timestamp_ns)
        first = ordered[0]
        last = ordered[-1]
        elapsed_s = (last.timestamp_ns - first.timestamp_ns) / 1_000_000_000
        if elapsed_s <= 0:
            return None

        dx_m = (last.position.x_px - first.position.x_px) / calibration.pixels_per_meter
        dy_m = (last.position.y_px - first.position.y_px) / calibration.pixels_per_meter

        return TrackEstimate(
            speed_mps=hypot(dx_m, dy_m) / elapsed_s,
            angle_deg=atan2(dy_m, dx_m) * 180.0 / pi,
            sample_count=len(ordered),
        )
