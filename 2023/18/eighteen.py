#! /usr/bin/env python

from itertools import pairwise


import advent_of_code as adv

test_data = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


def parse_line(line):
    direction, count, color = line.split()
    count = int(count)
    color = color[1:-1]
    return DIRECTIONS[direction], count, color


def parse(data):
    return [parse_line(line) for line in data.splitlines()]


def part1(data):
    current = (0, 0)
    dug = {current}
    for (dx, dy), count, _ in parse(data):
        for _ in range(count):
            x, y = current
            current = x + dx, y + dy
            dug.add(current)
    left = min(x for (x, y) in dug)
    right = max(x for (x, y) in dug)
    top = max(y for (x, y) in dug)
    bottom = min(y for (x, y) in dug)
    x, y = left, bottom
    while (x, y) not in dug:
        x += 1
        y += 1
    queue = {(x + 1, y + 1)}
    while queue:
        x, y = queue.pop()
        dug.add((x, y))
        for dx, dy in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in dug:
                queue.add((nx, ny))
    return len(dug)

assert (result := part1(test_data)) == 62, f"{result=}"
print("Part 1:", part1(adv.input()))


def parse_line(line):
    _, _, color = line.split()
    count = int(color[2:-2], 16)
    direction = int(color[-2])
    return [(1, 0), (0, -1), (-1, 0), (0, 1)][direction], count, color


def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom
    return (0 <= t <= 1) and (0 <= u <= 1)


def inside(x, y, ox, oy, segments):
    intersections = sum(
        1 for (ax, ay), (bx, by) in segments if intersect(x, y, ox, oy, ax, ay, bx, by)
    )
    return (intersections % 2) == 1


def part2(data):
    current = (0, 0)
    dug = [current]
    for (dx, dy), count, _ in parse(data):
        x, y = current
        current = x + dx * count, y + dy * count
        dug.append(current)
    assert dug[-1] == dug[0]
    del dug[-1]
    segments = [segment for segment in zip(dug, dug[1:] + dug[:1])]

    xs = sorted({x for x, y in dug[:-1]})
    ys = sorted({y for x, y in dug[:-1]})
    out_x, out_y = xs[0] - 1, ys[0] - 1
    rectangles = [
        (x1, y1, x2, y2)
        for x1, x2 in pairwise(xs)
        for y1, y2 in pairwise(ys)
        if inside((x1 + x2)/2, (y1 + y2)/2, out_x, out_y, segments)
    ]
    surface = sum((abs(x1 - x2) - 1) * (abs(y1 - y2) - 1) for x1, y1, x2, y2 in rectangles)
    edges = set()
    corners = set()
    for x1, y1, x2, y2 in rectangles:
        corners.add((x1, y1))
        corners.add((x1, y2))
        corners.add((x2, y1))
        corners.add((x2, y2))
        edges.add((x1, y1+1, x1, y2-1))
        edges.add((x1+1, y1, x2-1, y1))
        edges.add((x1+1, y2, x2-1, y2))
        edges.add((x2, y1+1, x2, y2-1))
    
    return (
        surface
        + sum(abs(x2 - x1) + 1 if y1 == y2 else abs(y2 - y1) + 1 for x1, y1, x2, y2 in edges)
        + len(corners)
    )


assert (result := part2(test_data)) == 952408144115, f"{result=}"
print("Part 2:", part2(adv.input()))
