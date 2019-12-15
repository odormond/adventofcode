#! /usr/bin/env python

import asyncio
from collections import defaultdict
import advent_of_code as adv

from int_code import Computer


def turn_and_move(position, direction, turn):
    """direction is 0, 1, 2, 3 for up, right, down, left
    turn is 0 for left and 1 for right
    """
    direction = (direction + (turn if turn else -1)) % 4
    x, y = position
    dx, dy = ((0, 1), (1, 0), (0, -1), (-1, 0))[direction]
    return (x+dx, y+dy), direction


brain = adv.input(11, adv.to_list_of_int)
hull = defaultdict(lambda: 0)
computer = Computer(brain)
async def robot():
    position = (0, 0)
    direction = 0
    while True:
        await computer.inputs.put(hull[position])
        hull[position] = await computer.outputs.get()  # paint with returned color
        turn = await computer.outputs.get()  # which side to turn
        position, direction = turn_and_move(position, direction, turn)
asyncio.get_event_loop().run_until_complete(asyncio.wait((robot(), computer.run()), return_when=asyncio.FIRST_COMPLETED))
print("Part one:", len(hull))
input("Press enter to continue")

hull = defaultdict(lambda: 0)
computer = Computer(brain)
hull[(0, 0)] = 1
asyncio.get_event_loop().run_until_complete(asyncio.wait((robot(), computer.run()), return_when=asyncio.FIRST_COMPLETED))
xoff = -min(x for (x, y), color in hull.items() if color == 1) + 1
ymin = min(y for (x, y), color in hull.items() if color == 1)
ymax = max(y for (x, y), color in hull.items() if color == 1) + 1
display = ["\033[2J"]
for (x, y), color in hull.items():
    if color == 0:
        continue
    display.append(f"\033[{ymax-y};{x+xoff}H#")
display.append(f"\033[{ymax-ymin+1};0H")
print(''.join(display))
