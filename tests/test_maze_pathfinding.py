"""Tests for maze pathfinding edge cases."""

from gh_space_shooter.game.maze import find_path, generate_maze


def test_path_includes_start_and_goal():
    maze = generate_maze(seed=3)
    path = find_path(maze, maze.start, maze.exit)
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.exit


def test_path_is_none_for_wall_goal():
    maze = generate_maze(seed=5)
    wall = next(
        (x, y)
        for y, row in enumerate(maze.cells)
        for x, is_wall in enumerate(row)
        if is_wall
    )
    assert find_path(maze, maze.start, wall) is None
