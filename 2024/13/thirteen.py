#! /usr/bin/env python

from math import hypot
import re
import advent_of_code as aoc

test_data = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

BUTTON_RE = re.compile(r"Button [AB]: X\+(?P<x>\d+), Y\+(?P<y>\d+)")
PRIZE_RE = re.compile(r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)")


def parse_button(line):
    match = BUTTON_RE.match(line)
    return int(match.group("x")), int(match.group("y"))


def parse_prize(line):
    match = PRIZE_RE.match(line)
    return int(match.group("x")), int(match.group("y"))


def parse(data):
    machines = []
    for machine in data.strip().split("\n\n"):
        a, b, prize = machine.splitlines()
        machines.append((parse_button(a), parse_button(b), parse_prize(prize)))
    return machines


class NoSolutionError(Exception):
    pass


def closest(start, target, vector):
    sx, sy = start
    tx, ty = target
    vx, vy = vector
    a, b = tx - sx, ty - sy
    k = int((a * vx + b * vy) / (vx**2 + vy**2))
    if k <= 0:
        raise NoSolutionError
    if hypot(a - k * vx, b - k * vy) < hypot(a - (k + 1) * vx, b - (k + 1) * vy):
        return k
    return k + 1


def claw(u, v, a, b):
    ax, ay = a
    bx, by = b
    return (u * ax + v * bx, u * ay + v * by)


def solve(a, b, target):
    ax, ay = a
    bx, by = b
    minus_b = (-bx, -by)
    u, v = 0, closest((0, 0), target, b)
    backtrack_v2 = backtrack_v = 0
    while (start := claw(u, v, a, b)) != target:
        if v < 0:
            raise NoSolutionError
        try:
            u += closest(start, target, a)
        except NoSolutionError:
            if backtrack_v > 3:
                raise
            v -= 1
            backtrack_v += 1
            continue
        else:
            backtrack_v = 0
        if (start := claw(u, v, a, b)) == target:
            break
        try:
            v -= closest(start, target, minus_b)
        except NoSolutionError:
            if backtrack_v2 > 3:
                raise
            v -= 1
            backtrack_v2 += 1
            continue
        else:
            backtrack_v2 = 0
    return (u, v)


def solver(data, correction=0):
    tokens = 0
    for a, b, p in parse(data):
        px, py = p
        try:
            u, v = solve(a, b, (px + correction, py + correction))
        except NoSolutionError:
            pass
        else:
            tokens += 3 * u + v
    return tokens


def part1(data):
    return solver(data)


assert (result := part1(test_data)) == 480, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    return solver(data, 10000000000000)


print("Part 2:", part2(aoc.input()))
