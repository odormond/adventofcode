#! /usr/bin/env python3

import itertools
import os.path
import advent_of_code as adv

TEST_PROG = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".strip().splitlines()


def to_mask(line):
    mask = line.split(' = ')[1]
    and_mask = int(mask.replace('X', '1'), 2)
    or_mask = int(mask.replace('X', '0'), 2)
    return and_mask, or_mask


def interpret_v1(line, mask, mem):
    if line.startswith('mask'):
        mask = to_mask(line)
    else:
        op, value = line.split(' = ')
        value = int(value)
        addr = int(op[op.rfind('[') + 1 : -1])
        mem[addr] = value & mask[0] | mask[1]
    return mask, mem


def run(prog, interpreter):
    mask = 0, 0
    mem = {}
    for line in prog:
        mask, mem = interpreter(line, mask, mem)
    return sum(mem.values())


assert run(TEST_PROG, interpret_v1) == 165

program = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_str)
print("Part 1:", run(program, interpret_v1))


def masked_set(addr, mask, value):
    mask = mask[::-1]
    floating = [i for i, m in enumerate(mask) if m == 'X']
    addr = sum(1 << i for i in range(36) if mask[i] == '1' or mask[i] == '0' and (addr & (1 << i)))
    return {
        addr | sum(b << shift for b, shift in zip(bits, floating)): value
        for bits in itertools.product((0, 1), repeat=len(floating))
    }


def interpret_v2(line, mask, mem):
    if line.startswith('mask'):
        mask = line.split(' = ')[1]
    else:
        op, value = line.split(' = ')
        value = int(value)
        addr = int(op[op.rfind('[') + 1 : -1])
        mem.update(masked_set(addr, mask, value))
    return mask, mem


TEST_PROG_v2 = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""".strip().splitlines()

assert run(TEST_PROG_v2, interpret_v2) == 208

print("Part 2:", run(program, interpret_v2))
