#! /usr/bin/env python

import asyncio
from itertools import product

import advent_of_code as adv

from int_code import Computer


def check_and_get_status_code(computer):
    status_code = 0
    while not computer.outputs.empty():
        assert status_code == 0
        status_code = computer.outputs.get_nowait()
    return status_code


TEST = adv.input(5, adv.to_list_of_int)
computer = Computer(TEST)
computer.inputs.put_nowait(1)
asyncio.get_event_loop().run_until_complete(computer.run())
status_code = check_and_get_status_code(computer)
print("Part one:", status_code)


for program, inputs, outputs in (
    ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], (0, 8), (0, 1)),
    ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], (0, 8), (1, 0)),
    ([3, 3, 1108, -1, 8, 3, 4, 3, 99], (0, 8), (0, 1)),
    ([3, 3, 1107, -1, 8, 3, 4, 3, 99], (0, 8), (1, 0)),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], (0, 2), (0, 1)),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], (0, 2), (0, 1)),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], (0, 8, 16), (999, 1000, 1001)),
):
    for input_, output in zip(inputs, outputs):
        computer = Computer(program[:])
        computer.inputs.put_nowait(input_)
        asyncio.get_event_loop().run_until_complete(computer.run())
        status_code = check_and_get_status_code(computer)
        assert status_code == output


computer = Computer(TEST)
computer.inputs.put_nowait(5)
asyncio.get_event_loop().run_until_complete(computer.run())
status_code = check_and_get_status_code(computer)
print("Part two:", status_code)
