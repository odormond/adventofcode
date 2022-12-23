#! /usr/bin/env python

from collections import defaultdict
from math import inf

import advent_of_code as adv

test_data = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""


def parse(data):
    return {
        (x, y) for y, line in enumerate(data.splitlines()) for x, c in enumerate(line) if c == '#'
    }


def neighbours(x, y, elves):
    north = {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}.intersection(elves)
    south = {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}.intersection(elves)
    west = {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}.intersection(elves)
    east = {(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}.intersection(elves)
    return north, south, west, east


def show(elves):
    lx = min(x for x, y in elves)
    hx = max(x for x, y in elves)
    ly = min(y for x, y in elves)
    hy = max(y for x, y in elves)
    print('\n'.join(''.join('#' if (x, y) in elves else '.' for x in range(lx, hx+1)) for y in range(ly, hy+1)))
    input()


def simulate(data, max_rounds):
    elves = parse(data)
    progress = True
    rounds = 0
    phase = 0
    while progress and rounds < max_rounds:
        progress = False
        proposals = defaultdict(set)
        for x, y in elves:
            north, south, west, east = neighbours(x, y, elves)
            if north | south | west | east:
                for attempt in range(4):
                    direction = (attempt + phase) % 4
                    if [north, south, west, east][direction] == set():
                        dx, dy = [(0, -1), (0, 1), (-1, 0), (1, 0)][direction]
                        proposals[(x + dx, y + dy)].add((x, y))
                        break
        for (px, py), candidates in proposals.items():
            if len(candidates) == 1:
                progress = True
                elves.remove(candidates.pop())
                elves.add((px, py))
        phase = (phase + 1) % 4
        rounds += 1
        #show(elves)
    lx = min(x for x, y in elves)
    hx = max(x for x, y in elves)
    ly = min(y for x, y in elves)
    hy = max(y for x, y in elves)
    # print('\n'.join(''.join('#' if (x, y) in elves else '.' for x in range(lx, hx+1)) for y in range(ly, hy+1)))
    return (hx + 1 - lx) * (hy + 1 - ly) - len(elves), rounds


assert (result := simulate(test_data, 10)[0]) == 110, f"{result=}"
print("Part 1:", simulate(adv.input(), 10)[0])

assert (result := simulate(test_data, inf)[1]) == 20, f"{result=}"
print("Part 2:", simulate(adv.input(), inf)[1])
