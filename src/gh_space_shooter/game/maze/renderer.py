"""Pixel-art renderer for the Cyberpunk Purple NEON MAZE animation."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

from .activity import EnergyPellet
from .generator import Maze
from .scene import GameState, advance_game, create_game

# Cyberpunk Purple palette
BG = (9, 5, 17)
PANEL = (17, 13, 34)
GRID = (29, 22, 54)
WALL = (42, 27, 83)
WALL_EDGE = (109, 74, 255)
LAVENDER = (185, 162, 255)
MAGENTA = (232, 121, 249)
WHITE = (238, 233, 255)
MUTED = (125, 112, 160)
GHOST_COLORS = ((232, 121, 249), (92, 221, 255), (255, 105, 160))


def _font(size: int = 12) -> ImageFont.ImageFont:
    """Use Pillow's bundled bitmap font for portable rendering."""
    return ImageFont.load_default(size=size)


def _glow(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int,
          color: tuple[int, int, int], layers: int = 3) -> None:
    x, y = center
    for layer in range(layers, 0, -1):
        r = radius + layer * 3
        alpha_color = tuple(int(channel * (0.12 + 0.08 * layer)) for channel in color)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=alpha_color)
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)


def _draw_player(draw: ImageDraw.ImageDraw, center: tuple[int, int], size: int,
                 frame: int) -> None:
    """Draw a tiny pixel-art explorer with an animated energy core."""
    x, y = center
    s = max(2, size // 8)
    # Helmet and body are deliberately blocky to preserve the arcade look.
    draw.rectangle((x-2*s, y-3*s, x+2*s, y+s), fill=LAVENDER)
    draw.rectangle((x-s, y-2*s, x+s, y-s), fill=BG)
    draw.rectangle((x-2*s, y+s, x+2*s, y+3*s), fill=MAGENTA)
    draw.rectangle((x-3*s, y, x-s, y+2*s), fill=LAVENDER)
    draw.rectangle((x+s, y, x+3*s, y+2*s), fill=LAVENDER)
    leg_offset = (frame % 2) * s
    draw.rectangle((x-2*s, y+3*s, x-s, y+4*s+leg_offset), fill=WHITE)
    draw.rectangle((x+s, y+3*s, x+2*s, y+4*s+(s-leg_offset)), fill=WHITE)
    _glow(draw, (x, y), max(2, s), MAGENTA, layers=1)


def _draw_ghost(draw: ImageDraw.ImageDraw, center: tuple[int, int], size: int,
                color: tuple[int, int, int], frame: int) -> None:
    x, y = center
    r = max(4, size // 3)
    draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
    draw.rectangle((x-r, y, x+r, y+r//2), fill=color)
    wave = frame % 2
    for index in range(3):
        left = x-r + index * (2*r//3)
        offset = wave * 2 if index % 2 == 0 else 0
        draw.polygon(
            [(left, y+r//2), (left+2*r//3, y+r//2),
             (left+r//3, y+r+offset)],
            fill=color,
        )
    eye_y = y-r//4
    for eye_x in (x-r//3, x+r//3):
        draw.ellipse((eye_x-2, eye_y-2, eye_x+2, eye_y+2), fill=WHITE)
        draw.point((eye_x, eye_y), fill=BG)


def _draw_scene(maze: Maze, pellets: tuple[EnergyPellet, ...],
                state: GameState, frame_index: int, tile: int,
                header_height: int, footer_height: int) -> Image.Image:
    margin = 20
    width = maze.width * tile + margin * 2
    height = maze.height * tile + header_height + footer_height + margin
    image = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(image)

    # Subtle terminal grid and HUD panels.
    for x in range(0, width, 16):
        draw.line((x, 0, x, height), fill=(14, 10, 27))
    for y in range(0, height, 16):
        draw.line((0, y, width, y), fill=(14, 10, 27))
    draw.rounded_rectangle((12, 10, width-12, header_height-4), radius=8, fill=PANEL,
                           outline=GRID, width=1)
    draw.text((24, 17), "NEON MAZE", font=_font(16), fill=LAVENDER)
    draw.text((width-156, 20), "ARCADE // 01", font=_font(11), fill=MAGENTA)

    origin_x, origin_y = margin, header_height
    for y, row in enumerate(maze.cells):
        for x, is_wall in enumerate(row):
            x0, y0 = origin_x + x*tile, origin_y + y*tile
            if is_wall:
                draw.rectangle((x0, y0, x0+tile-1, y0+tile-1), fill=WALL)
                draw.rectangle((x0, y0, x0+tile-1, y0+2), fill=WALL_EDGE)
                draw.rectangle((x0, y0, x0+2, y0+tile-1), fill=(75, 48, 145))
            else:
                draw.rectangle((x0, y0, x0+tile-1, y0+tile-1), fill=(13, 9, 25))

    pellet_map = {pellet.position: pellet for pellet in pellets}
    for position, pellet in pellet_map.items():
        if position in state.collected:
            continue
        px = origin_x + position[0]*tile + tile//2
        py = origin_y + position[1]*tile + tile//2
        radius = 2 + min(2, pellet.intensity//2)
        _glow(draw, (px, py), radius, MAGENTA if pellet.intensity >= 3 else LAVENDER, 2)

    # Exit portal pulses between lavender and magenta.
    ex, ey = maze.exit
    portal_center = (origin_x + ex*tile + tile//2, origin_y + ey*tile + tile//2)
    portal_color = MAGENTA if frame_index % 2 else LAVENDER
    _glow(draw, portal_center, max(4, tile//3), portal_color, 3)
    draw.ellipse((portal_center[0]-tile//3, portal_center[1]-tile//3,
                  portal_center[0]+tile//3, portal_center[1]+tile//3),
                 outline=WHITE, width=2)

    for index, ghost in enumerate(state.ghosts):
        gx, gy = ghost.position
        center = (origin_x + gx*tile + tile//2, origin_y + gy*tile + tile//2)
        _draw_ghost(draw, center, tile, GHOST_COLORS[index % len(GHOST_COLORS)], frame_index)

    px, py = state.player.position
    player_center = (origin_x + px*tile + tile//2, origin_y + py*tile + tile//2)
    _draw_player(draw, player_center, tile, frame_index)

    footer_y = origin_y + maze.height*tile + 8
    draw.rounded_rectangle((12, footer_y, width-12, height-10), radius=8,
                           fill=PANEL, outline=GRID, width=1)
    draw.text((24, footer_y+8), f"ENERGY  {state.player.score:02d}", font=_font(12), fill=WHITE)
    draw.text((width//2-34, footer_y+8), f"TICK  {state.tick:03d}",
              font=_font(12), fill=LAVENDER)
    status = "GATE UNLOCKED" if state.complete else "COLLECT ENERGY // FIND THE EXIT"
    draw.text((width-190, footer_y+8), status, font=_font(10),
              fill=MAGENTA if state.complete else MUTED)
    return image


def render_neon_maze(
    maze: Maze,
    pellets: Iterable[EnergyPellet] = (),
    output_path: str | Path = "game.gif",
    *,
    ghost_count: int = 2,
    tile_size: int = 20,
    frames_per_step: int = 2,
    frame_duration_ms: int = 90,
    max_frames: int = 180,
) -> Path:
    """Render a complete maze run as an optimized animated GIF.

    The player follows the deterministic route, collecting all supplied
    pellets before reaching the exit. Rendering is deterministic and offline.
    """
    if tile_size < 12:
        raise ValueError("tile_size must be at least 12 pixels")
    if frames_per_step < 1 or frame_duration_ms < 20 or max_frames < 2:
        raise ValueError("Invalid animation timing or frame limit")

    pellet_tuple = tuple(pellets)
    state = create_game(maze, pellet_tuple, ghost_count=ghost_count)
    frames: list[Image.Image] = []
    header_height, footer_height = 44, 38

    def capture(snapshot: GameState, index: int) -> None:
        frames.append(
            _draw_scene(maze, pellet_tuple, snapshot, index, tile_size,
                        header_height, footer_height).convert("P", palette=Image.Palette.ADAPTIVE)
        )

    capture(state, 0)
    frame_index = 1
    while not state.complete and len(frames) < max_frames:
        state = advance_game(state, pellet_tuple)
        for _ in range(frames_per_step):
            if len(frames) >= max_frames:
                break
            capture(state, frame_index)
            frame_index += 1

    if not state.complete:
        # Preserve a truthful end state: do not pretend a truncated run won.
        raise ValueError(
            f"Animation exceeded max_frames={max_frames}; increase max_frames "
            f"(route requires {len(state.route)} movement steps)."
        )

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        destination,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )
    return destination
