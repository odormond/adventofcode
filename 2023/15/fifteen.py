#! /usr/bin/env python

import advent_of_code as adv

test_data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

def parse(data):
    return data.replace('\n', '').split(',')


def part1(data):
    return sum(HASH(instruction) for instruction in parse(data))


def HASH(string):
    h = 0
    for c in string:
        h += ord(c)
        h *= 17
        h %= 256
    return h

assert HASH('HASH') == 52

assert (result := part1(test_data)) == 1320, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    boxes = [{} for i in range(256)]
    for instruction in parse(data):
        if '=' in instruction:
            op = '='
            label, arg = instruction.split('=')
            box = HASH(label)
            boxes[box][label] = int(arg)
        else:
            op = '-'
            label, arg = instruction.split('-')
            box = HASH(label)
            if label in boxes[box]:
                boxes[box].pop(label)
    return sum(
        i * j * f
        for i, box in enumerate(boxes, 1)
        for j, f in enumerate(box.values(), 1)
    )



assert (result := part2(test_data)) == 145, f"{result=}"
print("Part 2:", part2(adv.input()))
