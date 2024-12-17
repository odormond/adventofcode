#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

def parse(data):
    a, b, c, _, prog = data.strip().splitlines()
    a = int(a.split()[-1])
    b = int(b.split()[-1])
    c = int(c.split()[-1])
    prog = [int(v) for v in prog.split()[-1].split(",")]
    return a, b, c, prog


def combo(a, b, c, o):
    match o:
        case 4:
            return a
        case 5:
            return b
        case 6:
            return c
        case 7:
            print("invalid")
            raise SystemExit(1)
        case _:
            return o


def adv(a, b, c, o, pc):
    numerator = a
    denominator = 1 << combo(a, b, c, o)
    return numerator // denominator, b, c, pc


def bxl(a, b, c, o, pc):
    return a, b ^ o, c, pc


def bst(a, b, c, o, pc):
    return a, combo(a, b, c, o) % 8, c, pc


def jnz(a, b, c, o, pc):
    if a != 0:
        pc = o
    return a, b, c, pc


def bxc(a, b, c, o, pc):
    return a, b ^ c, c, pc


def bdv(a, b, c, o, pc):
    numerator = a
    denominator = 1 << combo(a, b, c, o)
    return a, numerator // denominator, c, pc


def cdv(a, b, c, o, pc):
    numerator = a
    denominator = 1 << combo(a, b, c, o)
    return a, b, numerator // denominator, pc


def run(a, b, c, prog):
    output = []
    def out(a, b, c, o, pc):
        output.append(combo(a, b, c, o) % 8)
        return a, b, c, pc

    ops = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    pc = 0
    while pc < len(prog):
        opcode = prog[pc]
        operand = prog[pc + 1]
        pc += 2
        a, b, c, pc = ops[opcode](a, b, c, operand, pc)
    return output, a, b, c


assert run(0, 0, 9, [2, 6])[2] == 1
assert run(10, 0, 0, [5, 0, 5, 1, 5, 4])[0] == [0, 1, 2]
assert run(2024, 0, 0, [0, 1, 5, 4, 3, 0])[:2] == ([4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0], 0)
assert run(0, 29, 0, [1, 7])[2] == 26
assert run(0, 2024, 43690, [4, 0])[2] == 44354


def part1(data):
    a, b, c, prog = parse(data)
    return ",".join(map(str, run(a, b, c, prog)[0]))


assert (result := part1(test_data)) == "4,6,3,5,6,3,5,2,1,0", f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    a, b, c, prog = parse(data)
    for a in range(8 ** (len(prog) - 1), 8 ** len(prog)):
        output, _, _, _ = run(a, b, c, prog)
        print("\r\033[J", a, "/", 8**len(prog), end="", flush=True)
        if output == prog:
            print()
            return a


"""
2,4, 1,5, 7,5, 1,6, 0,3, 4,3, 5,5, 3,0
                                     v
                                     3

a = 0b11???

bst(4)  b = a % 8                                 24  25  30  31          29
bxl(5)  b = b ^ 5         b^3 == a >> b^5 2   3   0   1   6   7     4     5
cdv(5)  c = a // 2**b                     7>0 6>0 5>0 4>1 3>2 2>6-7 1>4-7 0>0-7
bxl(6)  b = b ^ 6         b^6 == a >> b   1   0   3   2   5   4     7     6
adv(3)  a = a // 2**3  => 8**(len(prog)-1) <= a < 8**len(prog)
bxc(3)  b = b ^ c         b == c                  0^3 1^2     4^7         5^6
out(5)  out b % 8         0               3
jnz(0)  jump if a != 0
"""


def part2(data):
    a, b, c, prog = parse(data)
    output = []
    a = 0
    while output != prog:
        if output == prog[-len(output):]:
            a *= 8
        else:
            a += 1
        output, *_ = run(a, b, c, prog)
    return a


test_data = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

assert (result := part2(test_data)) == 117440, f"{result=}"
print("Part 2:", part2(aoc.input()))
