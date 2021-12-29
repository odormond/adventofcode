#! /usr/bin/env python

from itertools import product
from math import inf
from pathlib import Path
import advent_of_code as adv


PATTERN = """\
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  #########
"""

test_data = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


"""Allowed positions
#############
#ab.c.d.e.fg#
###h#i#j#k###
  #l#m#n#o#
  #p#q#r#s#
  #t#u#v#w#
  #########
"""
POSITIONS = {
    0: (1, 1),  # a
    1: (1, 2),  # b
    2: (1, 4),  # c
    3: (1, 6),  # d
    4: (1, 8),  # e
    5: (1, 10),  # f
    6: (1, 11),  # g
    7: (2, 3),  # h
    8: (2, 5),  # i
    9: (2, 7),  # j
    10: (2, 9),  # k
    11: (3, 3),  # l
    12: (3, 5),  # m
    13: (3, 7),  # n
    14: (3, 9),  # o
    15: (4, 3),  # p
    16: (4, 5),  # q
    17: (4, 7),  # r
    18: (4, 9),  # s
    19: (5, 3),  # t
    20: (5, 5),  # u
    21: (5, 7),  # v
    22: (5, 9),  # w
}
INVERSE_POSITIONS = {p: l for l, p in POSITIONS.items()}


def parse(text):
    state = [None] * 15
    for l, line in enumerate(text.strip().splitlines()):
        for c, v in enumerate(line):
            if v in 'ABCD':
                state[INVERSE_POSITIONS[(l, c)]] = v
    return tuple(state)


test_init = parse(test_data)
pb_init = adv.input(Path(__file__).parent.name, parse)


# Part 1 setup

HALLWAY = (0, 1, 2, 3, 4, 5, 6)  # 'abcdefg'
ROOMS = (7, 8, 9, 10, 11, 12, 13, 14)  # 'hijklmno'
POD_ROOMS = {'A': (7, 11), 'B': (8, 12), 'C': (9, 13), 'D': (10, 14)}  # {'A': 'hl', 'B': 'im', 'C': 'jn', 'D': 'ko'}
FULL_PATHS = [
    (0, 1, None, 7, 11),  # 'ab.hl',
    (0, 1, None, 2, None, 8, 12),  # 'ab.c.im',
    (0, 1, None, 2, None, 3, None, 9, 13),  # 'ab.c.d.jn',
    (0, 1, None, 2, None, 3, None, 4, None, 10, 14),  # 'ab.c.d.e.ko',
    (6, 5, None, 10, 14),  # 'gf.ko',
    (6, 5, None, 4, None, 9, 13),  # 'gf.e.jn',
    (6, 5, None, 4, None, 3, None, 8, 12),  # 'gf.e.d.im',
    (6, 5, None, 4, None, 3, None, 2, None, 7, 11),  # 'gf.e.d.c.hl',
    (11, 7, None, 2, None, 8, 12),  # 'lh.c.im',
    (11, 7, None, 2, None, 3, None, 9, 13),  # 'lh.c.d.jn',
    (11, 7, None, 2, None, 3, None, 4, None, 10, 14),  # 'lh.c.d.e.ko',
    (12, 8, None, 3, None, 9, 13),  # 'mi.d.jn',
    (12, 8, None, 3, None, 4, None, 10, 14),  # 'mi.d.e.ko',
    (13, 9, None, 4, None, 10, 14),  # 'nj.e.ko',
]
ENERGY_USE = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
FINAL_STATE = (
    None, None, None, None, None, None, None,  # Hallway
    'A', 'B', 'C', 'D',
    'A', 'B', 'C', 'D',
)
INDIVIDUAL_ROOMS = ((1, 0), (5, 6), (7, 11), (8, 12), (9, 13), (10, 14))


def path(start, end):
    for path in FULL_PATHS:
        if start in path and end in path:
            break
    else:
        assert False, f"Path not found for free check: {start} -> {end}"
    s, e = path.index(start), path.index(end)
    if e < s:
        segment = path[e:s][::-1]
    else:
        segment = path[s+1:e+1]
    return segment


ALLOWED_MOVES = {}
for pod, pod_room in POD_ROOMS.items():
    ALLOWED_MOVES[pod] = paths = {}
    for start, end in [
        *[(r, h) for r, h in product(ROOMS, HALLWAY)],
        *[(h, a) for h, a in product(HALLWAY, pod_room)],
        *[(o, a) for o, a in product(set(ROOMS) - set(pod_room), pod_room)],
    ]:
        paths.setdefault(start, {})[end] = path(start, end)


# Solver

def moves_from(state):
    for start in (2, 3, 4):
        pod = state[start]
        if pod:
            for end, path in ALLOWED_MOVES[pod][start].items():
                assigned_room = POD_ROOMS[pod]
                if end in assigned_room and any(state[r] not in (pod, None) for r in assigned_room):
                    continue  # The room contains at least a pod not assigned to it
                if not any(state[p] for p in path if p is not None):  # path is not blocked
                    yield start, end, len(path)
    for room in INDIVIDUAL_ROOMS:
        for start in room:
            pod = state[start]
            if pod:
                for end, path in ALLOWED_MOVES[pod][start].items():
                    assigned_room = POD_ROOMS[pod]
                    if end in assigned_room and any(state[r] not in (pod, None) for r in assigned_room):
                        continue  # The room contains at least a pod not assigned to it
                    if not any(state[p] for p in path if p is not None):  # path is not blocked
                        yield start, end, len(path)
                break  # that is the closed to the hallway and blocks the others so abort the loop


