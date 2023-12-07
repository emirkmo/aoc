from pathlib import Path
import pandas as pd

with open(Path(__file__).parent / 'input.txt') as f:
    lines = f.readlines()

_hand_lines = [(linelist[0], int(linelist[1])) for line in lines if (linelist := line.strip().split())]

df = pd.DataFrame(_hand_lines, columns=["cards", "bid"])

print(df.head())