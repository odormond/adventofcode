#! /usr/bin/env python3

import itertools

from advent import Inputs

source = Inputs(2018).get(13).text

railway_map = [list(line) for line in source.splitlines()]

original_carts = []
for y, line in enumerate(railway_map):
    for x, cart in enumerate(line[:]):
        if cart in '><^v':
            line[x] = {'>': '-', '<': '-', 'v': '|', '^': '|'}[cart]
            original_carts.append((y, x, cart, 'l'))


def print_map(plan, carts):
    carts = {(y, x): c for y, x, c, t in carts}
    rendered = '\n'.join(''.join(carts.get((y, x), l) for x, l in enumerate(line))
                         for y, line in enumerate(plan))
    for c in '><^v':
        rendered = rendered.replace(c, '\033[7m'+c+'\033[27m')
    rendered = rendered.replace('X', '\033[41mX\033[49m')
    print('\033[2J\033[1;1H'+rendered, flush=True)


def tick(plan, state, clear_crash=False):
    new_state = []
    occupied = {(y, x) for y, x, c, t in state}
    crash = False
    state = sorted(state)
    while state:
        y, x, c, t = state.pop(0)
        occupied.remove((y, x))
        y, x, c, t = tick_cart(plan, (y, x, c, t))
        if (y, x) in occupied:
            crash = (y, x)
            c = 'X'
        new_state.append((y, x, c, t))
        occupied.add((y, x))
        if crash:
            if clear_crash:
                occupied.remove((y, x))
                new_state = [cart for cart in new_state if cart[:2] != (y, x)]
                state = [cart for cart in state if cart[:2] != (y, x)]
                crash = False
            else:
                return [(ry, rx, ('X' if (ry, rx) == (y, x) else c), t)
                        for ry, rx, c, t in new_state + state], crash
    return new_state, crash


def tick_cart(plan, cart):
    y, x, c, t = cart
    y, x = map(sum, zip((y, x), {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}[c]))
    p = plan[y][x]
    if p in '/':
        c = {'>': '^', '<': 'v', '^': '>', 'v': '<'}[c]
    elif p in '\\':
        c = {'>': 'v', '<': '^', '^': '<', 'v': '>'}[c]
    elif p == '+':
        c = {'>': {'l': '^', 'r': 'v'},
             '<': {'l': 'v', 'r': '^'},
             '^': {'l': '<', 'r': '>'},
             'v': {'l': '>', 'r': '<'},
             }[c].get(t, c)
        t = {'l': 's', 's': 'r', 'r': 'l'}[t]
    return y, x, c, t


carts = original_carts[:]
crash = False
while crash is False:
    carts, crash = tick(railway_map, carts)
# print_map(railway_map, carts)
y, x = crash
print(f"Part one: {x},{y}")

carts = original_carts[:]
count = 0
while len(carts) > 1:
    count += 1
    carts, _ = tick(railway_map, carts, True)
# print_map(railway_map, carts)
y, x, c, t = carts[0]
print(f"Part two: {x},{y}")
