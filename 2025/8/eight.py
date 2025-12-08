#! /usr/bin/env python

from itertools import combinations
from math import hypot, prod

import advent_of_code as aoc

test_data = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

def parse(data):
    return [tuple(int(v) for v in line.split(",")) for line in data.splitlines()]


def distance(a, b):
    return hypot(*(u - v for u, v in zip(a, b, strict=True)))


def solver(data, count=None):
    boxes = parse(data)
    ordered_pairs = sorted(combinations(boxes, 2), key=lambda pair: distance(pair[0], pair[1]))
    if count is None:
        count = len(ordered_pairs)
    circuits = []
    for a, b in ordered_pairs[:count]:
        link = []
        for i, circuit in enumerate(circuits):
            if a in circuit or b in circuit:
                link.append(i)
        if link:
            union = {a, b}
            for i in link:
                union |= circuits[i]
            circuits = [circuit for i, circuit in enumerate(circuits) if i not in link] + [union]
        else:
            circuits.append({a, b})
        if len(circuits) == 1 and len(circuits[0]) == len(boxes):
            return a[0] * b[0]
    return prod(sorted(len(circuit) for circuit in circuits)[-3:])


assert (result := solver(test_data, 10)) == 40, f"{result=}"
print("Part 1:", solver(aoc.input(), 1000))


assert (result := solver(test_data)) == 25272, f"{result=}"
print("Part 2:", solver(aoc.input()))
