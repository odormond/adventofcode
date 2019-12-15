#! /usr/bin/env python

import asyncio
from time import sleep

import advent_of_code as adv
from int_code import Computer


arkanoid = adv.input(13, adv.to_list_of_int)
computer = Computer(arkanoid)
asyncio.run(computer.run())
blocks = set()
while not computer.outputs.empty():
    c, l, o = tuple(computer.outputs.get_nowait() for _ in range(3))
    if o == 2:
        blocks.add((c, l))

print("Part one:", len(blocks))
input("Press enter to continue")


async def game():
    class Context:
        def __init__(self):
            self.blocks = set()
            self.paddle = None
            self.ball = None
            self.score = None
            self.over = False

    async def draw(context):
        while not context.over:
            c = await context.outputs.get()
            l = await context.outputs.get()
            o = await context.outputs.get()
            if (c, l) == (-1, 0):
                context.score = o
                context.over = not context.blocks
                print(f"\033[1;1H{context.score}", end='', flush=True)
            elif o == 0:
                context.blocks.discard((c, l))
                print(f"\033[{l+2};{c+1}H ", end='', flush=True)
            elif o == 1:
                if l == 0:
                    print(f"\033[{l+2};{c+1}H_", end='', flush=True)
                else:
                    print(f"\033[{l+2};{c+1}H|", end='', flush=True)
            elif o == 2:
                context.blocks.add((c, l))
                print(f"\033[{l+2};{c+1}H#", end='', flush=True)
            elif o == 3:
                context.paddle = (c, l)
                print(f"\033[{l+2};{c+1}H=", end='', flush=True)
            elif o == 4:
                context.ball = (c, l)
                print(f"\033[{l+2};{c+1}Ho", end='', flush=True)

    async def play(context):
        while context.score is None:
            await asyncio.sleep(0)
        while not context.over:
            b = context.ball[0]
            p = context.paddle[0]
            if b == p:
                move = 0
            elif b < p:
                 move = -1
            else:
                 move = 1
            await context.inputs.put(move)
            await asyncio.sleep(0)
            await asyncio.sleep(0)

    print("\033[2J", end='', flush=True)
    computer = Computer([2] + arkanoid[1:], inputs=asyncio.Queue(1))
    context = Context()
    context.outputs = computer.outputs
    context.inputs = computer.inputs
    await asyncio.gather(computer.run(), draw(context), play(context))
    return context.score
    
score = asyncio.run(game())
print("\033[2J\rPart two:", score)
