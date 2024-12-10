#! /usr/bin/env python

from collections import defaultdict

import advent_of_code as aoc

test_data = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

def parse(data):
    return defaultdict(
        lambda: -1,
        {(l, c): int(h) for l, line in enumerate(data.splitlines()) for c, h in enumerate(line)},
    )


def neighbour(l, c):
    return [(l-1, c), (l, c-1), (l+1, c), (l, c+1)]


def next_pos(pos, height_map):
    h = height_map[pos]
    for n in neighbour(*pos):
        if height_map[n] == h + 1:
            yield n


def trails(start, height_map):
    paths = [[start]]
    while paths:
        path = paths.pop(0)
        for pos in next_pos(path[-1], height_map):
            if height_map[pos] == 9:
                yield path + [pos]
            else:
                paths.append(path + [pos])


def solve(data):
    height_map = parse(data)
    trailheads = [pos for pos, h in height_map.items() if h == 0]
    total_score = 0
    total_rating = 0
    for head in trailheads:
        summits = set()
        for trail in trails(head, height_map):
            summits.add(trail[-1])
            total_rating += 1
        total_score += len(summits)
    return total_score, total_rating


test_score, test_rating = solve(test_data)
assert test_score == 36, f"{test_score=}"
assert test_rating == 81, f"{test_rating=}"

score, rating = solve(aoc.input())
print("Part 1:", score)
print("Part 2:", rating)
