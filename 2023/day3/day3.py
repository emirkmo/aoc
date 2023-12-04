from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import numpy as np


class Offsets(Enum):
    up = 1, 0
    down = -1, 0
    left = 0, -1
    right = 0, 1
    up_left = 1, -1
    up_right = 1, 1
    down_left = -1, -1
    down_right = -1, 1

class LeftRightOffsets(Enum):
    left = 0, -1
    right = 0, 1


@dataclass
class PartNumber:
    x: int
    y: int
    connected: bool
    number: int
    length: int

@dataclass
class Schematic:
    rows: int
    cols: int
    array: np.ndarray
    visited: set[tuple[int, int]] = field(default_factory=set)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    @staticmethod
    def is_symbol(val: str) -> bool:
        return val != '.' and not val.isdigit()

    def get_neighbors(self):
        """Create a dictionary of nodes with their neighbors."""
        parts: list[PartNumber] = []
        was_digit = False
        numbers = []
        number_connection_status = []
        connected = False
        for row in range(self.rows):
            if was_digit:
                part = PartNumber(row, -1, any(number_connection_status), int("".join(numbers)), len(numbers))
                parts.append(part)
            was_digit = False
            numbers = []
            number_connection_status = []
            connected = False
            for col in range(self.cols):
                val: str = self.array[row][col]
                # print(row,col,val)
                # print(numbers)
                if not val.isdigit():
                    if was_digit: # previous value was a digit
                        part = PartNumber(row, col, any(number_connection_status), int("".join(numbers)), len(numbers))
                        parts.append(part)
                        # reset
                        numbers = []
                        was_digit = False
                        number_connection_status = []
                    continue

                # Get connected status
                connected = False
                for direction in Offsets:  # type: ignore
                    row_offset, col_offset = direction.value
                    new_row, new_col = row + row_offset, col + col_offset
                    if not self.in_bounds(new_row, new_col):
                        continue

                    new_val: str = self.array[new_row][new_col]
                    if self.is_symbol(new_val):
                        connected = True
                number_connection_status.append(connected)

                numbers.append(val)
                was_digit = True


        return parts

    def pass_base_conditions(self, row: int, col: int) -> bool:
        """Check if the node is in bounds and is a number node."""
        return self.in_bounds(row, col) and self.array[row][col].isdigit() and (row, col) not in self.visited

    def visit(self, row: int, col: int) -> None:
        """Mark a node as visited."""
        self.visited.add((row, col))

    def get_gear_ratio(self) -> int:
        strategy = BreadthFirstStrategy()
        ratios = 0
        for row in range(self.rows):
            for col in range(self.cols):
                val: str = self.array[row][col]
                if val != "*": # not a gear
                    continue

                numbers: list[int] = []
                for direction in Offsets:
                    row_offset, col_offset = direction.value
                    new_row, new_col = row + row_offset, col + col_offset
                    if not self.in_bounds(new_row, new_col):
                        continue

                    if (new_row, new_col) in self.visited:
                        continue

                    new_val: str = self.array[new_row][new_col]
                    if new_val.isdigit(): # unvisited number, breadt first explore it.
                        number = strategy.explore(self, new_row, new_col)
                        # print(number)
                        numbers.append(number)
                # if numbers: print(numbers)

                # print("NUMBERS!\n\n")
                # print(numbers)
                if len(numbers) == 2: # gear ratio time!
                    ratio = numbers[0] * numbers[1]
                    ratios += ratio
                    self.visited.clear() # clear visited for next gear ratio

        return ratios


class BreadthFirstStrategy:
    directions = LeftRightOffsets

    def get_neighbors(self, state: Schematic, row: int, col: int) -> list[tuple[int, int]]:

        neighbors = []
        for direction in self.directions:  # type: ignore
            row_offset, col_offset = direction.value
            new_row, new_col = row + row_offset, col + col_offset
            if state.pass_base_conditions(new_row, new_col):
                neighbors.append((new_row, new_col))

        return neighbors

    def explore(self, state: Schematic, row: int, col: int) -> int:
        """Iterative breadth first graph traversal with size."""
        number: dict[int, str] = {}
        if not state.pass_base_conditions(row, col):
            raise ValueError("Invalid start state.")
            # numbers = list(dict(sorted(number.items())).values())
            # return int("".join(numbers))

        # We're on a node, visit it, and increment.
        state.visit(row, col)
        number[col] = state.array[row][col]
        queue = [(row, col)]
        while len(queue) > 0:
            current_row, current_col = queue.pop(0)
            #print(queue, current_row, current_col)
            neighbors = self.get_neighbors(state, current_row, current_col)
            for neighbor_row, neighbor_col in neighbors:
                queue.append((neighbor_row, neighbor_col))
                state.visit(neighbor_row, neighbor_col)
                number[neighbor_col] = state.array[neighbor_row][neighbor_col]

        numbers = list(dict(sorted(number.items())).values())
        # print(number, numbers, int("".join(numbers)))
        return int("".join(numbers))

def main():

    with open(Path(__file__).parent.absolute()/"input.txt") as f:
        lines = f.readlines()

    schematic_array = np.array([l for line in lines for l in line if l!= '\n']).reshape((140,140))

    schematic = Schematic(schematic_array.shape[0], schematic_array.shape[1], schematic_array)

    parts = schematic.get_neighbors()


    print(f"Part1, total_part_numbers={sum([p.number for p in parts if p.connected])}")

    print(f"Part2: total_gear_ratios={schematic.get_gear_ratio()}")

if __name__ == "__main__":
    main()
