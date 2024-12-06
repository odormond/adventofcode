#! /usr/bin/env python

from collections import defaultdict
from copy import deepcopy
from itertools import product

import advent_of_code as aoc

test_data = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

def parse(data):
    grid = {
        (l, c): v
        for l, line in enumerate(data.splitlines())
        for c, v in enumerate(line)
    }
    obstacles = {pos for pos, v in grid.items() if v == "#"}
    start = {pos for pos, v in grid.items() if v == "^"}.pop()
    bound = max(grid)
    return obstacles, start, bound


TURN = {
    (-1, 0): (0, 1),  # up to right
    (0, 1): (1, 0),  # right to down
    (1, 0): (0, -1),  # down to left
    (0, -1): (-1, 0),  # left to up
}


def part1(data):
    obstacles, (guard_l, guard_c), (max_l, max_c) = parse(data)
    dl, dc = (-1, 0)  # up
    visited = set()
    while 0 <= guard_l <= max_l and 0 <= guard_c <= max_c:
        visited.add((guard_l, guard_c))
        if (guard_l + dl, guard_c + dc) in obstacles:
            dl, dc = TURN[(dl, dc)]
        guard_l += dl
        guard_c += dc
    return len(visited)


assert (result := part1(test_data)) == 41, f"{result=}"
print("Part 1:", part1(aoc.input()))


def will_loop(gl, gc, dl, dc, max_l, max_c, obstacles, visited=None):
    visits = defaultdict(set)
    while 0 <= gl <= max_l and 0 <= gc <= max_c:
        if visited and (gl, gc) in visited and (dl, dc) in visited[(gl, gc)]:
            return True
        if (gl, gc) in visits and (dl, dc) in visits[(gl, gc)]:
            return True
        visits[(gl, gc)].add((dl, dc))
        while (gl + dl, gc + dc) in obstacles:
            dl, dc = TURN[(dl, dc)]
            visits[(gl, gc)].add((dl, dc))
        gl += dl
        gc += dc
    return False


def part2_smart(data):
    obstacles, (guard_l, guard_c), (max_l, max_c) = parse(data)
    dl, dc = (-1, 0)  # up
    visits = defaultdict(set)
    new_obstacles = set()
    while 0 <= guard_l <= max_l and 0 <= guard_c <= max_c:
        guard = guard_l, guard_c
        visits[guard].add((dl, dc))
        while (guard_l + dl, guard_c + dc) in obstacles:
            dl, dc = TURN[(dl, dc)]
            visits[guard].add((dl, dc))
        next_pos = guard_l + dl, guard_c + dc
        if (
            0 <= next_pos[0] <= max_l and 0 <= next_pos[1] <= max_c  # In front of us is in the field
            and next_pos not in visits  # We wouldn't be blocking the path that brought us there
            and will_loop(*guard, *TURN[(dl, dc)], max_l, max_c, obstacles | {next_pos}, visits)  # We're stuck in a loop
        ):
            new_obstacles.add(next_pos)
        guard_l += dl
        guard_c += dc
    return len(new_obstacles)


def part2_brute(data):
    count = 0
    obstacles, start, (max_l, max_c) = parse(data)
    dl, dc = (-1, 0)  # up
    for extra in product(range(max_l + 1), range(max_c + 1)):
        if extra in obstacles or extra == start:
            continue
        if will_loop(*start, dl, dc, max_l, max_c, obstacles | {extra}):
            count += 1
    return count


assert (result := part2_smart(test_data)) == 6, f"{result=}"
assert (result := part2_brute(test_data)) == 6, f"{result=}"
print("Part 2 (smart):", part2_smart(aoc.input()))
# print("Part 2 (brute):", part2_brute(aoc.input()))
