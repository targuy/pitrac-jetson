"""Output interfaces for publishing Jetson prototype shot results."""

from typing import Protocol

from .tracking import TrackEstimate


class ShotPublisher(Protocol):
    """Publishes shot estimates to a UI, API, broker, or simulator adapter."""

    def publish(self, estimate: TrackEstimate) -> None:
        """Publish a single shot estimate."""


class MemoryShotPublisher:
    """In-memory publisher for tests and early web UI integration."""

    def __init__(self) -> None:
        self.estimates: list[TrackEstimate] = []

    def publish(self, estimate: TrackEstimate) -> None:
        self.estimates.append(estimate)

