#! /usr/bin/env python

import advent_of_code as aoc

test_data = """2333133121414131402"""


def parse(data):
    layout = []
    f = 0
    for i, c in enumerate(data.strip()):
        if i % 2 == 0:
            layout += [f] * int(c)
            f += 1
        else:
            layout += [None] * int(c)
    return layout


def part1(data):
    layout = parse(data)
    while layout[-1] is None:
        layout.pop()
    compact = layout[:]
    i = 0
    while i < len(compact):
        if compact[i] is None:
            compact[i] = compact.pop()
            while compact[-1] is None:
                compact.pop()
        i += 1
    return sum(b * f for b, f in enumerate(compact))


assert (result := part1(test_data)) == 1928, f"{result=}"
print("Part 1:", part1(aoc.input()))


def parse(data):
    layout = []
    f = 0
    b = 0
    for i, c in enumerate(data.strip()):
        c = int(c)
        if i % 2 == 0:
            layout.append((b, c, f))
            f += 1
        else:
            layout.append((b, c, None))
        b += c
    return layout


def holes(layout):
    pb, pc, _ = layout[0]
    for i, (b, c, _) in enumerate(layout[1:], 1):
        if pb + pc < b:
            yield i, (pb + pc), (b - pb - pc)
        pb, pc = b, c


def part2(data):
    layout = parse(data)
    compact = [(b, c, f) for b, c, f in layout if f is not None]
    for b, c, f in reversed(layout):
        if f is None:
            continue
        for i, hb, hc in holes(compact):
            if hb < b and hc >= c:
                compact.insert(i, (hb, c, f))
                compact.remove((b, c, f))
                break
    return sum((b + i) * f for b, c, f in compact for i in range(c) if f is not None)



assert (result := part2(test_data)) == 2858, f"{result=}"
print("Part 2:", part2(aoc.input()))
