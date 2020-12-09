#! /usr/bin/env python3

from collections import deque
import os.path
import advent_of_code as adv


TEST_RULES = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


def parse_rule(rule):
    container, content = rule.split(" contain ")
    container, _ = container.rsplit(" ", 1)
    bags = {}
    if content == "no other bags.":
        return container, bags
    for bag in content[:-1].split(", "):
        count, bag = bag.split(" ", 1)
        bag, _ = bag.rsplit(" ", 1)
        bags[bag] = int(count)
    return container, bags


def to_rules(text):
    return dict(map(parse_rule, text.strip().splitlines()))


def colour_containers(colour, rules):
    # Direct containment
    containers = {container for container, bags in rules.items() if colour in bags}
    # Indirect containment
    while True:
        indirect = set()
        for inner in containers:
            for container, bags in rules.items():
                if inner in bags and container not in containers:
                    indirect.add(container)
        containers.update(indirect)
        if not indirect:
            break
    return containers


assert len(colour_containers("shiny gold", to_rules(TEST_RULES))) == 4

rules = adv.input(int(os.path.basename(os.path.dirname(__file__))), to_rules)
print("Part 1:", len(colour_containers("shiny gold", rules)))


def contained_bags(colour, rules):
    open_set = deque([(colour, 1)])
    closed_set = {}
    while open_set:
        colour, multiplier = open_set.popleft()
        closed_set[colour] = closed_set.get(colour, 0) + multiplier
        for bag, count in rules[colour].items():
            open_set.append((bag, count * multiplier))
    return sum(closed_set.values()) - 1


assert contained_bags("shiny gold", to_rules(TEST_RULES)) == 32
assert (
    contained_bags(
        "shiny gold",
        to_rules(
            """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""
        ),
    )
    == 126
)

print("Part 2:", contained_bags("shiny gold", rules))
