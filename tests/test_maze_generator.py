"""Tests for deterministic maze generation and connectivity."""

import pytest

from gh_space_shooter.game.maze import find_path, generate_maze, reachable_cells


def test_generation_is_deterministic():
    first = generate_maze(width=21, height=13, seed=42)
    second = generate_maze(width=21, height=13, seed=42)
    assert first.cells == second.cells


def test_different_seeds_can_change_layout():
    first = generate_maze(width=21, height=13, seed=1)
    second = generate_maze(width=21, height=13, seed=2)
    assert first.cells != second.cells


def test_generated_maze_has_valid_start_to_exit_path():
    maze = generate_maze(width=21, height=13, seed=7)
    path = find_path(maze)
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.exit
    assert all(maze.is_floor(cell) for cell in path)


def test_all_floor_cells_are_reachable():
    maze = generate_maze(width=21, height=13, seed=13)
    reachable = reachable_cells(maze)
    all_floor = {
        (x, y)
        for y, row in enumerate(maze.cells)
        for x, is_wall in enumerate(row)
        if not is_wall
    }
    assert reachable == all_floor


@pytest.mark.parametrize("width,height", [(4, 9), (9, 4), (10, 11), (11, 10)])
def test_invalid_dimensions_are_rejected(width, height):
    with pytest.raises(ValueError):
        generate_maze(width=width, height=height)
