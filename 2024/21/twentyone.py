#! /usr/bin/env python

from functools import cache, partial
from itertools import permutations

import advent_of_code as aoc

test_data = """\
029A
980A
179A
456A
379A
"""

tests = (
    ("029A", 68),
    ("980A", 60),
    ("179A", 68),
    ("456A", 64),
    ("379A", 64),
)


def parse(data):
    return [(code, int(code[:-1])) for code in data.splitlines()]


PADS = {
    "NUMPAD": {
        "A": (0, 0),
        "0": (0, 1),
        "1": (1, 2),
        "2": (1, 1),
        "3": (1, 0),
        "4": (2, 2),
        "5": (2, 1),
        "6": (2, 0),
        "7": (3, 2),
        "8": (3, 1),
        "9": (3, 0),
    },
    "DIRPAD": {
        "A": (0, 0),
        "^": (0, 1),
        "<": (-1, 2),
        "v": (-1, 1),
        ">": (-1, 0),
    },
}
INVALID = (0, 2)
MOVES = {
    "<": (0, 1),
    ">": (0, -1),
    "^": (1, 0),
    "v": (-1, 0),
}


def is_valid(l, c, moves):
    for move in moves:
        dl, dc = MOVES[move]
        l += dl
        c += dc
        if (l, c) == INVALID:
            return False
    return True


def shortests(seqs):
    seqs = sorted(seqs, key=len)
    shortest = len(seqs[0])
    return ["".join(s) for s in seqs if len(s) == shortest]


def from_pad(code, pad):
    seqs = [()]
    l, c = (0, 0)
    for key in code:
        tl, tc = PADS[pad][key]
        dl, dc = tl - l, tc - c
        if dl == dc == 0:
            perm = {()}
        else:
            perm = set(
                filter(
                    partial(is_valid, l, c),
                    permutations(["^" if dl > 0 else "v"] * abs(dl) + ["<" if dc > 0 else ">"] * abs(dc))
                )
            )
        seqs = [s + p + ("A",) for s in seqs for p in perm]
        l, c = tl, tc
    return shortests(seqs)


@cache
def solve(code, chain, pad="NUMPAD"):
    seqs = from_pad(code, pad)
    if chain == 0:
        return min(len(s) for s in seqs)
    return min(sum(solve(chunk + "A", chain - 1, "DIRPAD") for chunk in seq.split("A")[:-1]) for seq in seqs)


def solver(data, chain):
    return sum(solve(code, chain) * num for code, num in parse(data))


for code, min_seq_len in tests:
    assert (result := solve(code, 2)) == min_seq_len, f"{code}: wrong sequence length {result} != {min_seq_len}"

assert (result := solver(test_data, 2)) == 126384, f"{result=}"
print("Part 1:", solver(aoc.input(), 2))
print("Part 2:", solver(aoc.input(), 25))
