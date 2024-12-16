#! /usr/bin/env python

from collections import defaultdict
from heapq import heappush, heappop
from math import inf

import advent_of_code as aoc

tests = (
    ("""\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""", 7036, 45),
    ("""\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""", 11048, 64),
)

def parse(data):
    maze = set()
    for l, line in enumerate(data.splitlines()):
        for c, v in enumerate(line):
            if v == ".":
                maze.add((l,c))
            elif v == "S":
                start = (l, c)
            elif v == "E":
                maze.add((l,c))
                end = (l, c)
    return maze, start, end


TURN_LEFT = {
    (0, 1): (-1, 0),
    (0, -1): (1, 0),
    (1, 0): (0, 1),
    (-1, 0): (0, -1),
}
TURN_RIGHT = {
    (0, 1): (1, 0),
    (0, -1): (-1, 0),
    (1, 0): (0, -1),
    (-1, 0): (0, 1),
}

def solver(data):
    maze, start, end = parse(data)
    queue = []
    heappush(queue, (0, [start], (0, 1)))
    visited = defaultdict(lambda: inf)
    paths = []
    while queue:
        score, path, (dl, dc) = heappop(queue)
        l, c = path[-1]
        visited[(l, c, dl, dc)] = score
        if (l, c) == end:
            paths.append((score, path))
            continue
        nl, nc = l + dl, c + dc
        if (nl, nc) in maze and visited[(nl, nc, dl, dc)] > score + 1:
            next_item = score + 1, [*path, (nl, nc)], (dl, dc)
            if next_item not in queue:
                heappush(queue, next_item)
        for turn in (TURN_LEFT, TURN_RIGHT):
            dtl, dtc = turn[(dl, dc)]
            tl, tc = l + dtl, c + dtc
            if (tl, tc) in maze and visited[(tl, tc, dtl, dtc)] > score + 1001:
                next_item = score + 1001, [*path, (tl, tc)], (dtl, dtc)
                if next_item not in queue:
                    heappush(queue, next_item)
    paths = sorted(paths)
    best_score, _ = paths[0]
    best_paths = [path for score, path in paths if score == best_score]
    return best_score, len({place for path in best_paths for place in path})


for test, *expected in tests:
    assert (result := solver(test)) == tuple(expected), f"{result=} instead of {expected}"
print("Part 1: %d\nPart 2: %d" % solver(aoc.input()))
