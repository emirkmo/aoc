from pathlib import Path

import numpy as np
import pandas as pd

seeds = np.array([
    432986705,
    28073546,
    1364097901,
    88338513,
    2733524843,
    234912494,
    3151642679,
    224376393,
    485709676,
    344068331,
    1560394266,
    911616092,
    3819746175,
    87998136,
    892394515,
    435690182,
    4218056486,
    23868437,
    848725444,
    8940450,
])

titles = [
    "seed-to-soil map:",
    "soil-to-fertilizer map:",
    "fertilizer-to-water map:",
    "water-to-light map:",
    "light-to-temperature map:",
    "temperature-to-humidity map:",
    "humidity-to-location map:",
]

mappings = {
    "seed": "soil",
    "soil": "fertilizer",
    "fertilizer": "water",
    "water": "light",
    "light": "temperature",
    "temperature": "humidity",
    "humidity": "location",
}

used_titles = titles.copy()
maps = {}
with open(Path(__file__).parent/"input.txt") as f:
    ranges = []
    # while len(used_titles) > 0:
    maps = {}
    current_title = None
    for line in f:
        print(current_title)
        if not line.strip():
            maps[current_title] = ranges.copy()
            ranges = []
            current_title = None
            continue
        if line.strip() in titles:
            current_title = line.split('-')[0]
            continue
        if current_title:
            ranges.append([int(l) for l in line.split()])
    maps[current_title] = ranges.copy()
    ranges = []
    current_title = None


print(maps)

# Convert list of 3 ranges to a pandas dataframe
dfs = {}
source = seeds
df_map = pd.DataFrame()

df_map["seed"] = seeds

for i,map_ranges in enumerate(maps):
    source_name = map_ranges
    dest_name = mappings[map_ranges]
    print(i, map_ranges, source_name, dest_name)

    # if i == 0:
    #     source = seeds
    # else:
    #     source = np.hstack([val.flatten() for val in dfs[list(mappings.keys())[i-1]]["dest_items"].values])
    #     print(source)

    source = df_map[source_name].values


    df = pd.DataFrame(maps[source_name], columns=["dest_start", "source_start", "length"])
    df["dest_end"] = df["dest_start"] + df["length"]
    df["source_end"] = df["source_start"] + df["length"]
    df["offset"] = df["dest_start"] - df["source_start"]

    df["source_items"] = df.apply(lambda row: source[(source >= row["source_start"]) & (source <= row["source_end"])], axis=1)


    df["dest_items"] = df[["source_items", "offset"]].apply(lambda row: row["source_items"] + row["offset"], axis=1)



    df_map[dest_name] = df_map[source_name]

    for i, s in enumerate(df_map[source_name]):
        row_s = np.where(df["source_items"].apply(lambda x: s in x))[0]
        if not row_s:
            continue

        ind = row_s[0]
        df_map.loc[i, dest_name] = df_map.loc[i, dest_name] + df.loc[ind, "offset"]

print(df_map["location"].min())
print(df_map[df_map["humidity"] == df_map["humidity"].min()])

# for name, df in dfs.items():
#     print(name)

#     df["source_items"]

#print(df_map)
# print(maps)
        # for i, seed in enumerate(seeds):
        #     if seed == int(line):
        #         print(f"{titles[i]} {seed}")
        #         break
        # else:
        #     print("invalid seed