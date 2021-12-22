#! /usr/bin/env python

from collections import defaultdict, Counter
from itertools import cycle, product
from pathlib import Path
from time import time, sleep
import advent_of_code as adv


def to_start_position(text):
    return [int(player.split()[-1]) for player in text.strip().splitlines()]


test_pos = to_start_position("""\
Player 1 starting position: 4
Player 2 starting position: 8
""")
pb_pos = adv.input(Path(__file__).parent.name, to_start_position)


def die(count, sides):
    pass


def play(pos1, pos2, dice, win):
    score1 = score2 = rolls = 0
    while True:
        pos1 = ((pos1 - 1 + next(dice)) % 10) + 1
        score1 += pos1
        rolls += 3
        if score1 >= win:
            return 1, score2 * rolls
        pos2 = ((pos2 - 1 + next(dice)) % 10) + 1
        score2 += pos2
        rolls += 3
        if score2 >= win:
            return 2, score1 * rolls


def deterministict_dice():
    dice = cycle(range(1, 101))
    return cycle([next(dice) + next(dice) + next(dice) for _ in range(100)])


assert play(*test_pos, deterministict_dice(), 1000) == (1, 739785)
print("Part 1:", play(*pb_pos, deterministict_dice(), 1000)[1])


def estimate_wins(start_pos):
    dice_sums = Counter(sum(roll) for roll in product(range(1, 4), repeat=3))
    universes = Counter()
    max_queue = 0
    queue = [(start_pos, 0, 0, 1)]
    while queue:
        max_queue = max(max_queue, len(queue))
        pos, score, turns, clones = queue.pop(0)
        for roll, repeat in dice_sums.items():
            new_pos = ((pos - 1 + roll) % 10) + 1
            new_score = score + new_pos
            if new_score >= 21:
                universes[(True, turns + 1)] += repeat * clones
            else:
                universes[(False, turns + 1)] += repeat * clones
                queue.append((new_pos, new_score, turns + 1, repeat * clones))
    return universes

universes1 = estimate_wins(test_pos[0])
universes2 = estimate_wins(test_pos[1])
assert sum(
    universes1[(True, t)] * (universes2[(True, t)] + universes2[(False, t)])
    for t in range(min(t for win, t in universes1 if win), max(t for win, t in universes1 if win)+1)
) // 27 == 444356092776315

# We devide by 27 because player 1 wins at turn t and so the 3 * 3 * 3 = 27 end universes created
# by player 2 when he rolls the dice did not actually happen as the game stopped before that.


universes1 = estimate_wins(pb_pos[0])
universes2 = estimate_wins(pb_pos[1])
print(
    "Part 2:",
    sum(
        universes1[(True, t)] * (universes2[(True, t)] + universes2[(False, t)])
        for t in range(min(t for win, t in universes1 if win), max(t for win, t in universes1 if win)+1)
    ) // 27
)
