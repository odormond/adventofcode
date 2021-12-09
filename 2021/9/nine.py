#! /usr/bin/env python

from itertools import product
from functools import reduce
from pathlib import Path
import advent_of_code as adv


def to_grid_of_int(text):
    return [
        [int(c) for c in line]
        for line in text.strip().splitlines()
    ]


test_data = to_grid_of_int("""\
2199943210
3987894921
9856789892
8767896789
9899965678
""")
data = adv.input(Path(__file__).parent.name, to_grid_of_int)


def neighbours(line, column, n_lines, n_cols):
    for dl, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= line + dl < n_lines and 0 <= column + dc < n_cols:
            yield (line+dl, column+dc)


def low_points(grid):
    n_lines = len(grid)
    n_cols = len(grid[0])
    for line, column in product(range(n_lines), range(n_cols)):
        cell = grid[line][column]
        if all(cell < grid[l][c] for l, c in neighbours(line, column, n_lines, n_cols)):
            yield (line, column)


def total_risk_level(grid):
    return sum(grid[line][column] + 1 for line, column in low_points(grid))


assert total_risk_level(test_data) == 15
print("Part 1:", total_risk_level(data))


def ordered_bassin_sizes(grid):
    n_lines = len(grid)
    n_cols = len(grid[0])
    seeds = list(low_points(grid))
    bassins = []
    for seed in seeds:
        bassin = []
        bassins.append(bassin)
        visited = set()
        queue = [seed]
        while queue:
            line, column = queue.pop(0)
            if grid[line][column] == 9:
                continue
            bassin.append((line, column))
            visited.add((line, column))
            for l, c in neighbours(line, column, n_lines, n_cols):
                if (l, c) in visited:
                    continue
                queue.append((l, c))
                visited.add((l, c))
    return sorted(bassins, key=lambda x: -len(x))


assert reduce(lambda a, b: a*b, map(len, ordered_bassin_sizes(test_data)[:3]), 1) == 1134
print("Part 2:", reduce(lambda a, b: a*b, map(len, ordered_bassin_sizes(data)[:3]), 1))
