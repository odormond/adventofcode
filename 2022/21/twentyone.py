#! /usr/bin/env python

from operator import eq, add, sub, mul, floordiv

import advent_of_code as adv

test_data = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

OPS = {
    '==': eq,
    '+': add,
    '-': sub,
    '*': mul,
    '/': floordiv,
}


def part1(data):
    monkeys = {}
    lines = data.splitlines()
    while lines:
        line = lines.pop(0)
        monkey, job = line.split(': ')
        try:
            monkeys[monkey] = int(job)
        except ValueError:
            a, op, b = job.split()
            if a in monkeys and b in monkeys:
                monkeys[monkey] = OPS[op](monkeys[a], monkeys[b])
            else:
                lines.append(line)
    return monkeys['root']


assert (result := part1(test_data)) == 152, f"{result=}"
print("Part 1:", part1(adv.input()))


def expr(variables, var):
    if var not in variables:
        return 'x'
    if isinstance(variables[var], int):
        return variables[var]
    op, a, b = variables[var]
    return op, expr(variables, a), expr(variables, b)


INV_OPS = {
    '+': sub,
    '-': add,
    '*': floordiv,
    '/': mul,
}

def part2(data):
    monkeys = {}
    for line in data.splitlines():
        monkey, job = line.split(': ')
        if monkey == 'humn':
            continue
        try:
            monkeys[monkey] = int(job)
        except ValueError:
            a, op, b = job.split()
            if monkey == 'root':
                op = '=='
            if b == 'humn':
                assert op in ('+', '*')
                a, b = b, a
            monkeys[monkey] = op, a, b
    progress = True
    while progress:
        progress = False
        for monkey, job in monkeys.items():
            if isinstance(job, tuple):
                op, a, b = job
                if isinstance(monkeys.get(a), int) and isinstance(monkeys.get(b), int):
                    progress = True
                    monkeys[monkey] = OPS[op](monkeys[a], monkeys[b])
    op, a, b = expr(monkeys, 'root')
    while True:
        match a, b:
            case (op, (op2, c, d), e), v:  # (c op2 d) op e == v  -> (c op2 d) == v invop e
                a, b = (op2, c, d), INV_OPS[op](v, e)
            case (op, c, (op2, d, e)), v if op in '+*':  # c op (d op2 e) == v  -> (d op2 e) == v invop c  if op is commutative
                a, b = (op2, d, e), INV_OPS[op](v, c)
            case ('-', c, (op2, d, e)), v:  # c - (d op2 e) == v  -> c - v == (d op2 e)
                a, b = (op2, d, e), c - v
            case (op, 'x', c), v:  # x op c == v  -> x == v invop c
                return INV_OPS[op](v, c)
            case 'x', v:
                return v
            case _:
                raise RuntimeError(f"Unsupported case: {a} == {b}")


assert (result := part2(test_data)) == 301, f"{result=}"
print("Part 2:", part2(adv.input()))
