import pandas as pd
import numpy as np

df = pd.read_csv('day1input.csv', header=None,names=['d'])

a = np.array(df.d, dtype=np.int64)


i = 0
j = 3
# Sliding Window
previous_sum = None
increased = 0
while i < len(a):
    #while j <= len(a):
    win = a[i:j]
    winsum = sum(win)

    if previous_sum is not None:
        if winsum > previous_sum:
            increased += 1 
    previous_sum = winsum
    i += 1
    j += 1
print(increased)