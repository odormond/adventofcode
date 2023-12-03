#! /usr/bin/env python

from itertools import product

import advent_of_code as adv

test_data = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def inbound(x, y, width, height):
    return 0 <= x < width and 0 <= y < height


def surround(x1, x2, y, width, height):
    for x in range(x1 - 1, x2 + 2):
        if inbound(x, y - 1, width, height):
            yield (x, y - 1)
    for x in (x1 - 1, x2 + 1):
        if inbound(x, y, width, height):
            yield (x, y)
    for x in range(x1 - 1, x2 + 2):
        if inbound(x, y + 1, width, height):
            yield (x, y + 1)


def parse(data):
    parts = []
    unknown = []
    lines = data.splitlines()
    # Pad lines to ensure we can detect number at EOL
    lines = [line + '.' for line in lines]
    height = len(lines)
    width = len(lines[0])
    number = []
    for y, x in product(range(height), range(width)):
        cell = lines[y][x]
        if cell in '0123456789':
            number.append(cell)
        elif number:
            extend = len(number)
            number = int(''.join(number))
            no_symbol = True
            for sx, sy in surround(x - extend, x - 1, y, width, height):
                symbol = lines[sy][sx]
                if symbol not in '0123456789.':
                    parts.append(((sx, sy), symbol, number))
                    no_symbol = False
            if no_symbol:
                unknown.append(number)
            number = []
    return parts, unknown


def part1(data):
    parts, unknown = parse(data)
    return sum(num for pos, symbol, num in parts)


assert (result := part1(test_data)) == 4361, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    parts, unknown = parse(data)
    maybe_gears = {}
    for pos, symbol, part in parts:
        if symbol != '*':
            continue
        maybe_gears.setdefault(pos, []).append(part)
    return sum(
        part1 * other_parts[0]
        for pos, (part1, *other_parts) in maybe_gears.items()
        if len(other_parts) == 1
    )


assert (result := part2(test_data)) == 467835, f"{result=}"
print("Part 2:", part2(adv.input()))
