#! /usr/bin/env python3

import re
import os.path
import advent_of_code as adv

DIR_RE = re.compile(r'e|se|sw|ne|nw|w')
STEPS = {
    'e': (+1, 0),
    'ne': (0, +1),
    'nw': (-1, +1),
    'w': (-1, 0),
    'sw': (0, -1),
    'se': (+1, -1),
}

TEST = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""


def parse_input(text):
    return [re.findall(DIR_RE, line) for line in text.strip().splitlines()]


r"""
     (-1,1) -w- (0,1)
      /    \    /    \
     ne    nw  ne    nw
     /      \  /      \
(-1,0) -w- (0,0) -e- (1,0)
"""


def find_tile(steps):
    x, y = 0, 0
    for step in steps:
        dx, dy = STEPS[step]
        x += dx
        y += dy
    return x, y


def pattern(tiles):
    blacks = set()
    for tile in map(find_tile, tiles):
        if tile in blacks:
            blacks.remove(tile)
        else:
            blacks.add(tile)
    return blacks


assert len(pattern(parse_input(TEST))) == 10

tiles = adv.input(int(os.path.basename(os.path.dirname(__file__))), parse_input)
blacks = pattern(tiles)
print("Part 1:", len(blacks))


def neighbours(tile):
    x, y = tile
    for step in ('e', 'sw', 'w', 'nw', 'ne', 'e'):
        dx, dy = STEPS[step]
        x += dx
        y += dy
        yield (x, y)


def live(blacks):
    new = set()
    whites = {}
    for black in blacks:
        black_neighours = 0
        for neigh in neighbours(black):
            if neigh in blacks:
                black_neighours += 1
            else:
                whites.setdefault(neigh, set()).add(black)
        if 0 < black_neighours <= 2:
            new.add(black)
    for white, black_neighbours in whites.items():
        if len(black_neighbours) == 2:
            new.add(white)
    return new


blacks = pattern(parse_input(TEST))
for day in range(100):
    blacks = live(blacks)
assert len(blacks) == 2208

blacks = pattern(tiles)
for day in range(100):
    blacks = live(blacks)
print("Part 2:", len(blacks))
