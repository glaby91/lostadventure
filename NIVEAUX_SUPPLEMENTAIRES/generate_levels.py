#!/usr/bin/env python3
"""Create playable LostAdventure LAB tables and CPC character-mode previews.

The generated maps use 40x25 decimal cells, just like the existing .LAB files.
Walls are 1, food is 2, and the exit tile is 3 (see laby.asm).  All corridors,
food and the exit are connected to the central start chamber.
"""

from __future__ import annotations

import csv
import random
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
TABLES = OUT / "tables"
IMAGES = OUT / "images"
EXISTING_IMAGES = IMAGES / "existants"
NEW_IMAGES = IMAGES / "nouveaux"

WIDTH, HEIGHT = 40, 25
SCALE = 2
COLORS = {
    "background": (0, 0, 0),
    "wall": (99, 0, 247),
    "food": (1, 247, 0),
    "door": (159, 65, 159),
    "heart": (247, 239, 0),
}
GLYPHS = {
    143: [255, 255, 255, 255, 255, 255, 255, 255],
    231: [0, 60, 126, 255, 255, 126, 60, 0],
    207: [170, 85, 170, 85, 170, 85, 170, 85],
    244: [0, 0, 24, 60, 126, 255, 255, 0],
    245: [0, 0, 255, 255, 126, 60, 24, 0],
    246: [128, 224, 248, 254, 248, 224, 128, 0],
    247: [2, 14, 62, 254, 62, 14, 2, 0],
    228: [108, 254, 254, 254, 124, 56, 16, 0],
}
CELL_TO_GLYPH = {
    1: (143, "wall"),
    2: (231, "food"),
    3: (207, "door"),
    4: (244, "wall"),
    5: (245, "wall"),
    6: (246, "wall"),
    7: (247, "wall"),
    8: (228, "heart"),
}


def load_lab(path: Path) -> list[int]:
    values: list[int] = []
    for item in path.read_bytes().decode("latin1").split():
        try:
            values.append(int(item))
        except ValueError:
            break
        if len(values) == WIDTH * HEIGHT:
            break
    if len(values) != WIDTH * HEIGHT:
        raise ValueError(f"{path}: expected 1000 cells, found {len(values)}")
    if any(value not in CELL_TO_GLYPH and value != 0 for value in values):
        raise ValueError(f"{path}: unsupported cell values")
    return values


def save_lab(path: Path, values: list[int]) -> None:
    if len(values) != WIDTH * HEIGHT:
        raise ValueError("A LAB table must contain exactly 1000 cells")
    path.write_bytes(("\r\n".join(map(str, values)) + "\r\n").encode("ascii"))


def draw_cell(pixels, x: int, y: int, glyph_id: int, color_name: str) -> None:
    color = COLORS[color_name]
    for gy, row in enumerate(GLYPHS[glyph_id]):
        for gx in range(8):
            if row & (0x80 >> gx):
                for dy in range(SCALE):
                    for dx in range(SCALE):
                        pixels[x * 8 * SCALE + gx * SCALE + dx,
                               y * 8 * SCALE + gy * SCALE + dy] = color


def render(values: list[int], target: Path) -> None:
    image = Image.new("RGB", (WIDTH * 8 * SCALE, HEIGHT * 8 * SCALE), COLORS["background"])
    pixels = image.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            tile = values[y * WIDTH + x]
            if tile in CELL_TO_GLYPH:
                glyph_id, color_name = CELL_TO_GLYPH[tile]
                draw_cell(pixels, x, y, glyph_id, color_name)
    # laby.asm's COIN1 draws a character-143 frame over the map perimeter.
    for x in range(WIDTH):
        draw_cell(pixels, x, 0, 143, "wall")
        draw_cell(pixels, x, HEIGHT - 1, 143, "wall")
    for y in range(HEIGHT):
        draw_cell(pixels, 0, y, 143, "wall")
        draw_cell(pixels, WIDTH - 1, y, 143, "wall")
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, optimize=True)


