#! /usr/bin/env python3

import itertools

from advent import Inputs

HP = 200
ATTACK = 3
MOVES = ((-1, 0), (0, -1), (0, 1), (1, 0))

source = Inputs(2018).get(15).text.strip().splitlines()


def reading_order(obj):
    return obj.y, obj.x


def hp_reading_order(obj):
    return obj.hp, obj.y, obj.x


class Fighter:
    def __init__(self, y, x, race):
        self.y = y
        self.x = x
        self.race = race
        self.hp = HP
        self.attack = {'E': ATTACK, 'G': 3}[race]

    @property
    def pos(self):
        return self.y, self.x

    def __eq__(self, pos):
        return pos == (self.y, self.x) and self.hp > 0

    def __repr__(self):
        return f'{self.race}({self.y},{self.x})[{self.hp}]'


def fighters():
    return sorted((f for f in elves + goblins if f.hp > 0), key=reading_order)


def cell(y, x):
    pos = y, x
    return 'E' if pos in elves else 'G' if pos in goblins else cave[x + y*width]


def print_cave():
    print('\n'.join(''.join(cell(y, x) for x in range(width)) for y in range(height)))


def dcell(y, x, dmap, fighter, enemy, old_pos):
    c = cell(y, x)
    if c in 'EG':
        c = f'\033[1m{c}\033[0m'
    d = dmap[y][x]
    if d is None:
        if c == '#':
            out = '###'
        else:
            out = '  '+c
    else:
        out = f'{dmap[y][x]:2d}'+c
    if fighter and (y, x) == fighter.pos:
        return f'\033[34m{out}\033[0m'
    if enemy and (y, x) == enemy:
        return f'\033[31m{out}\033[0m'
    if (y, x) == old_pos:
        return f'\033[42m{out}\033[0m'
    return out


def print_dmap(dmap, fighter, enemy, old_pos):
    print('\033[2J\033[0;0H' + '\n'.join(''.join(dcell(y, x, dmap, fighter, enemy, old_pos) for x in range(width)) for y in range(height)))


def distances(start, race):
    d_map = [[None] * width for y in range(height)]
    d = 0
    processed = set()
    positions = [start]
    while positions:
        next_positions = []
        for y, x in positions:
            d_map[y][x] = d
            processed.add((y, x))
            for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                ny, nx = pos = y+dy, x+dx
                if cell(ny, nx) != '.':  # in ('#', race):
                    continue
                if pos not in processed:
                    next_positions.append(pos)
                    processed.add(pos)
        d += 1
        positions = next_positions
    return d_map


def find_enemy(fighter):
    d = enemy = None
    enemies = [e for e in {'E': goblins, 'G': elves}[fighter.race] if e.hp > 0]
    # Check contact
    contacts = sorted((e.hp, e.pos, e) for e in enemies if e.pos in [(fighter.y+dy, fighter.x+dx) for dy, dx in MOVES])
    if contacts:
        d_map = distances(fighter.pos, fighter.race)
        # print_dmap(d_map, fighter, contacts[0][1], None)
        return 0, contacts[0][2]
    d_map = distances(fighter.pos, fighter.race)
    targets = sorted((d_map[e.y+dy][e.x+dx], (e.y+dy, e.x+dx)) for e in enemies for dy, dx in MOVES if e.hp > 0 and d_map[e.y+dy][e.x+dx] is not None)
    if targets:
        # print_dmap(d_map, fighter, targets[0][1], None)
        return targets[0]
    return None, None


def take_turn(fighter):
    d, enemy = find_enemy(fighter)
    if d is None:
        return
    if d > 0:  # Must move, target it out of reach
        move(fighter, enemy)
        d, enemy = find_enemy(fighter)  # and re-acquire a target
    if d == 0:  # Ennemy in reach, attack
        enemy.hp -= fighter.attack
        if enemy.hp <= 0:
            pass  # print(f'\033[{enemy.y+1};{3*enemy.x+1}H\033[45m  .\033[0m')


def move(fighter, enemy):
    fighters = {'E': elves, 'G': goblins}[fighter.race]
    d_map = distances(enemy, fighter.race)
    y, x = fighter.pos
    _, fighter.y, fighter.x = sorted((d_map[y+dy][x+dx], y+dy, x+dx) for dy, dx in MOVES if d_map[y+dy][x+dx] is not None)[0]
    # print_dmap(d_map, fighter, enemy, (y, x))
    fighters.sort(key=reading_order)


width = len(source[0])
height = len(source)
cave = []
elves = []
goblins = []
for y, line in enumerate(source):
    for x, c in enumerate(line):
        cave.append('.' if c in 'EG' else c)
        if c in 'EG':
            {'E': elves, 'G': goblins}[c].append(Fighter(y, x, c))


rounds = 0
fighting = True
while fighting:
    for fighter in fighters():
        if fighter.hp <= 0:
            continue  # he died this round
        if [] in ([e for e in elves if e.hp > 0], [g for g in goblins if g.hp > 0]):
            fighting = False
            break
        take_turn(fighter)
    else:
        rounds += 1

print("Part one:", rounds * sum(f.hp for f in fighters()), rounds)


ATTACK = 23
while True:
    ATTACK += 1
    width = len(source[0])
    height = len(source)
    cave = []
    elves = []
    goblins = []
    for y, line in enumerate(source):
        for x, c in enumerate(line):
            cave.append('.' if c in 'EG' else c)
            if c in 'EG':
                {'E': elves, 'G': goblins}[c].append(Fighter(y, x, c))

    rounds = 0
    fighting = True
    while fighting:
        for fighter in fighters():
            if fighter.hp <= 0:
                continue  # he died this round
            if [] in ([e for e in elves if e.hp > 0], [g for g in goblins if g.hp > 0]):
                fighting = False
                break
            take_turn(fighter)
        else:
            rounds += 1

    # print(rounds * sum(f.hp for f in fighters()), rounds, ATTACK, sum(1 for e in elves if e.hp > 0), '/', len(elves), sum(1 for g in goblins if g.hp > 0), '/', len(goblins))
    if sum(1 for e in elves if e.hp > 0) == len(elves):
        break

print("Part two:", rounds * sum(f.hp for f in fighters()), rounds, ATTACK)
