#! /usr/bin/env python

import advent_of_code as adv


test_data = """\
A Y
B X
C Z
"""

ROCK = 1
PAPER = 2
SCISOR = 3
LOSE = 0
DRAW = 3
WIN = 6

POINTS = {
    ('A', 'X'): ROCK + DRAW,
    ('A', 'Y'): PAPER + WIN,
    ('A', 'Z'): SCISOR + LOSE,
    ('B', 'X'): ROCK + LOSE,
    ('B', 'Y'): PAPER + DRAW,
    ('B', 'Z'): SCISOR + WIN,
    ('C', 'X'): ROCK + WIN,
    ('C', 'Y'): PAPER + LOSE,
    ('C', 'Z'): SCISOR + DRAW,
}


def play(moves, points):
    return sum(points[move] for move in moves)


def to_moves(data):
    return [tuple(line.strip().split()) for line in data.splitlines()]


assert play(to_moves(test_data), POINTS) == 15
print("Part 1:", play(adv.input(to_moves), POINTS))


POINTS = {
    ('A', 'X'): SCISOR + LOSE,
    ('A', 'Y'): ROCK + DRAW,
    ('A', 'Z'): PAPER + WIN,
    ('B', 'X'): ROCK + LOSE,
    ('B', 'Y'): PAPER + DRAW,
    ('B', 'Z'): SCISOR + WIN,
    ('C', 'X'): PAPER + LOSE,
    ('C', 'Y'): SCISOR + DRAW,
    ('C', 'Z'): ROCK + WIN,
}

assert play(to_moves(test_data), POINTS) == 12
print("Part 2:", play(adv.input(to_moves), POINTS))
