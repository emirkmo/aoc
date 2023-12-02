from dataclasses import dataclass

from more_itertools import chunked  # itertools.batched in python 3.12


@dataclass
class Cube:
    color: str
    number: int
    max: int

    def __repr__(self):
        return f"{self.color} {self.number}"

max_cubes = {"red": 12, "green": 13, "blue": 14}

def ensure_game_validity(number: int, color: str) -> bool:
    if color not in max_cubes:
        return False
    if int(number) > max_cubes[color]:
        return False
    return True




with open("example_input.txt") as f:
    lines = f.readlines()

powers_total = 0
id_total = 0
for line in lines:
    if not line:
        continue
    game_id, games = line.split(":", 1)
    game_id = game_id.split()[1]
    games = games.split(";")
    invalid_game = False
    cubes = {"red": 0, "green": 0, "blue": 0}
    for game in games:
        numbers_cubes = game.split()

        batched_list = chunked(numbers_cubes, 2)
        for batch in batched_list:
            number = int(batch[0])
            color = batch[1]
            color = color.replace(",","").strip()
            if number > cubes[color]:
                cubes[color] = number

            valid_game = ensure_game_validity(number, color)
            if not valid_game:
                invalid_game = True


    power = 1
    for max_color in cubes.values():
        power *= max_color
    powers_total += power

    if not invalid_game:
        id_total += int(game_id)

print(powers_total)
print(id_total)