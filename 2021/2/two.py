#! /usr/bin/env python

from functools import reduce, partial
from pathlib import Path
import advent_of_code as adv

test_data = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


def forward(amplitude, position):
    horizontal, depth = position
    return (horizontal + amplitude, depth)


def down(amplitude, position):
    horizontal, depth = position
    return (horizontal, depth + amplitude)


def up(amplitude, position):
    horizontal, depth = position
    return (horizontal, depth - amplitude)


def to_list_of_moves(forward, down, up, data):
    moves = []
    for line in data.splitlines():
        command, amplitude = line.split()
        amplitude = int(amplitude)
        match command:
            case 'forward':
                moves.append(partial(forward, amplitude))
            case 'down':
                moves.append(partial(down, amplitude))
            case 'up':
                moves.append(partial(up, amplitude))
    return moves


def pilot(moves, start):
    return reduce(lambda position, move: move(position), moves, start)


horizontal, depth = pilot(to_list_of_moves(forward, down, up, test_data), (0, 0))
assert horizontal * depth == 150

moves = adv.input(Path(__file__).parent.name, partial(to_list_of_moves, forward, down, up))
horizontal, depth = pilot(moves, (0, 0))
print("Part 1:", horizontal * depth)


def aim_forward(amplitude, position):
    horizontal, depth, aim = position
    return (horizontal + amplitude, depth + aim * amplitude, aim)


def aim_down(amplitude, position):
    horizontal, depth, aim = position
    return (horizontal, depth, aim + amplitude)


def aim_up(amplitude, position):
    horizontal, depth, aim = position
    return (horizontal, depth, aim - amplitude)


def to_list_of_aim_moves(data):
    moves = []
    for line in data.splitlines():
        command, amplitude = line.split()
        amplitude = int(amplitude)
        moves.append((AIM_COMMANDS[command], amplitude))
    return moves


horizontal, depth, aim = pilot(to_list_of_moves(aim_forward, aim_down, aim_up, test_data), (0, 0, 0))
assert horizontal * depth == 900

moves = adv.input(Path(__file__).parent.name, partial(to_list_of_moves, aim_forward, aim_down, aim_up))
horizontal, depth, aim = pilot(moves, (0, 0, 0))
print("Part 2:", horizontal * depth)
