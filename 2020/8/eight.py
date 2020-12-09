#! /usr/bin/env python3

import os.path
import advent_of_code as adv


class InvalidOpcode(Exception):
    pass


class InfiniteLoop(Exception):
    pass


class OutOfCode(Exception):
    pass


class CPU:
    def __init__(self):
        self.accumulator = 0
        self.seen = set()

    def run(self, code):
        pc = 0
        while pc < len(code):
            opcode, arg = code[pc].split()
            arg = int(arg)
            if pc in self.seen:
                raise InfiniteLoop(self.accumulator)
            self.seen.add(pc)
            if opcode == "nop":
                pc += 1
            elif opcode == "acc":
                self.accumulator += arg
                pc += 1
            elif opcode == "jmp":
                pc += arg
            else:
                raise InvalidOpcode(opcode)
        raise OutOfCode(pc, self.accumulator)


TEST_CODE = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

try:
    CPU().run(TEST_CODE.strip().splitlines())
except InfiniteLoop as e:
    assert e.args == (5,)

code = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_str)
try:
    CPU().run(code)
except InfiniteLoop as e:
    print("Part 1:", *e.args)

for i in range(len(code)):
    opcode, arg = code[i].split()
    try:
        if opcode == "nop":
            CPU().run(code[:i] + [f"jmp {arg}"] + code[i + 1 :])
        elif opcode == "jmp":
            CPU().run(code[:i] + [f"nop {arg}"] + code[i + 1 :])
    except InfiniteLoop:
        pass
    except OutOfCode as e:
        pc, accumulator = e.args
        if pc == len(code):
            print("Part 2:", accumulator)
