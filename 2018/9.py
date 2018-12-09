#! /usr/bin/env python3

import re

from advent import Inputs

PROBLEM_RE = re.compile(r'(\d+) players; last marble is worth (\d+) points')
n_players, n_marbles = map(int, PROBLEM_RE.match(Inputs(2018).get(9).text).groups())

def play(n_players, n_marbles):
    players = [0] * n_players
    circle = [0]
    current = 0
    for marble in range(1, n_marbles+1):
        if marble % 1000 == 0:
            print(f'\r{marble}', end='', flush=True)
        if marble % 23 == 0:
            current = (current - 7) % len(circle)
            players[(marble-1)%n_players] += marble + circle.pop(current)
        else:
            current = (current + 1) % len(circle) + 1
            circle.insert(current, marble)
        # print(' '.join(f'{m:2d}' for m in circle[:current]), f'({marble:2d})', ' '.join(f'{m:2d}' for m in circle[current+1:]), sep='')
    print('\r\033[K', end='')
    return players


print("Part one:", max(play(n_players, n_marbles)))

print("Part two:", max(play(n_players, n_marbles*100)))
