"""Tests for the NEON MAZE pixel-art GIF renderer."""

from PIL import Image

from gh_space_shooter.game.maze import EnergyPellet, generate_maze
from gh_space_shooter.game.maze.renderer import render_neon_maze


def test_renderer_creates_animated_gif(tmp_path):
    maze = generate_maze(seed=12)
    pellets = [
        EnergyPellet((3, 1), 2, 3, "2026-01-01"),
        EnergyPellet((5, 3), 4, 9, "2026-01-02"),
    ]
    output = tmp_path / "neon-maze.gif"
    result = render_neon_maze(
        maze, pellets, output, ghost_count=2, frames_per_step=1,
        frame_duration_ms=80, max_frames=180,
    )
    assert result == output
    assert output.exists()
    with Image.open(output) as gif:
        assert gif.format == "GIF"
        assert gif.is_animated
        assert gif.n_frames > 1
        assert gif.size[0] > maze.width
        assert gif.size[1] > maze.height


def test_renderer_rejects_too_small_tiles(tmp_path):
    maze = generate_maze(seed=1)
    try:
        render_neon_maze(maze, output_path=tmp_path / "bad.gif", tile_size=8)
    except ValueError as error:
        assert "tile_size" in str(error)
    else:
        raise AssertionError("small tile size should be rejected")
