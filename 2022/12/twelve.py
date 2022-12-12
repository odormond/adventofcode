#! /usr/bin/env python

from collections import defaultdict
from itertools import product
from math import inf

import advent_of_code as adv

test_data = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


HEIGTH = 'SabcdefghijklmnopqrstuvwxyzE'

def parse(data):
    h_map = [[HEIGTH.index(c) for c in line] for line in data.splitlines()]
    heigth = len(h_map)
    width = len(h_map[0])
    for x, y in product(range(width), range(heigth)):
        if h_map[y][x] == 0:
            start = (x, y)
            h_map[y][x] = 1
        elif h_map[y][x] == 27:
            end = (x, y)
            h_map[y][x] = 26
    return h_map, width, heigth, start, end


def neighboors(x, y, width, heigth):
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if 0 <= x + dx < width and 0 <= y + dy < heigth:
            yield x + dx, y + dy


class PriorityQueue:
    def __init__(self):
        self.queue = defaultdict(set)
        self.priorities = []

    def push(self, priority, value):
        self.queue[priority].add(value)
        self.priorities = sorted(self.queue)

    def pop(self):
        p = self.priorities[0]
        top = self.queue[p]
        value = top.pop()
        if not top:
            del self.queue[p], self.priorities[0]
        return p, value

    def __bool__(self):
        return bool(self.priorities)


def find_path(h_map, width, heigth, start, end):
    visited = set()
    queue = PriorityQueue()
    d_map = [[inf for _ in range(width)] for _ in range(heigth)]
    queue.push(0, start)
    x, y = start
    d_map[y][x] = 0
    last_d = 0
    while queue:
        _, (p, q) = queue.pop()
        visited.add((p, q))
        h = h_map[q][p]
        for x, y in neighboors(p, q, width, heigth):
            if (x, y) in visited:
                continue
            t = h_map[y][x]
            if t <= h + 1:
                n = d_map[y][x] = min(d_map[y][x], d_map[q][p] + 1)
                queue.push(n, (x, y))
    x, y = end
    return d_map[y][x]


assert (result := find_path(*parse(test_data))) == 31, f"{result=}"
print("Part 1:", find_path(*parse(adv.input())))


def find_best_path(h_map, width, heigth, start, end):
    starts = [(x, y) for y, line in enumerate(h_map) for x, h in enumerate(line) if h == 1]
    print(len(starts))
    return min(find_path(h_map, width, heigth, start, end) for start in starts)


assert (result := find_best_path(*parse(test_data))) == 29, f"{result=}"
print("Part 2:", find_best_path(*parse(adv.input())))
