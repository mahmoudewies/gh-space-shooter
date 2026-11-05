# 💜 Mahmoud's Purple Space Shooter

<p align="center">
  <img src="game.gif" alt="Mahmoud's GitHub contribution space shooter" width="100%" />
</p>

<p align="center">
  <strong>MY CONTRIBUTIONS. MY BATTLEFIELD.</strong><br/>
  A cyberpunk-purple Galaga-style animation generated from my GitHub contribution graph.
</p>

<p align="center">
  <code>#090511</code> · <code>#6D4AFF</code> · <code>#B9A2FF</code> · <code>#E879F9</code>
</p>

## How it works

Every contribution cell becomes an enemy. The original game engine maps contribution activity to enemy strength, then animates a ship clearing the grid with projectiles, particle effects, and a moving starfield.

This fork preserves the original gameplay and contribution mapping while applying a custom purple palette inside the renderer. The colors are part of the generated frames, not a post-processing tint.

## Automatic updates

The GitHub Actions workflow at `.github/workflows/update-game.yml` is intended to regenerate `game.gif` daily and can also be started manually from the **Actions** tab. It installs this fork so the customized renderer is used.

## Run locally

Requires Python 3.12+.

```bash
git clone https://github.com/mahmoudewies/gh-space-shooter.git
cd gh-space-shooter
pip install .
```

Set a GitHub token with `read:user` permission, then run:

```bash
# Linux / macOS
export GH_TOKEN="your_token"
gh-space-shooter mahmoudewies --output game.gif --strategy random

# Windows PowerShell
$env:GH_TOKEN="your_token"
gh-space-shooter mahmoudewies --output game.gif --strategy random
```

## Credits

Built on the original [gh-space-shooter](https://github.com/czl9707/gh-space-shooter) project by [@czl9707](https://github.com/czl9707). This fork preserves the original MIT license and adapts its rendering palette and profile presentation.

---

<p align="center"><sub>BUILT WITH PYTHON · PILLOW · GITHUB ACTIONS</sub></p>
