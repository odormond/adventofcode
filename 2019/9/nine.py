#! /usr/bin/env python

import asyncio
from itertools import product, permutations

import advent_of_code as adv

from int_code import Computer


async def day_2():
    for program, result in (
        ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ):
        computer = Computer(program)
        await computer.run()
        assert computer.memory == result

    # part one
    program = adv.input(2, adv.to_list_of_int)
    computer = Computer(program[0:1] + [12, 2] + program[3:])
    await computer.run()
    assert computer.memory[0] == 2894520

    # part two
    target_value = 19690720
    for noun, verb in product(range(100), repeat=2):
        computer = Computer(program[0:1] + [noun, verb] + program[3:])
        await computer.run()
        if computer.memory[0] == target_value:
            assert 100 * noun + verb == 9342
            break
asyncio.run(day_2())


async def day_5():
    TEST = adv.input(5, adv.to_list_of_int)
    computer = Computer(TEST)
    await computer.inputs.put(1)
    await computer.run()


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
            computer = Computer(program)
            await computer.inputs.put(input_)
            await computer.run()
            out = await computer.outputs.get()
            assert out == output, f"{out} == {output}"


    TEST = adv.input(5, adv.to_list_of_int)
    computer = Computer(TEST)
    await computer.inputs.put(5)
    await computer.run()

asyncio.run(day_5())


async def tune_amplifiers(code):
    best_thrust = 0
    best_phases = None
    for phases in permutations(range(5), 5):
        inp = 0
        for p in phases:
            amp = Computer(code)
            await amp.inputs.put(p)
            await amp.inputs.put(inp)
            await amp.run()
            inp = await amp.outputs.get()
        if inp > best_thrust:
            best_thrust = inp
            best_phases = phases
    return best_phases, best_thrust


for code, phases, thrust in (
    ([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], (4, 3, 2, 1, 0), 43210),
    ([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], (0, 1, 2, 3, 4), 54321),
    ([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], (1, 0, 4, 3, 2), 65210),
):
    assert asyncio.run(tune_amplifiers(code)) == (phases, thrust)

best_phases, best_thrust = asyncio.run(tune_amplifiers(adv.input(7, adv.to_list_of_int)))


async def tune_loop(code):
    best_thrust = 0
    best_phases = None
    for phases in permutations(range(5, 10), 5):
        in_queue = None
        amps = []
        for p in phases:
            amp = Computer(code, inputs=in_queue)
            amps.append(amp)
            in_queue = amp.outputs
            await amp.inputs.put(p)
        amps[-1].outputs = amps[0].inputs
        await amps[0].inputs.put(0)
        await asyncio.gather(*(a.run() for a in amps))
        thrust = await amps[-1].outputs.get()
        if thrust > best_thrust:
            best_thrust = thrust
            best_phases = phases
    return best_phases, best_thrust


for code, phases, thrust in (
    ([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5], (9, 8, 7, 6, 5), 139629729), 
    ([3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10], (9, 7, 8, 5, 6), 18216), 
):
    assert asyncio.run(tune_loop(code)) == (phases, thrust)

best_phases, best_thrust = asyncio.run(tune_loop(adv.input(7, adv.to_list_of_int)))


async def test_9_1():
    code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    computer = Computer(code)
    await computer.run()
    for data in code:
        assert computer.outputs.get_nowait() == data
asyncio.run(test_9_1())

async def test_9_2():
    code = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    computer = Computer(code)
    await computer.run()
    out = computer.outputs.get_nowait()
    assert int(out) and len(str(out)) == 16
asyncio.run(test_9_2())

async def test_9_3():
    computer = Computer([104, 1125899906842624, 99])
    await computer.run()
    assert computer.outputs.get_nowait() == 1125899906842624
asyncio.run(test_9_3())


program = adv.input(9, adv.to_list_of_int)
async def nine_part_one():
    computer = Computer(program)
    await computer.inputs.put(1)
    await computer.run()
    boost_key_code = computer.outputs.get_nowait()
    assert computer.outputs.empty()
    return boost_key_code
boost_key_code = asyncio.run(nine_part_one())
print("Part one:", boost_key_code)


async def nine_part_two():
    computer = Computer(program)
    await computer.inputs.put(2)
    await computer.run()
    distress_coordinates = computer.outputs.get_nowait()
    assert computer.outputs.empty()
    return distress_coordinates
distress_coordinates = asyncio.run(nine_part_two())
print("Part two:", distress_coordinates)
