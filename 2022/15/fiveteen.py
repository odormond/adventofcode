#! /usr/bin/env python

from itertools import product
import re

import advent_of_code as adv

test_data = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

SENSOR_BEACON_RE = re.compile(r'Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)')


def distance(sx, sy, ex, ey):
    return abs(sx - ex) + abs(sy - ey)


def parse(data):
    sensors = []
    for line in data.splitlines():
        sx, sy, bx, by = tuple(map(int, SENSOR_BEACON_RE.match(line).groups()))
        sensors.append(((sx, sy), (bx, by), distance(sx, sy, bx, by)))
    return sensors


def part1(data, scan_y):
    excluded = set()
    beacons = set()
    for (sx, sy), beacon, r in parse(data):
        beacons.add(beacon)
        if sy - r <= scan_y <= sy + r:
            half_width = r - abs(sy - scan_y)
            for x in range(sx - half_width, sx + half_width + 1):
                excluded.add((x, scan_y))
    return len(excluded - beacons)


assert (result := part1(test_data, 10)) == 26, f"{result=}"
print("Part 1:", part1(adv.input(), 2000000))


def part2(data, side):
    sensors = sorted(((r, pos) for pos, _, r in parse(data)), reverse=True)
    for y in range(side + 1):
        x = 0
        while x <= side:
            for r, (sx, sy) in sensors:
                if distance(sx, sy, x, y) <= r:
                    x = sx + r - abs(sy - y)
                    break
            else:
                return x * 4000000 + y
            x += 1


assert (result := part2(test_data, 20)) == 56000011, f"{result=}"
print("Part 2:", part2(adv.input(), 4000000))
