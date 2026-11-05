# 💜 NEON MAZE — Mahmoud Ewis

<p align="center">
  <strong>CONTRIBUTIONS POWER THE MAZE.</strong><br/>
  A classic top-down pixel-art arcade animation in a Cyberpunk Purple world.
</p>

<p align="center">
  <code>#090511</code> · <code>#6D4AFF</code> · <code>#B9A2FF</code> · <code>#E879F9</code>
</p>

## The concept

NEON MAZE transforms the public contribution calendar of a GitHub account into an auto-play arcade run. A tiny pixel explorer travels through a procedurally generated maze, collects energy pellets inspired by active contribution days, passes patrolling ghosts, and reaches the exit.

The maze layout is generated independently from contribution activity, so every route remains connected and completable. Contribution data affects collectible placement and intensity—not walls or private repository details.

## Generate the animation

Requires Python 3.12+.

```bash
git clone https://github.com/mahmoudewies/gh-space-shooter.git
cd gh-space-shooter
pip install ".[dev]"
```

Create a GitHub token with `read:user` permission and expose it as `GH_TOKEN`. Never commit the token.

**Windows PowerShell**
```powershell
$env:GH_TOKEN="your_token"
gh-space-shooter mahmoudewies --game maze --output assets/neon-maze.gif
```

**Linux / macOS**
```bash
export GH_TOKEN="your_token"
gh-space-shooter mahmoudewies --game maze --output assets/neon-maze.gif
```

### Offline generation

Use the included sample contribution calendar without making an API request:

```bash
gh-space-shooter mahmoudewies --game maze --raw-input tests/fixtures/neon-maze-contributions.json --output assets/neon-maze.gif
```

### Existing shooter mode

The original contribution shooter remains available:

```bash
gh-space-shooter mahmoudewies --game shooter --output game.gif
```

## Automatic updates

The workflow `.github/workflows/update-game.yml` is scheduled daily and can be started manually from the repository's **Actions** tab.

Before using it, add a repository Actions secret named `GH_TOKEN` containing a token with `read:user` permission. The workflow uses `GITHUB_TOKEN` only for committing the generated asset and does not rely on it to read the contribution calendar.

## Architecture

- **Maze engine:** deterministic randomized DFS + BFS route validation.
- **Gameplay:** immutable game states, automatic player route, pellet collection, decorative ghost patrol.
- **Renderer:** Pillow pixel-art frames, neon glow, HUD, and optimized animated GIF.
- **Data:** GitHub GraphQL contribution calendar; aggregate dates/counts/levels only.
- **Automation:** GitHub Actions with `contents: write` for the generated asset commit.

## Credits

Built on the original [gh-space-shooter](https://github.com/czl9707/gh-space-shooter) project by [@czl9707](https://github.com/czl9707). The original shooter mode and MIT license are preserved while NEON MAZE is developed as a separate game module.

---

<p align="center"><sub>BUILT WITH PYTHON · PILLOW · GITHUB GRAPHQL · GITHUB ACTIONS</sub></p>
