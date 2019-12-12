#! /usr/bin/env python

import asyncio
from itertools import product, permutations

import advent_of_code as adv

from int_code import Computer


async def tune_amplifiers(code):
    best_thrust = 0
    best_phases = None
    for phases in permutations(range(5), 5):
        inp = 0
        for p in phases:
            amp = Computer(code[:])
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
print("Part one:", best_thrust)


async def tune_loop(code):
    best_thrust = 0
    best_phases = None
    for phases in permutations(range(5, 10), 5):
        in_queue = None
        amps = []
        for p in phases:
            amp = Computer(code[:], inputs=in_queue)
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
print("Part two:", best_thrust)
