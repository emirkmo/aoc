from pathlib import Path

from aocd.models import Puzzle

day = int(Path(__file__).stem.replace("day", ""))

puzzle = Puzzle(2023, day)
lines = puzzle.input_data.split("\n")

# part 1
#puzzle.answer_a =
# part 2
# puzzle.answer_b =
