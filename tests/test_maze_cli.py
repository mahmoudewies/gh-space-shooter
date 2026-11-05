"""CLI-level integration test for rendering from offline contribution data."""

import json

from PIL import Image

from gh_space_shooter.cli import _generate_maze_output


def test_maze_output_uses_offline_contribution_payload(tmp_path):
    payload = {
        "username": "mahmoudewies",
        "total_contributions": 20,
        "weeks": [{
            "days": [
                {"date": "2026-11-01", "count": 4, "level": 2},
                {"date": "2026-11-02", "count": 7, "level": 3},
                {"date": "2026-11-03", "count": 0, "level": 0},
            ]
        }],
    }
    fixture = tmp_path / "contributions.json"
    fixture.write_text(json.dumps(payload), encoding="utf-8")
    loaded = json.loads(fixture.read_text(encoding="utf-8"))
    output = tmp_path / "neon-maze.gif"

    _generate_maze_output(loaded, str(output))

    assert output.exists()
    with Image.open(output) as gif:
        assert gif.format == "GIF"
        assert gif.is_animated
