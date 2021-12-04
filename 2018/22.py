#! /usr/bin/env python3

import functools
import itertools
import sys

sys.setrecursionlimit(10000)

DEPTH = 10647
TARGET = (7, 770)


def geologic_index(x, y):
    if (x, y) in ((0, 0), TARGET):
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion_level(x-1, y) * erosion_level(x, y-1)


@functools.lru_cache(maxsize=7*770)
def erosion_level(x, y):
    return (geologic_index(x, y) + DEPTH) % 20183


def risk_level(x, y):
    return erosion_level(x, y) % 3


def region_type(x, y):
    return ['rocky', 'wet', 'narrow'][risk_level(x, y)]


print("Part one:", sum(risk_level(x, y) for x, y in itertools.product(range(TARGET[0]+1), range(TARGET[1]+1))))
