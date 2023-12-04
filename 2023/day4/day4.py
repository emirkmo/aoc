from collections import deque
from pathlib import Path


def parse_cards(filename: str = "input.txt") -> list[list[str]]:
    with open(Path(__file__).parent.absolute() / "input.txt") as f:
        lines = f.readlines()

    lines = [line.split(":")[1].split("|") for line in lines]
    return lines


def get_winning_numbers(card: list[str]) -> set[int]:
    winning = {int(num.strip()) for num in card[0].split()}
    numbers = {int(num.strip()) for num in card[1].split()}
    return winning.intersection(numbers)


def get_total_points(card_lines: list[list[str]]) -> int:
    total_points = 0
    for card in card_lines:
        winning_numbers = get_winning_numbers(card)
        if winning_numbers:
            total_points += 2 ** (len(winning_numbers) - 1)
    return total_points


def pre_compute_wins(lines: list[list[str]]) -> dict[int, int]:
    winning_list: dict[int, int] = {}
    for i, card in enumerate(lines):
        winning = {int(num.strip()) for num in card[0].split()}
        numbers = {int(num.strip()) for num in card[1].split()}
        winning_numbers = winning.intersection(numbers)
        winning_list[i] = len(winning_numbers)
    return winning_list


def get_total_cards_won(n_cards: int, winning_cards: dict[int, int]) -> int:
    queue = deque()
    queue.extend(list(range(n_cards)))

    total_cards = 0
    while len(queue) > 0:
        card_num = queue.popleft()
        cards_won = winning_cards.get(card_num)
        if cards_won is None:
            break

        total_cards += 1

        for j in range(cards_won):
            if card_num + j + 1 < n_cards:
                queue.append(card_num + j + 1)
    return total_cards


def main():
    lines = parse_cards()
    total_points = get_total_points(lines)
    print(f"{total_points=}")

    winning_cards = pre_compute_wins(lines)
    total_cards = get_total_cards_won(len(lines), winning_cards)
    print(f"{total_cards=}")

if __name__ == "__main__":
    main()
