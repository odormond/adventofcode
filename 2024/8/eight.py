#! /usr/bin/env python

from collections import defaultdict
from itertools import combinations

import advent_of_code as aoc

test_data = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

def parse(data):
    return {
        (l, c): f
        for l, line in enumerate(data.splitlines())
        for c, f in enumerate(line)
        if f != "."
    }, len(data.splitlines()), len(data.splitlines()[0])


def part1(data):
    antenneas, height, width = parse(data)
    by_freq = defaultdict(list)
    for pos, freq in antenneas.items():
        by_freq[freq].append(pos)
    antinodes = set()
    for positions in by_freq.values():
        for a, b in combinations(positions, 2):
            dl, dc = (b[0] - a[0]), (b[1] - a[1])
            l, c = (a[0] - dl), (a[1] - dc)
            if 0 <= l < height and 0 <= c < width:
                antinodes.add((l, c))
            l, c = (b[0] + dl), (b[1] + dc)
            if 0 <= l < height and 0 <= c < width:
                antinodes.add((l, c))
    return len(antinodes)


assert (result := part1(test_data)) == 14, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    antenneas, height, width = parse(data)
    by_freq = defaultdict(list)
    for pos, freq in antenneas.items():
        by_freq[freq].append(pos)
    antinodes = set()
    for positions in by_freq.values():
        for a, b in combinations(positions, 2):
            dl, dc = (b[0] - a[0]), (b[1] - a[1])
            l, c = a
            while 0 <= l < height and 0 <= c < width:
                antinodes.add((l, c))
                l -= dl
                c -= dc
            l, c = a
            while 0 <= l < height and 0 <= c < width:
                antinodes.add((l, c))
                l += dl
                c += dc
    return len(antinodes)


assert (result := part2(test_data)) == 34, f"{result=}"
print("Part 2:", part2(aoc.input()))
