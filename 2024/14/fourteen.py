#! /usr/bin/env python

import re
import sys
from time import sleep

import advent_of_code as aoc

test_data = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

ROBOT_RE = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
TEST_WIDTH, TEST_HEIGHT = 11, 7
WIDTH, HEIGHT = 101, 103

def parse(data):
    for robot in data.splitlines():
        px, py, vx, vy = map(int, ROBOT_RE.match(robot).groups())
        yield (px, py), (vx, vy)


def part1(data, width, height, time):
    q1 = q2 = q3 = q4 = 0
    for (px, py), (vx, vy) in parse(data):
        x, y = ((px + time * vx) % width, (py + time * vy) % height)
        if x < width // 2:
            if y < height // 2:
                q1 += 1
            elif height // 2 < y:
                q2 += 1
        elif width // 2 < x:
            if y < height // 2:
                q3 += 1
            elif height // 2 < y:
                q4 += 1
    return q1 * q2 * q3 * q4

assert (result := part1(test_data, TEST_WIDTH, TEST_HEIGHT, 100)) == 12, f"{result=}"
print("Part 1:", part1(aoc.input(), WIDTH, HEIGHT, 100))


def show_time(robots, time, width, height):
    print("\033[2J", end="")
    for x, y in {
        ((px + time * vx) % width, (py + time * vy) % height)
        for (px, py), (vx, vy) in robots
    }:
        print(f"\033[{y+1};{x+1}H*", end="")
    print(f"\033[{height};1H", flush=True)


def part2(data, width, height):
    robots = list(parse(data))
    time = -1
    max_42 = 0
    while True:
        print("\r\033[J", time, end="", flush=True)
        time += 1
        christmas = {
            ((px + time * vx) % width, (py + time * vy) % height)
            for (px, py), (vx, vy) in robots
        }
        fortytwo = 0
        for _, py in christmas:
            if py == 42:
                fortytwo += 1
        if fortytwo > max_42:
            max_42 = fortytwo
            show_time(robots, time, width, height)
            if input(f"42: Is this a Christmas tree ({time})?").startswith("y"):
                break
    return time

print("Part 2:", part2(aoc.input(), WIDTH, HEIGHT))
