#! /usr/bin/env python

from functools import reduce
from operator import mul

import advent_of_code as adv

test_data = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

def parse(data):
    for line in data.splitlines():
        game, draws = line.split(': ')
        game_id = int(game.split(' ')[1])
        draws = [
            {
                colour: int(count)
                for count, colour in (cubes.split(' ') for cubes in draw.split(', '))
            }
            for draw in draws.split('; ')
        ]
        yield game_id, draws


def part1(data):
    LIMITS = {'red': 12, 'green': 13, 'blue': 14}
    return sum(
        game_id
        for game_id, draws in parse(data)
        if all(
            draw.get('red', 0) <= LIMITS['red']
            and draw.get('green', 0) <= LIMITS['green']
            and draw.get('blue', 0) <= LIMITS['blue']
            for draw in draws
        )
    )


assert (result := part1(test_data)) == 8, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    return sum(
        reduce(
            mul,
            (
                reduce(max, (draw.get(colour, 0) for draw in draws), 0)
                for colour in ('red', 'green', 'blue')
            ),
        )
        for _, draws in parse(data)
    )


assert (result := part2(test_data)) == 2286, f"{result=}"
print("Part 2:", part2(adv.input()))
