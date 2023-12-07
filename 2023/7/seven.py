#! /usr/bin/env python

from enum import IntEnum
import advent_of_code as adv

test_data = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

def parse(data):
    for line in data.splitlines():
        hand, bid = line.split()
        bid = int(bid)
        yield hand, bid


class HandType(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7


def hand_type(hand):
    kinds = set(hand)
    if len(kinds) == 1:
        return HandType.FIVE_OF_KIND
    if len(kinds) == 2 and hand.count(hand[0]) in (1, 4):
        return HandType.FOUR_OF_KIND
    if len(kinds) == 2:
        return HandType.FULL_HOUSE
    if len(kinds) == 3 and any(hand.count(card) == 3 for card in kinds):
        return HandType.THREE_OF_KIND
    if len(kinds) == 3:
        return HandType.TWO_PAIR
    if len(kinds) == 4:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def hand_value(hand):
    return hand_type(hand), *[CARDS.index(card) for card in hand]


def evaluate(data):
    return sum(
            rank * bid
        for rank, (hand, bid) in enumerate(sorted(parse(data), key=lambda x: hand_value(x[0])), 1)
    )


assert (result := evaluate(test_data)) == 6440, f"{result=}"
print("Part 1:", evaluate(adv.input()))


CARDS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


def hand_type(hand):
    kinds = set(hand)
    if 'J' in kinds and kinds != {'J'}:
        has_joker = True
        kinds -= {'J'}
    else:
        has_joker = False
    if len(kinds) == 1:
        return HandType.FIVE_OF_KIND
    if len(kinds) == 2 and (
        (has_joker is False and hand.count(hand[0]) in (1, 4))
        or (
            has_joker is True
            and sorted(hand.count(card) for card in kinds) in ([1, 1], [1, 2], [1, 3])
        )
    ):
        return HandType.FOUR_OF_KIND
    if len(kinds) == 2:
        return HandType.FULL_HOUSE
    if len(kinds) == 3 and (has_joker or any(hand.count(card) == 3 for card in kinds)):
        return HandType.THREE_OF_KIND
    if len(kinds) == 3:
        return HandType.TWO_PAIR
    if len(kinds) == 4:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


assert (result := evaluate(test_data)) == 5905, f"{result=}"
print("Part 2:", evaluate(adv.input()))
