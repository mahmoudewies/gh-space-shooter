"""Immutable arcade entities for NEON MAZE."""

from __future__ import annotations

from dataclasses import dataclass

Position = tuple[int, int]


@dataclass(frozen=True)
class Player:
    """The player's current position and collected-energy score."""

    position: Position
    score: int = 0


@dataclass(frozen=True)
class Ghost:
    """A decorative patrol enemy; it never blocks the guaranteed player route."""

    position: Position
    patrol_index: int
