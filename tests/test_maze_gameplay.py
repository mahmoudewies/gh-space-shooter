"""Gameplay tests for player movement, collection, patrols, and completion."""

from gh_space_shooter.game.maze import EnergyPellet, generate_maze
from gh_space_shooter.game.maze.scene import advance_game, create_game, run_to_completion


def _pellets(maze):
    return [
        EnergyPellet(position=(3, 1), intensity=2, contribution_count=4, date="2026-01-01"),
        EnergyPellet(position=(5, 3), intensity=3, contribution_count=8, date="2026-01-02"),
    ]


def test_player_moves_one_route_cell_per_tick():
    maze = generate_maze(seed=21)
    state = create_game(maze, _pellets(maze), ghost_count=0)
    next_state = advance_game(state, _pellets(maze))
    assert next_state.tick == 1
    assert next_state.player.position == state.route[1]


def test_pellets_are_collected_and_increase_score():
    maze = generate_maze(seed=21)
    pellets = _pellets(maze)
    state = create_game(maze, pellets, ghost_count=0)
    for _ in range(len(state.route) - 1):
        state = advance_game(state, pellets)
    assert state.player.score == len(pellets)
    assert len(state.collected) == len(pellets)


def test_ghost_patrol_is_deterministic_and_does_not_block_player():
    maze = generate_maze(seed=8)
    pellets = _pellets(maze)
    first = create_game(maze, pellets, ghost_count=2)
    second = create_game(maze, pellets, ghost_count=2)
    assert first.ghosts == second.ghosts
    for _ in range(3):
        first = advance_game(first, pellets)
        second = advance_game(second, pellets)
    assert first.ghosts == second.ghosts
    assert first.player.position == second.player.position


def test_run_reaches_exit_after_collecting_every_pellet():
    maze = generate_maze(seed=42)
    pellets = _pellets(maze)
    final = run_to_completion(create_game(maze, pellets), pellets)
    assert final.complete
    assert final.player.position == maze.exit
    assert len(final.collected) == len(pellets)


def test_zero_ghosts_and_negative_ghost_count():
    maze = generate_maze(seed=3)
    assert create_game(maze, ghost_count=0).ghosts == ()
    try:
        create_game(maze, ghost_count=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative ghost count should be rejected")
