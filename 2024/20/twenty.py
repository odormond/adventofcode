#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def neighbour(pos):
    l, c = pos
    for dl, dc in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        yield l + dl, c + dc


def parse(data):
    track = set()
    for l, line in enumerate(data.splitlines()):
        for c, v in enumerate(line):
            if v != "#":
                track.add((l, c))
            if v == "S":
                start = (l, c)
            elif v == "E":
                end = (l, c)
    race = {}
    pos = start
    while pos != end:
        race[pos] = len(race)
        track.remove(pos)
        for n in neighbour(pos):
            if n in track:
                pos = n
                break
    race[end] = len(race)
    return race, start, end


def cheat(pos):
    l, c = pos
    for dl, dc in ((-2, 0), (0, -2), (2, 0), (0, 2)):
        yield l + dl, c + dc


def part1(data, threshold):
    race, start, end = parse(data)
    cheats = []
    for pos in race:
        for jump in cheat(pos):
            if jump in race and (save := race[jump] - race[pos] - 2) > 0:
                cheats.append((pos, save))
    return sum(1 for _, save in cheats if save >= threshold)


assert (result := part1(test_data, 2)) == 44, f"{result=}"
print("Part 1:", part1(aoc.input(), 100))


def cheat2(pos):
    l, c = pos
    for dl, dc in ((-2, 0), (0, -2), (2, 0), (0, 2)):
        yield l + dl, c + dc


def part2(data, threshold):
    race, start, end = parse(data)
    track = list(race)
    cheats = set()
    for i, pos in enumerate(track):
        l, c = pos
        for jump in track[i+1:]:
            tl, tc = jump
            if (cost := abs(tl - l) + abs(tc - c)) <= 20 and (save := race[jump] - race[pos] - cost) >= threshold:
                cheats.add((pos, jump, save))
    return len(cheats)


assert (result := part2(test_data, 50)) == 285, f"{result=}"
print("Part 2:", part2(aoc.input(), 100))
