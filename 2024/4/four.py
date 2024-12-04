#! /usr/bin/env python

from itertools import product

import advent_of_code as aoc

test_data = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

NEEDLE = tuple('XMAS')

def parse(data):
    return {
        (l, c): x
        for l, line in enumerate(data.splitlines())
        for c, x in enumerate(line)
    }

def part1(l, c):
    for dl, dc in product((-1, 0, 1), repeat=2):
        if (dl, dc) == (0, 0):
            continue
        yield [(l + dl * n, c + dc * n, x) for n, x in enumerate(NEEDLE)]


def solver(data, needle_placer):
    count = 0
    grid = parse(data)
    for (l, c) in grid:
        for letters in needle_placer(l, c):
            for tl, tc, x in letters:
                if grid.get((tl, tc)) != x:
                    break
            else:
                count += 1
    return count


assert (result := solver(test_data, part1)) == 18, f"{result=}"
print("Part 1:", solver(aoc.input(), part1))


test_data = """\
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
"""

def part2(l, c):
    return [
        [(l-1, c-1, "M"), (l, c, "A"), (l+1, c+1, "S"), (l+1, c-1, "M"), (l-1, c+1, "S")],
        [(l-1, c-1, "M"), (l, c, "A"), (l+1, c+1, "S"), (l-1, c+1, "M"), (l+1, c-1, "S")],
        [(l+1, c+1, "M"), (l, c, "A"), (l-1, c-1, "S"), (l+1, c-1, "M"), (l-1, c+1, "S")],
        [(l+1, c+1, "M"), (l, c, "A"), (l-1, c-1, "S"), (l-1, c+1, "M"), (l+1, c-1, "S")],
    ]


assert (result := solver(test_data, part2)) == 9, f"{result=}"
print("Part 2:", solver(aoc.input(), part2))
