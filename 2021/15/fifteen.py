#! /usr/bin/env python

from collections import defaultdict
from heapq import heappush, heappop
from itertools import product
from math import inf
from pathlib import Path
import advent_of_code as adv


def to_grid_of_int(text):
    return [
        [int(c) for c in line]
        for line in text.strip().splitlines()
    ]


test_data = to_grid_of_int("""\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""")
data = adv.input(Path(__file__).parent.name, to_grid_of_int)


def neighbours(line, column, n_lines, n_cols):
    for dl, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        if 0 <= line + dl < n_lines and 0 <= column + dc < n_cols:
            yield line + dl, column + dc


def risk(grid):
    n_lines = len(grid)
    n_cols = len(grid[0])
    risks = defaultdict(lambda: inf, {(0, 0): 0})
    visited = set()
    queue = []
    heappush(queue, (0, (0, 0)))  # risk first for the ordering
    while queue:
        risk, pos = heappop(queue)
        visited.add(pos)
        for neigh in neighbours(*pos, n_lines, n_cols):
            if neigh in visited:
                continue
            l, c = neigh
            new_risk = risk + grid[l][c]
            if new_risk < risks[neigh]:
                risks[neigh] = new_risk
                heappush(queue, (new_risk, neigh))
    return [[risks[l, c] for c in range(n_cols)] for l in range(n_lines)]


def find_path(grid, risks, pos=None):
    n_lines = len(grid)
    n_cols = len(grid[0])
    pos = pos or (n_lines - 1, n_cols - 1)
    line, column = pos
    prev_risk = risks[line][column] - grid[line][column]
    path = {pos}
    while pos != (0, 0):
        line, column = pos
        prev_risk = risks[line][column] - grid[line][column]
        prev_pos = [
            (l, c)
            for l, c in neighbours(line, column, n_lines, n_cols)
            if risks[l][c] == prev_risk
        ]
        if len(prev_pos) == 1:
            pos = prev_pos[0]
            path.add(pos)
            continue
        elif prev_pos == []:  # Deadend
            risks[line][column] = -1
            return None
        for prev in prev_pos:
            if leading_path := find_path(grid, risks, prev):
                return path.union(leading_path)
        risks[line][column] = -1
        return None
    return path
    

INV = '\033[7m'
RST = '\033[0m'

def print_path(grid):
    risks = risk(grid)
    path = find_path(grid, risks)
    # print('\n'.join(' '.join(f'{INV}{v}|{risks[l][c]:<4d}{RST}' if (l, c) in path else f'{v}|{risks[l][c]:<4d}' for c, v in enumerate(line)) for l, line in enumerate(grid)))
    print('\n'.join(''.join(f'{INV}{v}{RST}' if (l, c) in path else f'{v}' for c, v in enumerate(line)) for l, line in enumerate(grid)))


assert risk(test_data)[-1][-1] == 40
print("Part 1:", risk(data)[-1][-1])


def enlarge(grid):
    n_lines = len(grid)
    n_cols = len(grid[0])
    return [
        [(grid[l][c] + i + j - 1) % 9 + 1 for j in range(5) for c in range(n_cols)]
        for i in range(5) for l in range(n_lines)
    ]


test_grid = enlarge(test_data)
test_risks = risk(test_grid)
assert test_risks[-1][-1] == 315
#print_path(test_grid)


print("Part 2:", risk(enlarge(data))[-1][-1])
#print_path(enlarge(data))
