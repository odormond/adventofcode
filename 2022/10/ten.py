#! /usr/bin/env python

from pathlib import Path

import advent_of_code as adv


small_test_data = """\
noop
addx 3
addx -5
"""
test_data = Path('test_data').read_text()


def parse_asm(data):
    for line in data.splitlines():
        if line == 'noop':
            yield 'noop'
        else:
            op, arg = line.split()
            yield op, int(arg)


def execute(code):
    x = 1
    for instruction in code:
        match instruction:
            case 'noop':
                yield x
            case 'addx', dx:
                yield x
                yield x
                x += dx


test_small = list(execute(parse_asm(small_test_data))) 
assert test_small == [1, 1, 1, 4, 4]

def signal_strenghs(cpu):
    for cycle, signal in enumerate(cpu, 1):
        if cycle % 40 == 20:
            yield cycle * signal


test_result = list(signal_strenghs(execute(parse_asm(test_data))))
assert test_result == [420, 1140, 1800, 2940, 2880, 3960]
print("Part 1:", sum(signal_strenghs(execute(adv.input(parse_asm)))))


def display(code):
    crt = []
    for cycle, sprite_pos in enumerate(execute(code)):
        if sprite_pos-1 <= cycle % 40 <= sprite_pos + 1:
            crt.append('#')
        else:
            crt.append('.')
        if cycle % 40 == 39:
            crt.append('\n')
    return ''.join(crt)

test_crt = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""

assert display(parse_asm(test_data)) == test_crt
print("Part 2:", display(adv.input(parse_asm)), sep='\n')
