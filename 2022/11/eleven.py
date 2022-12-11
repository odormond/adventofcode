#! /usr/bin/env python

from functools import reduce
from operator import mul

import advent_of_code as adv

test_data = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


class Monkey:
    def __init__(self, notes, relief):
        self.inspections = 0
        self.items = []
        self.test_targets = {}
        for line in notes.splitlines():
            match line.strip().split():
                case 'Monkey', _:
                    pass
                case 'Starting', 'items:', *items:
                    self.items = [int(i) for i in ''.join(items).split(',')]
                case 'Operation:', 'new', '=', 'old', '*', 'old':
                    self.update_item = lambda w: (w * w // relief) % self.normalization
                case 'Operation:', 'new', '=', 'old', '*', n:
                    n = int(n)
                    self.update_item = lambda w: (w * n // relief) % self.normalization
                case 'Operation:', 'new', '=', 'old', '+', n:
                    n = int(n)
                    self.update_item = lambda w: ((w + n) // relief) % self.normalization
                case 'Test:', 'divisible', 'by', test_value:
                    self.test_value = int(test_value)
                case 'If', result, 'throw', 'to', 'monkey', m:
                    m = int(m)
                    self.test_targets[result == 'true:'] = m
                case unmatched:
                    print("Unmatched:", unmatched)

    def play_with(self, monkeys):
        while self.items:
            self.inspections += 1
            item = self.update_item(self.items.pop())
            monkeys[self.test_targets[item % self.test_value == 0]].items.append(item)

    def __str__(self):
        return str(self.__dict__)


def to_monkeys(data, relief):
    monkeys = [Monkey(notes, relief) for notes in data.split('\n\n')]
    normalization = reduce(mul, (m.test_value for m in monkeys))
    for m in monkeys:
        m.normalization = normalization
    return monkeys


def play(monkeys, rounds):
    for round_ in range(1, rounds + 1):
        for monkey in monkeys:
            monkey.play_with(monkeys)
    return monkeys


def monkey_business(monkeys):
    a, b, *_ = sorted([m.inspections for m in monkeys], reverse=True)
    return a * b


assert monkey_business(play(to_monkeys(test_data, 3), 20)) == 10605
print("Part 1:", monkey_business(play(to_monkeys(adv.input(), 3), 20)))


assert monkey_business(play(to_monkeys(test_data, 1), 10000)) == 2713310158
print("Part 2:", monkey_business(play(to_monkeys(adv.input(), 1), 10000)))

