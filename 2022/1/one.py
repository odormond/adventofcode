#! /usr/bin/env python

import advent_of_code as adv


def to_stock(data):
    per_elf = [[]]
    for line in data.splitlines():
        line = line.strip()
        if line:
            per_elf[-1].append(int(line))
        else:
            per_elf.append([])
    return per_elf


test_data = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

test_stock = to_stock(test_data)
assert max(sum(elf_stock) for elf_stock in test_stock) == 24000

stock = adv.input(to_stock)
print("Part 1:", max(sum(elf_stock) for elf_stock in stock))

assert sorted((sum(elf_stock) for elf_stock in test_stock), reverse=True)[:3] == [24000, 11000, 10000]
print("Part 2:", sum(sorted((sum(elf_stock) for elf_stock in stock), reverse=True)[:3]))
