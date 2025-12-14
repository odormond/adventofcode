#! /usr/bin/env python

from functools import partial
from multiprocessing import Pool

import advent_of_code as aoc

test_data = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

def parse(data):
    shapes = []
    regions = []
    for chunk in data.split("\n\n"):
        if "x" not in chunk:
            _, *lines = chunk.strip().splitlines()
            shapes.append(
                {(l, c) for l, line in enumerate(lines) for c, s in enumerate(line) if s == "#"}
            )
        else:
            for line in chunk.strip().splitlines():
                dimensions, *shape_counts = line.split()
                width, height = dimensions[:-1].split("x")
                regions.append((int(width), int(height), [int(count) for count in shape_counts]))
    return shapes, regions


def fit(shapes, region):
    width, height, shape_counts = region
    area = width * height
    shape_sizes = [len(shape) for shape in shapes]
    if 9 * sum(shape_counts) <= area:
        return 1  # All the enclosing squares fit
    if sum(count * shape_sizes[shape] for shape, count in enumerate(shape_counts)) > area:
        return 0
    raise RuntimeError(f"Need a complex fit: {region}")


def part1(data):
    shapes, regions = parse(data)

    with Pool() as p:
        return sum(p.map(partial(fit, shapes), regions))


if __name__ == "__main__":
    # assert (result := part1(test_data)) == 2, f"{result=}"  # Troll
    print("Part 1:", part1(aoc.input()))
