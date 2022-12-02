"""Day 2, originally written in the notebook"""
from enum import IntEnum

import numpy as np
import pandas as pd


class Scores(IntEnum):
    win = 6
    draw = 3
    lose = 0


class RPS(IntEnum):
    rock = 1
    paper = 2
    scissors = 3


wins = {1: 2, 2: 3, 3: 1}
losses = {1: 3, 2: 1, 3: 2}


d = {"A": 1, "B": 2, "C": 3}
d2 = {"X": 1, "Y": 2, "Z": 3}  # What if lose draw win
d2_2 = {"X": 0, "Y": 3, "Z": 6}  # What if lose draw win


def rules(s1, s2):

    p1, p2 = d[s1], d2[s2]

    if p1 == p2:
        return Scores.draw + p2

    if RPS(p1) is RPS.rock:
        if RPS(p2) is RPS.paper:
            return Scores.win + p2
        return Scores.lose + p2

    if RPS(p1) is RPS.paper:
        if RPS(p2) is RPS.scissors:
            return Scores.win + p2
        return Scores.lose + p2

    if RPS(p1) is RPS.scissors:
        if RPS(p2) is RPS.rock:
            return Scores.win + p2
        return Scores.lose + p2


def new_rules(s1, s2):

    p1, p2 = d[s1], d2_2[s2]

    if Scores(p2) is Scores.draw:
        return Scores.draw + p1

    if Scores(p2) is Scores.win:
        return wins[p1] + Scores.win

    if Scores(p2) is Scores.lose:
        return losses[p1] + Scores.lose


df = pd.read_csv("input.txt", header=None, names=["p1", "p2"], delim_whitespace=True)

first = df.apply(lambda x: rules(x.p1, x.p2), axis=1)
second = df.apply(lambda x: new_rules(x.p1, x.p2), axis=1)
print(first.sum())
print(second.sum())
