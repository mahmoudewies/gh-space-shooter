"""Input validation tests for NEON MAZE scene construction."""

import pytest

from gh_space_shooter.game.maze import EnergyPellet, generate_maze
from gh_space_shooter.game.maze.scene import create_game


def test_pellet_cannot_be_placed_inside_a_wall():
    maze = generate_maze(seed=5)
    wall = next(
        (x, y)
        for y, row in enumerate(maze.cells)
        for x, is_wall in enumerate(row)
        if is_wall
    )
    pellet = EnergyPellet(wall, 1, 1, "2026-01-01")
    with pytest.raises(ValueError, match="not a floor cell"):
        create_game(maze, [pellet])
