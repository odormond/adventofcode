#! /usr/bin/env python

from itertools import product
from pathlib import Path
from string import digits, ascii_uppercase
import advent_of_code as adv


def to_grid_of_int(text):
    return [
        [int(c) for c in line]
        for line in text.strip().splitlines()
    ]


test_data = to_grid_of_int("""\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""")
data = adv.input(Path(__file__).parent.name, to_grid_of_int)


def neighbours(line, column, n_lines, n_cols):
    for dl, dc in product((-1, 0, 1), repeat=2):
        if (dl, dc) == (0, 0):
            continue
        if 0 <= line + dl < n_lines and 0 <= column + dc < n_cols:
            yield line + dl, column + dc


def flashed_cell(cell):
    return f'\033[1m{(digits+ascii_uppercase)[cell]}\033[0m'


def print_grid(grid, flashed):
    print('\n'.join(''.join(flashed_cell(cell) if (l, c) in flashed else str(cell) for c, cell in enumerate(line)) for l, line in enumerate(grid)))
    input("enter to continue")


def step(grid):
    n_lines = len(grid)
    n_cols = len(grid[0])

    grid = [[cell + 1 for cell in line] for line in grid]
    flashed = []
    queue = []
    for l, line in enumerate(grid):
        for c, cell in enumerate(line):
            if cell > 9:
                flashed.append((l, c))
                queue.append((l, c))
    while queue:
        line, column = queue.pop(0)
        for l, c in neighbours(line, column, n_lines, n_cols):
            if grid[l][c] == 9:
                flashed.append((l, c))
                queue.append((l, c))
            grid[l][c] += 1
    for l, c in flashed:
        assert flashed.count((l, c)) == 1, f"Multiflash!: {(l, c)} #{flashed.count((l, c))}"
        grid[l][c] = 0
    return grid, flashed


def iterate(grid, count):
    total = 0
    for i in range(count):
        grid, flashed = step(grid)
        total += len(flashed)
    return total


def find_all_flash(grid):
    n_lines = len(grid)
    n_cols = len(grid[0])
    flashed = []
    i = 0
    while len(flashed) != n_lines * n_cols:
        i += 1
        grid, flashed = step(grid)
    return i


assert (count := iterate(test_data, 100)) == 1656, f"Wrong flash count: {count}"
print("Part 1:", iterate(data, 100))


assert (count := find_all_flash(test_data)) == 195, f"Wrong all flash step: {count}"
print("Part 2:", find_all_flash(data))
