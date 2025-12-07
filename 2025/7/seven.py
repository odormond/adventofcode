#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

def parse(data):
    lines = data.splitlines()
    return {
        (l, c) for l, line in enumerate(lines) for c, v in enumerate(line) if v == "^"
    }, next(c for c, v in enumerate(lines[0]) if v == "S"), len(lines)


def part1(data):
    splitters, start, height = parse(data)
    splits = 0
    beams = {start}
    for l in range(height):
        new_beams = set()
        for c in beams:
            if (l, c) in splitters:
                splits += 1
                new_beams |= {c - 1, c + 1}
            else:
                new_beams.add(c)
        beams = new_beams
    return splits


assert (result := part1(test_data)) == 21, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    splitters, start, height = parse(data)
    beams = {start: 1}
    for l in range(height):
        new_beams = {}
        for c, timelines in beams.items():
            if (l, c) in splitters:
                new_beams[c - 1] = new_beams.get(c - 1, 0) + timelines
                new_beams[c + 1] = new_beams.get(c + 1, 0) + timelines
            else:
                new_beams[c] = new_beams.get(c, 0) + timelines
        beams = new_beams
    return sum(beams.values())


assert (result := part2(test_data)) == 40, f"{result=}"
print("Part 2:", part2(aoc.input()))
