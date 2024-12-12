#! /usr/bin/env python

from collections import defaultdict
from itertools import combinations

import advent_of_code as aoc

tests = (
    ("""\
AAAA
BBCD
BBCC
EEEC
""", 140, 80),
    ("""\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""", 772, 436),
    ("""\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""", 692, 236),
    ("""\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""", 1184, 368),
    ("""\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""", 1930, 1206),
)


def parse(data):
    plants = defaultdict(set)
    for l, line in enumerate(data.splitlines()):
        for c, plant in enumerate(line):
            plants[plant].add((l, c))
    return plants


def neighbours(plot):
    l, c = plot
    yield from ((l - 1, c), (l, c - 1), (l + 1, c), (l, c + 1))


def connected(plots):
    regions = []
    while plots:
        region = []
        queue = [plots.pop()]
        while queue:
            plot = queue.pop()
            region.append(plot)
            for n in neighbours(plot):
                if n in plots:
                    queue.append(n)
                    plots.remove(n)
        regions.append(region)
    return regions


def perimeter(region):
    length = 4 * len(region)
    for (la, ca), (lb, cb) in combinations(region, 2):
        if (abs(la - lb), abs(ca - cb)) in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            length -= 2
    return length


def solver(data, border_fn):
    plants = parse(data)
    return sum(
        len(region) * border_fn(region)
        for plant, plots in plants.items()
        for region in connected(plots)
    )


def part1(data):
    return solver(data, perimeter)


for i, (data, expected, _) in enumerate(tests):
    assert (result := part1(data)) == expected, f"test {i}: {result=} {expected=}"

print("Part 1:", part1(aoc.input()))


def sides(region):
    inner_edges = set()
    for (la, ca), (lb, cb) in combinations(region, 2):
        if (abs(la - lb), abs(ca - cb)) in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            if la == lb:
                inner_edges.add(((la - 0.5, (ca + cb) / 2), (la + 0.5, (ca + cb) / 2)))
            else:
                inner_edges.add((((la + lb) / 2, ca - 0.5), ((la + lb) / 2, ca + 0.5)))
    outer_edges = set()
    for l, c in region:
        for edge in (
            ((l - 0.5, c - 0.5), (l + 0.5, c - 0.5), 1),  # left
            ((l - 0.5, c - 0.5), (l - 0.5, c + 0.5), 1),  # top
            ((l - 0.5, c + 0.5), (l + 0.5, c + 0.5), -1),  # right
            ((l + 0.5, c - 0.5), (l + 0.5, c + 0.5), -1),  # bottom
        ):
            if edge[:2] not in inner_edges:
                outer_edges.add(edge)
    sides = 0
    queue = sorted(outer_edges)
    while queue:
        *side, orientation = queue.pop(0)
        progress = True
        while progress:
            progress = False
            for *edge, facing in queue[:]:
                if orientation != facing:
                    continue
                if (common := set(side) & set(edge)):
                    l1, c1 = (set(side) - common).pop()
                    l2, c2 = (set(edge) - common).pop()
                    if (l1 - l2) == 0 or (c1 - c2) == 0:
                        # aligned so part of the same side
                        queue.remove((*edge, facing))
                        side = min((l1, c1), (l2, c2)), max((l1, c1), (l2, c2))
                        progress = True
        sides += 1
    return sides



def part2(data):
    return solver(data, sides)


for i, (data, _, expected) in enumerate(tests):
    assert (result := part2(data)) == expected, f"test {i}: {result=} {expected=}"
print("Part 2:", part2(aoc.input()))
