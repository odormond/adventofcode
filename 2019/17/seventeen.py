#! /usr/bin/env python

import asyncio
from itertools import product

import advent_of_code as adv
from int_code import Computer

ASCII = adv.input(17, adv.to_list_of_int)

computer = Computer(ASCII)
asyncio.get_event_loop().run_until_complete(computer.run())
output = []
scaffolds = set()
x = y = width = height = 0
while not computer.outputs.empty():
    out = chr(computer.outputs.get_nowait())
    output.append(out)
    if out == '\n':
        x = 0
        y += 1
    elif out != '.':
        scaffolds.add((x, y))
    if out in '<>v^':
        robot = (x, y)
    x += 1
    width = max(width, x)
    height = max(height, y)
print(''.join(output))
intersections = {
    (x, y)
    for x, y in product(range(width), range(height))
    if (x, y) in scaffolds and all((x+dx, y+dy) in scaffolds for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)))
}
print(len(intersections), sorted(intersections))
print("Part one:", sum((x-1)*y for x, y in intersections))


MAIN = 'A,B,A,B,A,C,B,C,A,C\n'
A = 'R,4,L,10,L,10\n'
B = 'L,8,R,12,R,10,R,4\n'
C = 'L,8,L,8,R,10,R,4\n'
VIDEO = 'n\n'
computer = Computer([2] + ASCII[1:])
for c in MAIN + A + B + C + VIDEO:
    computer.inputs.put_nowait(ord(c))
asyncio.get_event_loop().run_until_complete(computer.run())
outputs = []
while not computer.outputs.empty():
    outputs.append(computer.outputs.get_nowait())
solution = outputs.pop()
print(''.join(map(chr, outputs)))
print("Part two:", solution)
