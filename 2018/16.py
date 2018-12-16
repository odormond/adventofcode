#! /usr/bin/env python3

from advent import Inputs

source = Inputs(2018).get(16).text


def addr(a, b, c, regs):
    regs[c] = regs[a] + regs[b]
    return regs


def addi(a, b, c, regs):
    regs[c] = regs[a] + b
    return regs


def mulr(a, b, c, regs):
    regs[c] = regs[a] * regs[b]
    return regs


def muli(a, b, c, regs):
    regs[c] = regs[a] * b
    return regs


def banr(a, b, c, regs):
    regs[c] = regs[a] & regs[b]
    return regs


def bani(a, b, c, regs):
    regs[c] = regs[a] & b
    return regs


def borr(a, b, c, regs):
    regs[c] = regs[a] | regs[b]
    return regs


def bori(a, b, c, regs):
    regs[c] = regs[a] | b
    return regs


def setr(a, b, c, regs):
    regs[c] = regs[a]
    return regs


def seti(a, b, c, regs):
    regs[c] = a
    return regs


def gtir(a, b, c, regs):
    regs[c] = 1 if a > regs[b] else 0
    return regs


def gtri(a, b, c, regs):
    regs[c] = 1 if regs[a] > b else 0
    return regs


def gtrr(a, b, c, regs):
    regs[c] = 1 if regs[a] > regs[b] else 0
    return regs


def eqir(a, b, c, regs):
    regs[c] = 1 if a == regs[b] else 0
    return regs


def eqri(a, b, c, regs):
    regs[c] = 1 if regs[a] == b else 0
    return regs


def eqrr(a, b, c, regs):
    regs[c] = 1 if regs[a] == regs[b] else 0
    return regs


instructions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def match_instruction(inst, in_regs, out_regs):
    op, a, b, c = inst
    return [i for i in instructions if i(a, b, c, in_regs[:]) == out_regs]


program = []
matches = {}
samples = 0
for line in source.splitlines():
    if not line:
        out_regs = in_regs = inst = None
        continue
    if line.startswith('Before'):
        in_regs = eval(line[8:])
    elif line.startswith('After'):
        out_regs = eval(line[8:])
        match = match_instruction(inst, in_regs, out_regs)
        if len(match) >= 3:
            samples += 1
        op, a, b, c = inst
        for fn in match:
            matches.setdefault(fn, set()).add(op)
    else:
        inst = [int(i) for i in line.split()]
        if in_regs is None:
            program.append(inst)


print("Part one:", samples)

opcodes = {}
matches = sorted(((v, k) for k, v in matches.items()), key=lambda x: len(x[0]))
while matches:
    ops, fn = matches.pop(0)
    assert len(ops) == 1
    op = ops.pop()
    opcodes[op] = fn
    for ops, dn in matches:
        if op in ops:
            ops.remove(op)
    matches.sort(key=lambda x: len(x[0]))

regs = [0, 0, 0, 0]
for op, a, b, c in program:
    opcodes[op](a, b, c, regs)

print("Part two:", regs[0])
