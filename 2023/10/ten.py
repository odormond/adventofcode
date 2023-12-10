#! /usr/bin/env python

from itertools import product

import advent_of_code as adv

test_data = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""

test_data_2 = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

test_data_3 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

test_data_4 = """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

CONNECTIONS = {
    '|': ((0, -1), (0, 1)),
    '-': ((-1, 0), (1, 0)),
    'L': ((0, -1), (1, 0)),
    'J': ((-1, 0), (0, -1)),
    '7': ((-1, 0), (0, 1)),
    'F': ((0, 1), (1, 0)),
    '.': (),
}


def parse(data):
    data = data.splitlines()
    width = len(data[0])
    height = len(data)
    pipes = {}
    for y, line in enumerate(data):
        for x, pipe in enumerate(line):
            if pipe == 'S':
                start = (x, y)
                continue
            pipes[(x, y)] = sorted(
                (tx, ty)
                for dx, dy in CONNECTIONS[pipe]
                if 0 <= (tx := x + dx) < width and 0 <= (ty := y + dy) < height
            )
    sx, sy = start
    connecting = sorted(
        (tx, ty)
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1))
        if 0 <= (tx := sx + dx) < width and 0 <= (ty := sy + dy) < height
        and (sx, sy) in pipes[(tx, ty)]
    )
    assert len(connecting) == 2
    pipes[start] = connecting
    return start, pipes


def find_loop(start, pipes):
    cursors = pipes[start]
    prevs = [start] * 2
    loop = {start, *cursors}
    while cursors[0] != cursors[1]:
        for i, (cursor, prev) in enumerate(zip(cursors, prevs)):
            tmp = pipes[cursor][:]
            tmp.remove(prev)
            cursors[i] = tmp[0]
            prevs[i] = cursor
            loop.add(tmp[0])
    return loop


def part1(data):
    loop = find_loop(*parse(data))
    return len(loop) // 2


assert (result := part1(test_data)) == 4, f"{result=}"
assert (result := part1(test_data_2)) == 4, f"{result=}"
assert (result := part1(test_data_3)) == 8, f"{result=}"
assert (result := part1(test_data_4)) == 8, f"{result=}"
print("Part 1:", part1(adv.input()))


test_data_5 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

test_data_6 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

test_data_7 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


def close_segment(segment):
    if segment == []:
        return 0
    elif len(segment) == 1:
        return 1
    else:
        a, *_, b = segment
        if (a, b) in (('F', 'J'), ('L', '7'), ('7', 'L')):
            return 1
        else:
            return 2


def compact(pipes, horizontal):
    compacted = 0
    segment = []
    for p in pipes:
        if p == '.':
            compacted += close_segment(segment)
            segment = []
        else:
            if (not horizontal and p == '-') or (horizontal and p == '|'):
                compacted += 1
                segment = []
                continue
            segment.append(p)
            if (not horizontal and p in 'JL') or (horizontal and p in 'J7'):
                compacted += close_segment(segment)
                segment = []
    compacted += close_segment(segment)
    return compacted


def part2(data):
    lines = data.splitlines()
    width = len(lines[0])
    height = len(lines)
    grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    start, pipes = parse(data)
    loop = find_loop(start, pipes)
    inside = 0
    for x, y in product(range(width), range(height)):
        if (x, y) in loop:
            continue
        west = compact([grid[(ex, y)] if (ex, y) in loop else '.' for ex in range(x)], True)
        east = compact([grid[(ex, y)] if (ex, y) in loop else '.' for ex in range(x + 1, width)], True)
        north = compact([grid[(x, ey)] if (x, ey) in loop else '.' for ey in range(y)], False)
        south = compact([grid[(x, ey)] if (x, ey) in loop else '.' for ey in range(y + 1, height)], False)
        if min(west, east, north, south) % 2 == 1:
            inside += 1
    return inside


assert (result := part2(test_data_5)) == 4, f"{result=}"
assert (result := part2(test_data_6)) == 8, f"{result=}"
assert (result := part2(test_data_7)) == 10, f"{result=}"
print("Part 2:", part2(adv.input()))
