"""Deterministic NEON MAZE gameplay simulation."""

from __future__ import annotations

from dataclasses import dataclass

from .activity import EnergyPellet
from .entities import Ghost, Player, Position
from .generator import Maze
from .pathfinding import find_path


@dataclass(frozen=True)
class GameState:
    """Complete immutable snapshot of one simulation frame."""

    player: Player
    ghosts: tuple[Ghost, ...]
    collected: frozenset[Position]
    tick: int
    complete: bool
    route: tuple[Position, ...]


def _join_paths(segments: list[list[Position]]) -> tuple[Position, ...]:
    route: list[Position] = []
    for segment in segments:
        if not segment:
            continue
        route.extend(segment if not route else segment[1:])
    return tuple(route)


def _build_player_route(maze: Maze, pellets: tuple[EnergyPellet, ...]) -> tuple[Position, ...]:
    """Visit every distinct pellet in stable order, then reach the exit."""
    targets = sorted(
        {pellet.position for pellet in pellets},
        key=lambda point: (point[1], point[0]),
    )
    current = maze.start
    segments: list[list[Position]] = []
    for target in targets:
        segment = find_path(maze, current, target)
        if segment is None:
            continue
        segments.append(segment)
        current = target
    final_segment = find_path(maze, current, maze.exit)
    if final_segment is None:
        raise ValueError("Maze exit is unreachable from the player route")
    segments.append(final_segment)
    return _join_paths(segments)


def create_game(
    maze: Maze,
    pellets: tuple[EnergyPellet, ...] | list[EnergyPellet] = (),
    ghost_count: int = 2,
) -> GameState:
    """Create a deterministic, completable arcade run."""
    if ghost_count < 0:
        raise ValueError("ghost_count cannot be negative")
    pellet_tuple = tuple(pellets)
    for pellet in pellet_tuple:
        if not maze.is_floor(pellet.position):
            raise ValueError(f"Pellet position is not a floor cell: {pellet.position}")

    route = _build_player_route(maze, pellet_tuple)
    patrol = find_path(maze, maze.exit, maze.start) or [maze.start]
    ghosts = tuple(
        Ghost(
            position=patrol[min(len(patrol) - 1, (index + 1) * len(patrol) // (ghost_count + 1))],
            patrol_index=min(len(patrol) - 1, (index + 1) * len(patrol) // (ghost_count + 1)),
        )
        for index in range(ghost_count)
    )
    initial_collected = frozenset(
        pellet.position for pellet in pellet_tuple if pellet.position == maze.start
    )
    return GameState(
        player=Player(position=maze.start, score=len(initial_collected)),
        ghosts=ghosts,
        collected=initial_collected,
        tick=0,
        complete=len(route) == 1 and route[0] == maze.exit,
        route=route,
    )


def advance_game(
    state: GameState,
    pellets: tuple[EnergyPellet, ...] | list[EnergyPellet] = (),
) -> GameState:
    """Advance one frame, collect pellets, and move patrol ghosts.

    Ghosts are visual hazards only in this profile animation: they cannot
    invalidate the route or prevent the player from completing the maze.
    """
    if state.complete:
        return state

    next_tick = state.tick + 1
    next_index = min(next_tick, len(state.route) - 1)
    next_position = state.route[next_index]
    pellet_positions = {pellet.position for pellet in pellets}
    collected = state.collected | (
        {next_position} if next_position in pellet_positions else set()
    )

    ghosts: list[Ghost] = []
    for ghost in state.ghosts:
        # A compact back-and-forth patrol along the deterministic route.
        patrol_length = max(1, len(state.route))
        phase = (ghost.patrol_index + next_tick) % (2 * patrol_length - 2) if patrol_length > 1 else 0
        patrol_index = phase if phase < patrol_length else 2 * patrol_length - 2 - phase
        patrol_index = min(patrol_index, patrol_length - 1)
        ghosts.append(
            Ghost(position=state.route[patrol_index], patrol_index=patrol_index)
        )

    all_pellets = {pellet.position for pellet in pellets}
    complete = next_position == state.route[-1] and all_pellets.issubset(collected)
    return GameState(
        player=Player(position=next_position, score=len(collected)),
        ghosts=tuple(ghosts),
        collected=frozenset(collected),
        tick=next_tick,
        complete=complete,
        route=state.route,
    )


def run_to_completion(
    state: GameState,
    pellets: tuple[EnergyPellet, ...] | list[EnergyPellet] = (),
) -> GameState:
    """Run the deterministic simulation until the exit is reached."""
    current = state
    # The route is finite; this bound also protects callers from malformed states.
    for _ in range(max(1, len(state.route) + 1)):
        if current.complete:
            return current
        current = advance_game(current, pellets)
    return current
