"""Tests for contribution-driven energy pellet placement."""

from gh_space_shooter.game.maze import build_energy_pellets, generate_maze, reachable_cells


def test_pellets_only_appear_on_reachable_floor():
    maze = generate_maze(seed=17)
    days = [
        {"date": "2026-01-01", "count": 2, "level": 1},
        {"date": "2026-01-02", "count": 8, "level": 3},
        {"date": "2026-01-03", "count": 20, "level": 4},
    ]
    pellets = build_energy_pellets(maze, days)
    reachable = reachable_cells(maze)
    assert len(pellets) == 3
    assert all(p.position in reachable for p in pellets)
    assert all(p.position not in {maze.start, maze.exit} for p in pellets)


def test_zero_activity_produces_no_pellets():
    maze = generate_maze(seed=19)
    days = [{"date": "2026-01-01", "count": 0, "level": 0}]
    assert build_energy_pellets(maze, days) == []


def test_pellet_values_are_capped():
    maze = generate_maze(seed=23)
    pellets = build_energy_pellets(
        maze,
        [{"date": "2026-01-01", "count": 1000, "level": 99}],
    )
    assert pellets[0].contribution_count == 99
    assert pellets[0].intensity == 4
