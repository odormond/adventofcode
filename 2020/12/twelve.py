#! /usr/bin/env python3

import os.path
from functools import partial

import advent_of_code as adv

TEST = """
F10
N3
F7
R90
F11
"""


def rotate(dx, dy, count):
    for i in range(count):
        dx, dy = dy, -dx
    return dx, dy


def ship_move(x, y, dx, dy, mx=0, my=0, val=0, rot=partial(rotate, count=0)):
    return x + mx + dx * val, y + my + dy * val, *rot(dx, dy)


def to_moves(text, move):
    moves = []
    for instruction in text.strip().splitlines():
        op, val = instruction[0], int(instruction[1:])
        INST = {
            "F": {"val": val},
            "N": {"my": val},
            "E": {"mx": val},
            "S": {"my": -val},
            "W": {"mx": -val},
            "R": {"rot": partial(rotate, count=val // 90)},
            "L": {"rot": partial(rotate, count=4 - val // 90)},
        }
        moves.append(partial(move, **INST[op]))
    return moves


def navigate(moves, *ship):
    for move in moves:
        ship = move(*ship)
    return sum(map(abs, ship[:2]))


assert navigate(to_moves(TEST, ship_move), 0, 0, 1, 0) == 25

instructions = adv.input(int(os.path.basename(os.path.dirname(__file__))), str)
print("Part 1:", navigate(to_moves(instructions, ship_move), 0, 0, 1, 0))


def waypoint_move(x, y, dx, dy, mx=0, my=0, val=0, rot=partial(rotate, count=0)):
    dx += mx
    dy += my
    return x + dx * val, y + dy * val, *rot(dx, dy)


assert navigate(to_moves(TEST, waypoint_move), 0, 0, 10, 1) == 286

print("Part 2:", navigate(to_moves(instructions, waypoint_move), 0, 0, 10, 1))
