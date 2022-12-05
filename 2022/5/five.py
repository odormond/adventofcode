#! /usr/bin/env python

import re

import advent_of_code as adv

test_data = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

MOVE_RE = re.compile(r'^move (\d+) from (\d+) to (\d+)$')


def parse(data):
    stack_lines, moves_lines = data.split('\n\n')
    stack_lines = stack_lines.splitlines()
    stack_ids = stack_lines.pop()
    count = int(stack_ids.strip().split().pop())
    stacks = [[] for _ in range(count)]
    for line in stack_lines[::-1]:
        for idx, stack in enumerate(stacks):
            pos = 1 + 4 * idx
            if pos > len(line) or line[pos] == ' ':
                continue
            stack.append(line[pos])

    moves = [
        tuple(int(i) for i in MOVE_RE.match(move).groups()) for move in moves_lines.splitlines()
    ]
    return stacks, moves


def do_moves(stacks, moves, reverse):
    for count, frm, to in moves:
        frm = stacks[frm - 1]
        to = stacks[to - 1]
        if reverse:
            to += frm[-count:][::-1]
        else:
            to += frm[-count:]
        del frm[-count:]


def solve(data, reverse):
    stacks, moves = parse(data)
    do_moves(stacks, moves, reverse)
    return ''.join(stack[-1] for stack in stacks)


assert solve(test_data, True) == 'CMZ'
print("Part 1:", solve(adv.input(), True))

assert solve(test_data, False) == 'MCD'
print("Part 2:", solve(adv.input(), False))
