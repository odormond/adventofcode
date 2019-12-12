#! /usr/bin/env python

import asyncio
from itertools import product

import advent_of_code as adv

from int_code import Computer


for program, result in (
    ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
):
    computer = Computer(program)
    asyncio.get_event_loop().run_until_complete(computer.run())
    assert computer.memory == result


program = adv.input(2, adv.to_list_of_int)
computer = Computer(program[0:1] + [12, 2] + program[3:])
asyncio.get_event_loop().run_until_complete(computer.run())

print("Part one:", computer.memory[0])


target_value = 19690720
for noun, verb in product(range(100), repeat=2):
    computer = Computer(program[0:1] + [noun, verb] + program[3:])
    asyncio.get_event_loop().run_until_complete(computer.run())
    if computer.memory[0] == target_value:
        print("Part two:", 100 * noun + verb)
