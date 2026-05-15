"""Ball sensor interfaces and simple test doubles."""

from collections.abc import Iterable, Iterator
from typing import Protocol

from .events import BallEvent


class BallSensor(Protocol):
    """Source of timestamped ball events."""

    def events(self) -> Iterator[BallEvent]:
        """Yield ball events in timestamp order."""


class ScriptedBallSensor:
    """Deterministic sensor source for development and tests."""

    def __init__(self, events: Iterable[BallEvent]) -> None:
        self._events = tuple(events)

    def events(self) -> Iterator[BallEvent]:
        yield from self._events

