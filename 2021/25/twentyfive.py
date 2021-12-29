#! /usr/bin/env python

from pathlib import Path
import advent_of_code as adv


def parse(text):
    east = set()
    south = set()
    for l, line in enumerate(text.strip().splitlines()):
        for c, v in enumerate(line):
            if v == '>':
                east.add((l, c))
            elif v == 'v':
                south.add((l, c))
    return east, south, l+1, c+1


test = parse("""\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""")
pb = adv.input(Path(__file__).parent.name, parse)


def step(east, south, n_lines, n_cols):
    new_east = set()
    for cucumber in sorted(east):
        l, c = cucumber
        if (l, (c+1) % n_cols) not in east.union(south):
            new_east.add((l, (c+1) % n_cols))
        else:
            new_east.add(cucumber)
    east = new_east
    new_south = set()
    for cucumber in sorted(south):
        l, c = cucumber
        if ((l+1) % n_lines, c) not in east.union(south):
            new_south.add(((l+1) % n_lines, c))
        else:
            new_south.add(cucumber)
    south = new_south
    return east, south


def dump(east, south, n_lines, n_cols):
    for l in range(n_lines):
        line = []
        for c in range(n_cols):
            if (l, c) in east:
                line.append('>')
            elif (l, c) in south:
                line.append('v')
            else:
                line.append('.')
        print(''.join(line))
    input()


def lock(east, south, n_lines, n_cols):
    new_east = new_south = None
    i = 0
    while True:
        new_east, new_south = step(east, south, n_lines, n_cols)
        i += 1
        if new_east == east and new_south == south:
            break
        east, south = new_east, new_south
    return i, east, south


assert lock(*test)[0] == 58
cnt, east, south = lock(*pb)
print("Part 1:", cnt)
