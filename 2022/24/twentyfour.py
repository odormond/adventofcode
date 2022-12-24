#! /usr/bin/env python

from functools import reduce

import advent_of_code as adv

test_data = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""


def parse(data):
    lines = data.splitlines()
    start = lines[0].index('.') - 1, -1
    end = lines[-1].index('.') - 1, len(lines) - 2
    blizzards = [{(x - 1, y - 1) for y, line in enumerate(lines) for x, c in enumerate(line) if c == b} for b in '>v<^']
    return start, end, blizzards, len(lines[-1]) - 2, len(lines) - 2


def forecasting(blizzards, width, height):
    forecasts = []
    occupied = reduce(set.union, blizzards, set())
    while occupied not in forecasts:
        forecasts.append(occupied)
        blizzards = [
            {((x + [1, 0, -1, 0][i]) % width, (y + [0, 1, 0, -1][i]) % height) for x, y in b}
            for i, b in enumerate(blizzards)
        ]
        occupied = reduce(set.union, blizzards, set())
    return forecasts


def moves(x, y, width, height, end):
    yield (x, y)  # stay still
    for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        if (x + dx, y + dy) == end:
            yield end
        if 0 <= x + dx < width and 0 <= y + dy < height:
            yield (x + dx, y + dy)


def simulate(pos, goals, blizzards, width, height):
    forecasts = forecasting(blizzards, width, height)
    cycle = len(forecasts)
    steps = 0
    queue = {pos}
    while True:
        forecast = forecasts[(steps + 1) % cycle]
        n_queue = set()
        for pos in queue:
            if pos == goals[0]:
                del goals[0]
                if not goals:
                    return steps
                n_queue = {pos}
                break
            for n_pos in moves(*pos, width, height, goals[0]):
                if n_pos not in forecast:
                    n_queue.add(n_pos)
        steps += 1
        queue = n_queue


def part1(data):
    start, end, blizzards, width, height = parse(data)
    return simulate(start, [end], blizzards, width, height)


assert (result := part1(test_data)) == 18, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    start, end, blizzards, width, height = parse(data)
    return simulate(start, [end, start, end], blizzards, width, height)


assert (result := part2(test_data)) == 54, f"{result=}"
print("Part 2:", part2(adv.input()))
