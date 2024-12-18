#! /usr/bin/env python

from heapq import heappop, heappush

import advent_of_code as aoc

test_data = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
TEST_SIZE = 7
SIZE = 71


def parse(data):
    return [tuple(map(int, line.split(","))) for line in data.splitlines()]


def next_pos(pos, forbidden, size):
    x, y = pos
    for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in forbidden:
            yield (nx, ny)


def path_finder(falling_bytes, size, counts):
    corrupted = set(falling_bytes[:counts])
    start = (0, 0)
    end = (size - 1, size - 1)
    queue = []
    heappush(queue, (0, start))
    visited = {start}
    while queue:
        steps, pos = heappop(queue)
        if pos == end:
            return steps
        for n in next_pos(pos, corrupted, size):
            if n not in visited:
                visited.add(n)
                heappush(queue, (steps + 1, n))


def part1(data, size, counts):
    return path_finder(parse(data), size, counts)


assert (result := part1(test_data, TEST_SIZE, 12)) == 22, f"{result=}"
print("Part 1:", part1(aoc.input(), SIZE, 1024))


def part2(data, size):
    falling_bytes = parse(data)
    for counts in range(len(falling_bytes)):
        if path_finder(falling_bytes, size, counts) is None:
            return falling_bytes[counts - 1]


assert (result := part2(test_data, TEST_SIZE)) == (6, 1), f"{result=}"
print("Part 2:", part2(aoc.input(), SIZE))
