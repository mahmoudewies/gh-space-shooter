"""Classic arcade maze engine powered by GitHub contribution activity."""

from .activity import EnergyPellet, build_energy_pellets
from .entities import Ghost, Player
from .generator import Maze, generate_maze
from .pathfinding import find_path, reachable_cells
from .scene import GameState, advance_game, create_game, run_to_completion

__all__ = [
    "EnergyPellet",
    "GameState",
    "Ghost",
    "Maze",
    "Player",
    "advance_game",
    "build_energy_pellets",
    "create_game",
    "find_path",
    "generate_maze",
    "reachable_cells",
    "run_to_completion",
]
