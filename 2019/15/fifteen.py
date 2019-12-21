#! /usr/bin/env python

import asyncio
import os

import advent_of_code as adv
from int_code import Computer


MOVES = {
    # direction: (undo direction, (dx, dy))
    1: (2, (0, -1)),
    2: (1, (0, 1)),
    3: (4, (1, 0)),
    4: (3, (-1, 0)),
}
WALL = 0
OXIM = 2
SENSED = '#.os'
DROID = adv.input(15, adv.to_list_of_int)

COLS, LINES = os.get_terminal_size()
CX = COLS // 2
CY = LINES // 2


def draw(mapping, pos):
    x, y = pos
    sym = mapping[pos]
    print(f"\033[{CY+y};{CX+x}H{SENSED[sym]}", end='', flush=True)


async def droid():
    print("\033[2J", end='')
    computer = Computer(DROID)
    mapping = {(0, 0): 3}
    async def pilot():
        undos = []
        pos = (0, 0)
        def next_move():
            for move, (undo, (dx, dy)) in MOVES.items():
                x, y = pos
                new_pos = x+dx, y+dy
                if new_pos not in mapping:
                    undos.append((undo, pos))
                    return move, new_pos
            if undos:
                undo = undos.pop()
                return undo
            return None

        draw(mapping, pos)
        move = next_move()
        while move:
            cmd, pos = move
            await computer.inputs.put(cmd)
            sensed = await computer.outputs.get()
            mapping[pos] = sensed
            draw(mapping, pos)
            if sensed == WALL:
                _, pos = undos.pop()
            move = next_move()

    await asyncio.wait((computer.run(), pilot()), return_when=asyncio.FIRST_COMPLETED)
    return mapping

mapping = asyncio.run(droid())
print(f"\033[{CY};{CX}Hs\033[1;1H", end='')
input("Press enter to continue")

oxim = [pos for pos, sym in mapping.items() if sym == OXIM][0]


def colorize(mapping, start):
    def neighbours(distances, pos):
        x, y = pos
        for _, (dx, dy) in MOVES.values():
            neigh = x+dx, y+dy
            if neigh in distances and distances[neigh] is None:
                yield neigh

    def color(pos, value):
        x, y = pos
        print(f"\033[{CY+y};{CX+x}H{str(value)[-1]}", end='', flush=True)

    print("\033[2J", end='')
    distances = {pos: None for pos, sym in mapping.items() if sym != WALL}
    next_color = 0
    to_color = {start}
    while to_color:
        next_to_color = set()
        for pos in to_color:
            distances[pos] = next_color
            color(pos, next_color)
            for neigh in neighbours(distances, pos):
                next_to_color.add(neigh)
        next_color += 1
        to_color = next_to_color
    return distances

distances = colorize(mapping, (0, 0))
print("\033[1;1HPart one:", distances[oxim])
input("Press enter to continue")

distances = colorize(mapping, oxim)
print("\033[1;1HPart two:", max(distances.values()))
