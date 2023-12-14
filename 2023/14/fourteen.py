#! /usr/bin/env python

import advent_of_code as adv

test_data = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

def parse(data):
    rocks = [
        (l, c, symbol)
        for l, line in enumerate(data.splitlines())
        for c, symbol in enumerate(line)
        if symbol != '.'
    ]
    rounds = {(l, c) for l, c, s in rocks if s == 'O'}
    cubes = {(l, c) for l, c, s in rocks if s == '#'}
    return rounds, cubes


def roll_north(rounds, cubes, width, height):
    rolled = set()
    for c in range(width):
        pos, pack = 0, 0
        for l in range(height):
            if (l, c) in rounds:
                pack += 1
            elif (l, c) in cubes:
                for i in range(pos, pos + pack):
                    rolled.add((i, c))
                pos, pack = l + 1, 0
        for i in range(pos, pos + pack):
            rolled.add((i, c))
    assert len(rounds) == len(rolled)
    return rolled


def roll_west(rounds, cubes, width, height):
    rolled = set()
    for l in range(height):
        pos, pack = 0, 0
        for c in range(width):
            if (l, c) in rounds:
                pack += 1
            elif (l, c) in cubes:
                for i in range(pos, pos + pack):
                    rolled.add((l, i))
                pos, pack = c + 1, 0
        for i in range(pos, pos + pack):
            rolled.add((l, i))
    assert len(rounds) == len(rolled)
    return rolled


def roll_south(rounds, cubes, width, height):
    rolled = set()
    for c in range(width):
        pos, pack = height - 1, 0
        for l in range(height - 1, -1, -1):
            if (l, c) in rounds:
                pack += 1
            elif (l, c) in cubes:
                for i in range(pos, pos - pack, -1):
                    rolled.add((i, c))
                pos, pack = l - 1, 0
        for i in range(pos, pos - pack, -1):
            rolled.add((i, c))
    assert len(rounds) == len(rolled)
    return rolled


def roll_east(rounds, cubes, width, height):
    rolled = set()
    for l in range(height):
        pos, pack = width - 1, 0
        for c in range(width - 1, -1, -1):
            if (l, c) in rounds:
                pack += 1
            elif (l, c) in cubes:
                for i in range(pos, pos - pack, -1):
                    rolled.add((l, i))
                pos, pack = c - 1, 0
        for i in range(pos, pos - pack, -1):
            rolled.add((l, i))
    assert len(rounds) == len(rolled)
    return rolled


def part1(data):
    height = len(data.splitlines())
    width = len(data.splitlines()[0])
    rounds, cubes = parse(data)

    rounds = roll_north(rounds, cubes, width, height)

    return sum(height - l for l, c in rounds)


assert (result := part1(test_data)) == 136, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data, count):
    height = len(data.splitlines())
    width = len(data.splitlines()[0])
    rounds, cubes = parse(data)

    seen = {}
    for i in range(count):
        rounds = roll_north(rounds, cubes, width, height)
        rounds = roll_west(rounds, cubes, width, height)
        rounds = roll_south(rounds, cubes, width, height)
        rounds = roll_east(rounds, cubes, width, height)
        state = tuple(sorted(rounds))
        if state not in seen:
            seen[state] = sum(height - l for l, c in rounds)
        else:
            break

    for offset, known in enumerate(seen):
        if known == state:
            break

    cycle = len(seen) - offset
    return list(seen.values())[offset + (count - offset) % cycle - 1]


assert (result := part2(test_data, 1000000000)) == 64, f"{result=}"
print("Part 2:", part2(adv.input(), 1000000000))
