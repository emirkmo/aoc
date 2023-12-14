from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Literal

import numpy as np
from aocd.models import Puzzle
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.prepared import prep

day = int(Path(__file__).absolute().stem.replace("day", ""))

puzzle = Puzzle(2023, day)
lines = puzzle.input_data.split("\n")


class Cardinal(Enum):
    up = -1, 0
    down = 1, 0
    left = 0, -1
    right = 0, 1


class Offsets(Enum):
    up = 1, 0
    down = -1, 0
    left = 0, -1
    right = 0, 1
    up_left = 1, -1
    up_right = 1, 1
    down_left = -1, -1
    down_right = -1, 1


SYMBOL = Literal["|", "-", "L", "J", "7", "F"]

pipe_offsets: dict[SYMBOL, dict[Cardinal, Offsets]] = {
    "|": {Cardinal.up: Offsets.up, Cardinal.down: Offsets.down},  # up, down
    "-": {Cardinal.right: Offsets.right, Cardinal.left: Offsets.left},  # right, left
    "L": {
        Cardinal.left: Offsets.up_left,
        Cardinal.down: Offsets.down_right,
    },  # left up, down right
    "J": {
        Cardinal.down: Offsets.down_left,
        Cardinal.right: Offsets.up_right,
    },  # down left, right up
    "7": {
        Cardinal.right: Offsets.down_right,
        Cardinal.up: Offsets.up_left,
    },  # right down, up left
    "F": {
        Cardinal.up: Offsets.up_right,
        Cardinal.left: Offsets.down_left,
    },  # up right, left, down
}

pipe_headings: dict[SYMBOL, dict[Cardinal, Cardinal]] = {
    "|": {Cardinal.up: Cardinal.up, Cardinal.down: Cardinal.down},
    "-": {Cardinal.left: Cardinal.left, Cardinal.right: Cardinal.right},
    "L": {Cardinal.down: Cardinal.right, Cardinal.left: Cardinal.up},
    "J": {Cardinal.down: Cardinal.left, Cardinal.right: Cardinal.up},
    "7": {Cardinal.up: Cardinal.left, Cardinal.right: Cardinal.down},
    "F": {Cardinal.up: Cardinal.right, Cardinal.left: Cardinal.down},
}


@dataclass
class Node:
    row: int
    col: int
    symbol: SYMBOL
    heading_map: dict[Cardinal, Cardinal] = field(init=False)

    def __post_init__(self):
        self.heading_map = pipe_headings[self.symbol]

    def traverse(self, incoming_direction: Cardinal) -> Cardinal:
        """Tarverse in a given heading and return the next row,col and heading"""
        # heading = pipe_headings[self.symbol][incoming_direction]
        # offset = pipe_offsets[self.symbol][incoming_direction]
        return self.heading_map[incoming_direction]
        # return offset, heading


def get_starting_node() -> tuple[int, int]:
    for row, line in enumerate(lines):
        if "S" in line:
            col = line.index("S")
            return row, col
    raise ValueError("No starting node found")


def find_starting_pipe(network) -> tuple[Node, Cardinal]:
    """Find the starting pipe"""
    row, col = get_starting_node()
    for direction in Cardinal:
        new_row = row + direction.value[0]
        new_col = col + direction.value[1]
        symbol = network[new_row, new_col]
        if symbol == ".":
            continue
        node = Node(new_row, new_col, network[new_row, new_col])
        try:
            out_direction = node.traverse(direction)
            return node, out_direction
        except KeyError:
            continue
    raise ValueError("No starting pipe found")


# np.array(lines)

drawing = np.array([val for line in lines for val in line if val != "\n"]).reshape(
    (len(lines), len(lines[0]))
)


def find_traversed(drawing):
    current_node, heading = find_starting_pipe(drawing)
    symbol = current_node.symbol
    traversed = 1

    while symbol != "S":
        new_row = current_node.row + heading.value[0]
        new_col = current_node.col + heading.value[1]
        symbol = drawing[new_row, new_col]
        if symbol == "S":
            break
        current_node = Node(new_row, new_col, symbol)
        heading = current_node.traverse(heading)
        traversed += 1

    return traversed // 2 + traversed % 2


puzzle.answer_a = find_traversed(drawing)


def draw_polygon_from_path(drawing) -> Polygon:
    current_node, heading = find_starting_pipe(drawing)
    symbol = current_node.symbol
    traversed = 1
    path = [(current_node.row, current_node.col)]

    while symbol != "S":
        new_row = current_node.row + heading.value[0]
        new_col = current_node.col + heading.value[1]
        symbol = drawing[new_row, new_col]
        path.append((new_row, new_col))
        if symbol == "S":
            break
        current_node = Node(new_row, new_col, symbol)
        heading = current_node.traverse(heading)
        traversed += 1

    return Polygon(np.array(path))


def prepare_polygon_and_points(drawing):
    poly = draw_polygon_from_path(drawing)
    x, y = np.meshgrid(np.arange(drawing.shape[0]), np.arange(drawing.shape[1]))
    points = np.vstack((x.flatten(), y.flatten())).T
    points = np.apply_along_axis(Point, 1, points)
    return prep(poly), points


prep_poly, points = prepare_polygon_and_points(drawing)
points_inside = np.apply_along_axis(prep_poly.contains, 0, points).sum()
puzzle.answer_b = points_inside