def do_move(state, move):
    state = list(state)
    start, end, steps = move
    pod = state[start]
    cost = ENERGY_USE[pod]
    state[start] = None
    state[end] = pod
    return cost * steps, tuple(state)


def print_state(state, prefix=''):
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w = [s or '.' for s in state]
    print(prefix + "#############")
    print(prefix + f"#{a}{b}.{c}.{d}.{e}.{f}{g}#")
    print(prefix + f"###{h}#{i}#{j}#{k}###")
    print(prefix + f"  #{l}#{m}#{n}#{o}#")
    print(prefix + f"  #{p}#{q}#{r}#{s}#")
    print(prefix + f"  #{t}#{u}#{v}#{w}#")
    print(prefix + "  #########")
    return input()


def solve(state):
    energy = 0
    min_energy_for_state = {state: 0}
    pending_states_by_energy = {0: {state}}
    while pending_states_by_energy:
        if FINAL_STATE in pending_states_by_energy.get(energy, set()):
            return energy
        for state in pending_states_by_energy.pop(energy, []):
            for move in moves_from(state):
                dE, new_state = do_move(state, move)
                min_energy = min_energy_for_state.get(new_state, inf)
                if energy + dE < min_energy:  # We can reach new_state with less energy
                    if min_energy < inf:
                        # We had a less optimal state. Remove it to avoid useless future processing
                        pending_states_by_energy[min_energy].remove(new_state)
                    min_energy_for_state[new_state] = energy + dE
                    pending_states_by_energy.setdefault(energy + dE, set()).add(new_state)
        energy += 1


assert (s := solve(test_init)) == 12521, f"Wrong solution: {s}"
print("Part 1:", solve(pb_init))


# Part 2 setup

ROOMS = {7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}
POD_ROOMS = {'A': {7, 11, 15, 19}, 'B': {8, 12, 16, 20}, 'C': {9, 13, 17, 21}, 'D': {10, 14, 18, 22}}
FULL_PATHS = [
    (0, 1, None, 7, 11, 15, 19),  # 'ab.hlpt',
    (0, 1, None, 2, None, 8, 12, 16, 20),  # 'ab.c.imqu',
    (0, 1, None, 2, None, 3, None, 9, 13, 17, 21),  # 'ab.c.d.jnrv',
    (0, 1, None, 2, None, 3, None, 4, None, 10, 14, 18, 22),  # 'ab.c.d.e.kosw',
    (6, 5, None, 10, 14, 18, 22),  # 'gf.kosw',
    (6, 5, None, 4, None, 9, 13, 17, 21),  # 'gf.e.jnrv',
    (6, 5, None, 4, None, 3, None, 8, 12, 16, 20),  # 'gf.e.d.imqu',
    (6, 5, None, 4, None, 3, None, 2, None, 7, 11, 15, 19),  # 'gf.e.d.c.hlpt',
    (19, 15, 11, 7, None, 2, None, 8, 12, 16, 20),  # 'tplh.c.imqu',
    (19, 15, 11, 7, None, 2, None, 3, None, 9, 13, 17, 21),  # 'tplh.c.d.jnrv',
    (19, 15, 11, 7, None, 2, None, 3, None, 4, None, 10, 14, 18, 22),  # 'tplh.c.d.e.kosw',
    (20, 16, 12, 8, None, 3, None, 9, 13, 17, 21),  # 'uqmi.d.jnrv',
    (20, 16, 12, 8, None, 3, None, 4, None, 10, 14, 18, 22),  # 'uqmi.d.e.kosw',
    (21, 17, 13, 9, None, 4, None, 10, 14, 18, 22),  # 'vrnj.e.kosw',
]
ALLOWED_MOVES = {}
for pod, pod_room in POD_ROOMS.items():
    ALLOWED_MOVES[pod] = paths = {}
    for start, end in [
        *[(r, h) for r, h in product(ROOMS, HALLWAY)],
        *[(h, a) for h, a in product(HALLWAY, pod_room)],
        *[(o, a) for o, a in product(ROOMS - pod_room, pod_room)],
    ]:
        paths.setdefault(start, {})[end] = path(start, end)
FINAL_STATE = (
    None, None, None, None, None, None, None,  # Hallway
    'A', 'B', 'C', 'D',
    'A', 'B', 'C', 'D',
    'A', 'B', 'C', 'D',
    'A', 'B', 'C', 'D',
)
INDIVIDUAL_ROOMS = ((1, 0), (5, 6), (7, 11, 15, 19), (8, 12, 16, 20), (9, 13, 17, 21), (10, 14, 18, 22))


def correct_state(state):
    state = list(state)
    state[-4:-4] = ['D', 'C', 'B', 'A', 'D', 'B', 'A', 'C']
    return tuple(state)


test_fixed = correct_state(test_init)
pb_fixed = correct_state(pb_init)
assert (s := solve(test_fixed)) == 44169, f"Wrong solution: {s}"
print("\nPart 2:", solve(pb_fixed))
