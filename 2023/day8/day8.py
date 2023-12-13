from itertools import cycle
from math import lcm
from pathlib import Path

lrd: dict[str, int] = {"L": 0, "R": 1}

with open(Path(__file__).parent / "input.txt") as f:
    lines = f.readlines()

instructions = lines[0]
lines = lines[2:]

graph: dict[str, tuple[str, str]] = {} #defaultdict(tuple)
for line in lines:
    l, r = line.split(" = ")
    l = l.strip()
    tup = tuple(r.replace("(", "").replace(")", "").strip().split(", "))
    graph[l] = tup  # type: ignore

directions = cycle(lrd[character] for character in instructions.strip())
turns = 0
current_val = "AAA"
end_val = "ZZZ"
#while current_val != end_val:
for dir in directions:
    #print(turns, dir, current_val)
    if current_val == end_val:
        break
    current_val = graph[current_val][dir]
    turns += 1

print("Part 1:", turns)

# Ensure there is only a single end cycle!
current_vals = (akey for akey in graph.keys() if akey.endswith("A"))

for current_val in current_vals:
    init_dir = lrd[instructions[0]]
    init_val = current_val
    turns = 0
    ends = set()
    directions = cycle(lrd[character] for character in instructions.strip())
    for i,dir in enumerate(directions):
        if current_val.endswith("Z"):
            if current_val in ends:
                turns = i
                break
            ends.add(current_val)
            turns = i
        current_val = graph[current_val][dir]#(graph[val][dir] for val in current_val)
        if current_val == init_val and dir == init_dir:
            turns = i + 1
            print("start-cycle!")
            assert False
    assert(len(ends) == 1)


# Since there is a single cycle, safe to use least common multiple of cycle lengths
# (We could have calculated the cycle lengths from the previous step but I wanted to test
# assumptions first then write simpler code here).
current_vals = (akey for akey in graph.keys() if akey.endswith("A"))
cycles = {}
for current_val in current_vals:
    turns = 0
    init_val = current_val
    directions = cycle(lrd[character] for character in instructions.strip())
    for i,dir in enumerate(directions):
        if current_val.endswith("Z"):
            turns = i
            cycles[init_val] = turns
            break
        current_val = graph[current_val][dir]

print(f"Part 2: {lcm(*cycles.values())}")