def bfs(values: list[int], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    distances = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
                continue
            if values[ny * WIDTH + nx] == 1:
                continue
            if (nx, ny) not in distances:
                distances[(nx, ny)] = distances[(x, y)] + 1
                queue.append((nx, ny))
    return distances


def make_maze(seed: int) -> tuple[list[int], int, int]:
    """Make a perfect maze rooted in a small central spawn chamber."""
    rng = random.Random(seed)
    values = [1] * (WIDTH * HEIGHT)
    # 19 by 12 odd-coordinate junctions fill the 40x25 interior.
    nodes = [(1 + 2 * x, 1 + 2 * y) for y in range(12) for x in range(19)]
    node_set = set(nodes)
    root = (19, 11)  # near the screen centre, matching the game start area
    seen = {root}
    stack = [root]
    values[root[1] * WIDTH + root[0]] = 0
    while stack:
        x, y = stack[-1]
        options = [(x + dx * 2, y + dy * 2) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        options = [p for p in options if p in node_set and p not in seen]
        if not options:
            stack.pop()
            continue
        nx, ny = rng.choice(options)
        seen.add((nx, ny))
        values[((y + ny) // 2) * WIDTH + ((x + nx) // 2)] = 0
        values[ny * WIDTH + nx] = 0
        stack.append((nx, ny))

    # A 3x3 room leaves likely BASIC/LOCATE start coordinates open and connected.
    for y in range(10, 13):
        for x in range(18, 21):
            values[y * WIDTH + x] = 0

    distances = bfs(values, root)
    exit_xy = max(
        (p for p in nodes if p != root),
        key=lambda p: (distances.get(p, -1), -(p[1] * WIDTH + p[0])),
    )
    exit_distance = distances[exit_xy]
    values[exit_xy[1] * WIDTH + exit_xy[0]] = 3

    # Count dead-end junctions as a second challenge measure.
    dead_ends = 0
    for x, y in nodes:
        degree = sum(
            values[ny * WIDTH + nx] != 1
            for nx, ny in ((x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2))
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT
        )
        if degree == 1:
            dead_ends += 1
    return values, exit_distance, dead_ends


def choose_mazes(count: int = 50) -> list[tuple[list[int], int, int]]:
    candidates = []
    seen = set()
    for seed in range(50000, 68000):
        maze = make_maze(seed)
        key = bytes(maze[0])
        if key in seen:
            continue
        seen.add(key)
        candidates.append(maze)
    candidates.sort(key=lambda item: (item[1], item[2], bytes(item[0])))
    selected = []
    for i in range(count):
        index = round((i + 1) * (len(candidates) - 1) / (count + 1))
        selected.append(candidates[index])
    return selected


def add_food(values: list[int], level: int, rng: random.Random) -> int:
    start = (19, 11)
    distances = bfs(values, start)
    # All dots are placed on open, reachable corridors, with more dots later.
    food_count = min(5 + (level - 11) // 3, 21)
    candidates = [
        (x, y) for y in range(1, HEIGHT - 1) for x in range(1, WIDTH - 1)
        if values[y * WIDTH + x] == 0 and (x, y) in distances
        and abs(x - 19) + abs(y - 11) > 2
    ]
    candidates.sort(key=lambda p: (distances[p], p[1], p[0]))
    picks = []
    # Stratified placement sends food to near, middle and remote parts of the maze.
    for i in range(food_count):
        pos = round((i + 1) * (len(candidates) - 1) / (food_count + 1))
        picks.append(candidates[pos])
    # Break any positional ties while keeping one dot per corridor cell.
    picks = list(dict.fromkeys(picks))
    if len(picks) < food_count:
        remainder = [p for p in candidates if p not in picks]
        rng.shuffle(remainder)
        picks.extend(remainder[:food_count - len(picks)])
    for x, y in picks:
        values[y * WIDTH + x] = 2
    return len(picks)


def make_contact_sheet(entries: list[tuple[str, Path]], target: Path, columns: int) -> None:
    thumb_w, thumb_h = 160, 100
    cell_w, cell_h = 176, 126
    rows = (len(entries) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), (15, 19, 27))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for i, (label, path) in enumerate(entries):
        x, y = (i % columns) * cell_w + 8, (i // columns) * cell_h + 8
        thumb = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.NEAREST)
        sheet.paste(thumb, (x, y))
        draw.text((x, y + thumb_h + 5), label, fill=(235, 240, 250), font=font)
    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target, optimize=True)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    EXISTING_IMAGES.mkdir(parents=True, exist_ok=True)
    NEW_IMAGES.mkdir(parents=True, exist_ok=True)
    image_index: list[tuple[str, Path]] = []
    with (OUT / "index.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerow(["niveau", "table", "miams", "distance_sortie_depuis_depart", "impasses", "validation"])
        for source in sorted(ROOT.glob("TABLE*.LAB"), key=lambda p: (p.stem != "TABLE", p.stem)):
            values = load_lab(source)
            target = EXISTING_IMAGES / f"{source.stem}.png"
            render(values, target)
            image_index.append((source.stem, target))
            writer.writerow(["existant", source.name, values.count(2), "", "", "1000 cases"])

        binary = (ROOT / "TABLE.BIN").read_bytes()
        if binary[:1] == b"\x00" and len(binary) >= 1128:
            start_values = list(binary[128:1128])
            if all(value in CELL_TO_GLYPH or value == 0 for value in start_values):
                start_png = EXISTING_IMAGES / "TABLE.BIN_depart.png"
                render(start_values, start_png)
                image_index.append(("TABLE.BIN départ", start_png))

        candidates = choose_mazes()
        for i, (values, distance, dead_ends) in enumerate(candidates, start=11):
            rng = random.Random(900000 + i)
            miams = add_food(values, i, rng)
            table = TABLES / f"TABLE{i}.LAB"
            image = NEW_IMAGES / f"TABLE{i}.png"
            save_lab(table, values)
            render(values, image)
            reachable = bfs(values, (19, 11))
            food_positions = [
                (idx % WIDTH, idx // WIDTH) for idx, value in enumerate(values) if value == 2
            ]
            if len(food_positions) != miams or any(p not in reachable for p in food_positions):
                raise AssertionError(f"TABLE{i}: unreachable Miam")
            if (next((idx % WIDTH, idx // WIDTH) for idx, value in enumerate(values) if value == 3)) not in reachable:
                raise AssertionError(f"TABLE{i}: unreachable exit")
            writer.writerow([i, table.name, miams, distance, dead_ends, "tous les Miam et la sortie accessibles"])
            image_index.append((f"Niveau {i}", image))

    make_contact_sheet(image_index[:len(list(ROOT.glob("TABLE*.LAB"))) + 1],
                       IMAGES / "apercu_tables_existantes.png", 4)
    make_contact_sheet(image_index[len(list(ROOT.glob("TABLE*.LAB"))) + 1:],
                       IMAGES / "apercu_50_nouveaux_niveaux.png", 5)
    print(f"Existing tables previewed; generated 50 new connected levels in {OUT}")


if __name__ == "__main__":
    main()
