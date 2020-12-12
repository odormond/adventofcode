#! /usr/bin/env python3

import os.path
import advent_of_code as adv


TEST = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""


def to_seat_grid(text):
    lines = text.strip().splitlines()
    height = len(lines)
    width = len(lines[0])
    return width, height, list("".join(lines))


def neighbours(x, y, width, height, cells):
    for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
        if 0 <= y + dy < height and 0 <= x + dx < width:
            yield (y + dy) * width + (x + dx)


def apply_rules(x, y, width, height, cells, rules):
    to_check, leave = rules
    adjacent = [cells[i] for i in to_check(x, y, width, height, cells)]
    seat = cells[y * width + x]
    if seat == "L" and adjacent.count("#") == 0:
        return "#"
    if seat == "#" and adjacent.count("#") >= leave:
        return "L"
    return seat


def iterate(grid, rules):
    width, height, cells = grid
    return (
        width,
        height,
        [
            apply_rules(x, y, width, height, cells, rules)
            for y in range(height)
            for x in range(width)
        ],
    )


def simulate(grid, rules):
    width, height, new = grid
    prev = None
    while prev != new:
        prev = new
        _, _, new = iterate((width, height, prev), rules)
    return width, height, new


assert simulate(to_seat_grid(TEST), (neighbours, 4))[2].count("#") == 37

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), to_seat_grid)
print("Part 1:", simulate(data, (neighbours, 4))[2].count("#"))


def visible(x, y, width, height, cells):
    vectors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    while vectors:
        dx, dy = vectors.pop(0)
        for distance in range(1, max(width, height)):
            tx = x + dx * distance
            ty = y + dy * distance
            if 0 <= ty < height and 0 <= tx < width and cells[ty * width + tx] in "L#":
                yield ty * width + tx
                break


assert simulate(to_seat_grid(TEST), (visible, 5))[2].count("#") == 26
print("Part 2:", simulate(data, (visible, 5))[2].count("#"))
