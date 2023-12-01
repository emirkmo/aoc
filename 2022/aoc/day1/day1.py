import numpy as np
import pandas as pd

with open("input.txt") as f:
    data = f.read().splitlines()

elf = 0
elves = {}
calories = 0
maxcals = 0
maxelf = 0
for cal in data:
    if cal == "":
        if calories > maxcals:
            maxcals = calories
            maxelf = elf
        elves[elf] = calories
        calories = 0
        elf += 1
        continue
    calories += int(cal)

print(maxelf, maxcals)

#for i, v in elves.items():

df = pd.DataFrame(index=elves.keys(), data=elves.values(), columns=['calories'])
df.sort_values(inplace=True, by='calories', ascending=False)
print(df.head(3).sum())
