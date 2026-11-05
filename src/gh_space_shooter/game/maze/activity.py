"""Map aggregate GitHub contribution days onto reachable maze floor cells."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .generator import Maze
from .pathfinding import reachable_cells


@dataclass(frozen=True)
class EnergyPellet:
    """A collectible whose visual intensity is derived from contribution data."""

    position: tuple[int, int]
    intensity: int
    contribution_count: int
    date: str


def build_energy_pellets(
    maze: Maze,
    contribution_days: Iterable[Mapping[str, object]],
) -> list[EnergyPellet]:
    """Create deterministic pellets from active days, only on reachable floor.

    Contribution counts are capped for visual balance. The mapping is a
    gameplay metaphor, not a one-pellet-per-commit representation.
    """
    floor = sorted(
        reachable_cells(maze) - {maze.start, maze.exit},
        key=lambda point: (point[1], point[0]),
    )
    active_days = [
        day for day in contribution_days
        if int(day.get("count", 0) or 0) > 0
    ]
    if not floor or not active_days:
        return []

    pellets: list[EnergyPellet] = []
    for index, day in enumerate(active_days[: len(floor)]):
        count = max(0, int(day.get("count", 0) or 0))
        raw_level = day.get("level", 0)
        level = max(0, min(4, int(raw_level or 0)))
        position_index = min(
            len(floor) - 1,
            (index * len(floor)) // max(1, min(len(active_days), len(floor))),
        )
        pellets.append(
            EnergyPellet(
                position=floor[position_index],
                intensity=max(1, level),
                contribution_count=min(count, 99),
                date=str(day.get("date", "")),
            )
        )
    return pellets
