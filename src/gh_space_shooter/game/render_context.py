"""Rendering context for drawable objects."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class RenderContext:
    """Rendering configuration, including the Cyberpunk Purple palette."""

    cell_size: int
    cell_spacing: int
    padding: int
    background_color: Tuple[int, int, int]
    grid_color: Tuple[int, int, int]
    ship_color: Tuple[int, int, int]
    bullet_color: Tuple[int, int, int]
    enemy_colors: dict[int, Tuple[int, int, int]]

    def get_cell_position(self, x: float, y: float) -> tuple[float, float]:
        """Convert a contribution-grid coordinate to pixel coordinates."""
        return (
            self.padding + x * (self.cell_size + self.cell_spacing),
            self.padding + y * (self.cell_size + self.cell_spacing),
        )

    @staticmethod
    def darkmode() -> "RenderContext":
        """Cyberpunk-purple theme for the Mahmoud Ewis edition."""
        return RenderContext(
            cell_size=12,
            cell_spacing=3,
            padding=40,
            background_color=(9, 5, 17),       # #090511
            grid_color=(23, 19, 41),          # #171329
            enemy_colors={
                1: (59, 29, 117),             # Deep violet
                2: (109, 74, 255),            # #6D4AFF
                3: (154, 123, 255),            # Electric lavender
                4: (211, 197, 255),            # Light lavender
            },
            ship_color=(185, 162, 255),       # #B9A2FF
            bullet_color=(232, 121, 249),     # Neon magenta
        )
