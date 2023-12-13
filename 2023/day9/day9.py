import numpy as np
from aocd.models import Puzzle
from numpy.typing import NDArray

puzzle = Puzzle(2023, 9)
lines = puzzle.input_data.split("\n")

def get_array_from_line(line: str) -> NDArray[np.int64]:
    return np.array(line.split()).astype(int)

def fill_in_last_from_zero_diff(a: NDArray[np.int64]) -> int:
    last_vals: list[int] = [a[-1]]
    while not np.all(a == 0):
        a = np.diff(a)
        last_vals.append(a[-1])
    return sum(last_vals)

def get_extrapolated_first(first_vals: list[int]) -> int:
    curr_val = first_vals.pop()
    while len(first_vals) > 0:
        next_val = first_vals.pop()
        curr_val = next_val - curr_val
    return curr_val

def fill_in_first_from_zero_diff(a: NDArray[np.int64]) -> int:
    first_vals: list[int] = [a[0]]
    while not np.all(a == 0):
        a = np.diff(a)
        first_vals.append(a[0])
    return get_extrapolated_first(first_vals)

history_sum = 0
first_sum = 0
for line in lines:
    a = get_array_from_line(line)
    history_sum += fill_in_last_from_zero_diff(a)
    first_sum += fill_in_first_from_zero_diff(a)
history_sum, first_sum

puzzle.answer_a = history_sum
puzzle.answer_b = first_sum
