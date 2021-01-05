#! /usr/bin/env python3

from functools import cache
import os.path
import advent_of_code as adv

TEST = ((9, 2, 6, 3, 1), (5, 8, 4, 7, 10))


def to_decks(text):
    return tuple(
        tuple(int(i) for i in player.splitlines() if not i.startswith('Player'))
        for player in text.strip().split('\n\n')
    )


def combat(player1, player2):
    player1, player2 = list(player1), list(player2)  # Don't modify input
    while player1 and player2:
        a = player1.pop(0)
        b = player2.pop(0)
        if a > b:
            player1.extend([a, b])
        else:
            player2.extend([b, a])
    score = 0
    for i, c in enumerate(reversed(player1 or player2)):
        score += (i + 1) * c
    return score


@cache
def recursive_combat(player1, player2):
    history1, history2 = set(), set()
    while player1 and player2:
        player1, player2 = list(player1), list(player2)  # Don't modify input
        if tuple(player1) in history1 or tuple(player2) in history2:
            return True, (player1, player2)
        history1.add(tuple(player1))
        history2.add(tuple(player2))
        a = player1.pop(0)
        b = player2.pop(0)
        if len(player1) >= a and len(player2) >= b:
            if recursive_combat(tuple(player1[:a]), tuple(player2[:b]))[0]:
                player1.extend([a, b])
            else:
                player2.extend([b, a])
        else:
            if a > b:
                player1.extend([a, b])
            else:
                player2.extend([b, a])
    return bool(player1), (player1, player2)


def score(player1, player2):
    score = 0
    for i, c in enumerate(reversed(player1 or player2)):
        score += (i + 1) * c
    return score


assert combat(*TEST) == 306
p1_win, decks = recursive_combat(*TEST)
assert p1_win is False
assert score(*decks) == 291

decks = adv.input(int(os.path.basename(os.path.dirname(__file__))), to_decks)
print("Part 1:", combat(*decks))
print("Part 2:", score(*recursive_combat(*decks)[1]))
