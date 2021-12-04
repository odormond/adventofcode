#! /usr/bin/env python3

from advent import Inputs

source = Inputs(2018).get(21).text


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


instructions = {op.__name__: op for op in [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]}


def run(program, regs, ip_reg):
    ip = regs[ip_reg]
    while 0 <= ip < len(program):
        op, a, b, c = program[ip]
        regs[ip_reg] = ip
        regs = instructions[op](a, b, c, regs)
        ip = regs[ip_reg] + 1
    return ip, regs


def compile(source):
    source = source.splitlines()
    ip_reg = int(source.pop(0).split()[1])
    return ip_reg, [(op, int(a), int(b), int(c)) for op, a, b, c in (line.split() for line in source)]


ip_reg, program = compile(source)
program[28] = ('seti', 100, 0, ip_reg)
regs = [0, 0, 0, 0, 0, 0]
print("Part one:", run(program, regs, ip_reg)[1][5])

regs = [0, 0, 0, 0, 0, 0]
exits = set()
while True:
    prev_f = regs[5]
    ip, regs = run(program, regs, ip_reg)
    f = regs[5]
    if f in exits:
        break
    exits.add(f)
    regs[ip_reg] = 6
print("Part two:", prev_f)
