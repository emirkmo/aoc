numbers = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


# For debugging
def replace_numbers(line: str) -> str:
    for key, value in numbers.items():
        line = line.replace(key, str(value))
    return line


def get_calibration(line: str) -> int:
    first_char = get_first_char(line)
    last_char = get_last_char(line)
    return int(f"{first_char}{last_char}")


def get_first_char(line: str) -> int:
    min_ind = 999999
    mind_ind_num_string = ""
    for num_string, num in numbers.items():
        ind = line.find(num_string)
        if min_ind > ind > -1:
            min_ind = ind
            mind_ind_num_string = num

    for i, char in enumerate(line):
        if char.isdigit():
            if i < min_ind:
                return int(char)
            elif not mind_ind_num_string:
                raise ValueError(f"No digit found {line}")
            return int(mind_ind_num_string)
    raise ValueError(f"No digit found {line}")


def get_last_char(line: str) -> int:
    min_ind = -1
    mind_ind_num_string = ""
    for num_string, num in numbers.items():
        ind = line.rfind(num_string)
        if min_ind < ind and ind != -1:
            min_ind = ind
            mind_ind_num_string = num

    for i, char in enumerate(line[::-1]):
        j = len(line) - i - 1
        if char.isdigit():
            if j > min_ind:
                return int(char)
            elif not mind_ind_num_string:
                raise ValueError(f"No digit found {line}")
            return int(mind_ind_num_string)
    raise ValueError(f"No digit found {line}")


lines = []
with open("input.txt") as f:
    lines = f.readlines()

with open("replaced.txt", "w") as f:
    for line in lines:
        f.write(replace_numbers(line))

calibrations = sum([get_calibration(line) for line in lines if line])
print(calibrations)
