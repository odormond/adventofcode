#! /usr/bin/env python

from itertools import combinations

import advent_of_code as adv

test_data = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

def parse(data):
    for line in data.splitlines():
        pos, speed = line.split(' @ ')
        pos = tuple(int(a) for a in pos.split(', '))
        speed = tuple(int(a) for a in speed.split(', '))
        yield pos, speed


LOW = 200000000000000
HI = 400000000000000


def intersect(x1, y1, vx, vy, x3, y3, wx, wy, low, hi):
    x2, y2 = (x1 + vx), (y1 + vy)
    x4, y4 = (x3 + wx), (y3 + wy)
    abx, aby = (x1 - x3), (y1 - y3)
    denom = vx * wy - vy * wx
    if denom == 0:
        # Parallel
        # Common point
        common = None
        for (x, y) in {(x1, y1), (x2, y2)} & {(x3, y3), (x4, y4)}:
            common = False
            if low <= x <= hi and low <= y <= hi:
                return x, y
        if common is not None:
            return common
        # Collinear: a = b + v * t => a - b = v * t => (a - b)_x / v_x == (a - b)_y / v_y
        if (
            (vx == 0 and abx == 0)
            or (vy == 0 and aby == 0)
            or (
                abx**2 / (abx**2 + aby**2) == vx**2 / (vx**2 + vy**2)
                and aby**2 / (abx**2 + aby**2) == vy**2 / (vx**2 + vy**2)
            )
        ):
            wvx, wvy = (wx - vx), (wy - vy)
            t = (abx / wvx) if wvx else (aby / wvy)
            x, y = x1 + vx * t, y1 + vy * t
            if t >= 0 and low <= x <= hi and low <= y <= hi:
                return x, y
            else:
                return False
        else:
            return False
    t = (aby * wx - abx * wy) / denom
    u = (aby * vx - abx * vy) / denom
    x, y = x1 + vx * t, y1 + vy * t
    if t >= 0 and u >= 0 and low <= x <= hi and low <= y <= hi:
        return x, y
    return False


def part1(data, low, hi):
    return sum(
        1
        for ((x1, y1, z1), (vx, vy, vz)), ((x3, y3, z3), (wx, wy, wz)) in combinations(parse(data), r=2)
        if intersect(x1, y1, vx, vy, x3, y3, wx, wy, low, hi)
    )


assert (result := part1(test_data, 7, 27)) == 2, f"{result=}"
print("Part 1:", part1(adv.input(), LOW, HI))


def part2(data):
    return parse(data)


# assert (result := part2(test_data)) == "", f"{result=}"
# print("Part 2:", part2(adv.input()))
