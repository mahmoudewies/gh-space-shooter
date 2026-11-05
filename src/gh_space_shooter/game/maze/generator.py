"""Deterministic, connected perfect-maze generation."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Maze:
    """A maze represented by True wall cells and False floor cells."""

    width: int
    height: int
    cells: tuple[tuple[bool, ...], ...]
    start: tuple[int, int]
    exit: tuple[int, int]

    def is_floor(self, position: tuple[int, int]) -> bool:
        x, y = position
        return (
            0 <= x < self.width
            and 0 <= y < self.height
            and not self.cells[y][x]
        )


def generate_maze(width: int = 21, height: int = 13, seed: int = 0) -> Maze:
    """Generate a deterministic perfect maze using randomized depth-first search.

    Dimensions must be odd and at least 5 so the maze has a one-cell outer
    border and a meaningful interior. The same dimensions and seed always
    produce the same maze.
    """
    if width < 5 or height < 5 or width % 2 == 0 or height % 2 == 0:
        raise ValueError("Maze width and height must be odd integers >= 5")

    grid = [[True for _ in range(width)] for _ in range(height)]
    rng = random.Random(seed)
    start = (1, 1)
    stack = [start]
    grid[start[1]][start[0]] = False

    while stack:
        x, y = stack[-1]
        candidates = []
        for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)):
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1:
                if grid[ny][nx]:
                    candidates.append((nx, ny, dx, dy))

        if not candidates:
            stack.pop()
            continue

        nx, ny, dx, dy = rng.choice(candidates)
        grid[y + dy // 2][x + dx // 2] = False
        grid[ny][nx] = False
        stack.append((nx, ny))

    exit_position = (width - 2, height - 2)
    return Maze(
        width=width,
        height=height,
        cells=tuple(tuple(row) for row in grid),
        start=start,
        exit=exit_position,
    )
