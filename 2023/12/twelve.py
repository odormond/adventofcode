#! /usr/bin/env python

from functools import lru_cache
import re

import advent_of_code as adv

test_data = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

def parse(data):
    for line in data.splitlines():
        springs, blocks = line.split()
        blocks = [int(block) for block in blocks.split(',')]
        yield springs, tuple(blocks)


def configurations(springs, blocks):
    springs_re = springs.replace('.', ' ').replace('?', '.')
    return foo(springs_re, blocks)


class TooShort(Exception):
    pass


def chunk_count(springs_re, largest):
    count = 0
    for chunk in springs_re.split():
        if '#' in chunk:
            if chunk.rindex('#') - chunk.index('#') + 1 > largest:
                count += 2
            else:
                count += 1
    return count


@lru_cache(maxsize=1000000)
def foo(springs_re, blocks):
    if not blocks:
        count = 0 if '#' in springs_re else 1
    elif sum(blocks) < springs_re.count('#'):
        count = 0
    elif len(blocks) < chunk_count(springs_re, max(blocks)):
        count = 0
    elif sum(blocks) + len(blocks) - 1 > len(springs_re):
        raise TooShort()
    else:
        count = 0
        try:
            padding = ' ' if len(blocks) > 1 else ''
            end = len(springs_re) - sum(blocks) + len(blocks)
            for pos in range(end):
                if '#' in springs_re[:pos]:
                    break
                candidate = ' ' * pos + '#' * blocks[0] + padding
                if re.match(springs_re[:len(candidate)], candidate):
                    count += foo(springs_re[len(candidate):], blocks[1:])
        except TooShort:
            pass
    return count


def part1(data):
    return sum(configurations(springs, blocks) for springs, blocks in parse(data))


assert (result := part1(test_data)) == 21, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    return sum(configurations('?'.join([springs] * 5), blocks * 5) for springs, blocks in parse(data))


assert (result := part2(test_data)) == 525152, f"{result=}"
print("Part 2:", part2(adv.input()))
