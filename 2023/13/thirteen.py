#! /usr/bin/env python

import advent_of_code as adv

test_data = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

def parse(data):
    for block in data.split('\n\n'):
        as_lines = block.splitlines()
        as_columns = [
            ''.join(as_lines[l][c] for l in range(len(as_lines))) for c in range(len(as_lines[0]))
        ]
        yield as_lines, as_columns


def count_diff(image, mirror):
    diff = 0
    for i, m in zip(image, mirror):
        for a, b in zip(i, m):
            if a != b:
                diff += 1
    return diff / 2

def locate_mirror(block, smudge, axis):
    width = len(block)
    left = [pos for pos in range(1, width // 2 + 1) if count_diff(block[:pos*2], block[:pos*2][::-1]) == smudge]
    right = [width - pos for pos in range(1, width // 2 + 1) if count_diff(block[-pos*2:], block[-pos*2:][::-1]) == smudge]
    total = left + right
    if total:
        return total[0]
    else:
        return 0


def main(data, smudge):
    return sum(
        100 * locate_mirror(as_lines, smudge, 'lines') or locate_mirror(as_columns, smudge, 'cols')
        for as_lines, as_columns in parse(data)
    )


assert (result := main(test_data, 0)) == 405, f"{result=}"
print("Part 1:", main(adv.input(), 0))


assert (result := main(test_data, 1)) == 400, f"{result=}"
print("Part 2:", main(adv.input(), 1))
