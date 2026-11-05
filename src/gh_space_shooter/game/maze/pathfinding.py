"""Breadth-first pathfinding helpers for maze validation and gameplay."""

from __future__ import annotations

from collections import deque

from .generator import Maze

Position = tuple[int, int]
_NEIGHBORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def reachable_cells(maze: Maze, start: Position | None = None) -> set[Position]:
    """Return all floor cells reachable from start (defaults to maze.start)."""
    origin = maze.start if start is None else start
    if not maze.is_floor(origin):
        return set()

    visited = {origin}
    queue = deque([origin])
    while queue:
        x, y = queue.popleft()
        for dx, dy in _NEIGHBORS:
            neighbor = (x + dx, y + dy)
            if neighbor not in visited and maze.is_floor(neighbor):
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


def find_path(
    maze: Maze,
    start: Position | None = None,
    goal: Position | None = None,
) -> list[Position] | None:
    """Return a shortest path including both endpoints, or None if unreachable."""
    origin = maze.start if start is None else start
    destination = maze.exit if goal is None else goal
    if not maze.is_floor(origin) or not maze.is_floor(destination):
        return None

    queue = deque([origin])
    parents: dict[Position, Position | None] = {origin: None}

    while queue:
        current = queue.popleft()
        if current == destination:
            path = []
            cursor: Position | None = current
            while cursor is not None:
                path.append(cursor)
                cursor = parents[cursor]
            return list(reversed(path))

        x, y = current
        for dx, dy in _NEIGHBORS:
            neighbor = (x + dx, y + dy)
            if neighbor not in parents and maze.is_floor(neighbor):
                parents[neighbor] = current
                queue.append(neighbor)

    return None
