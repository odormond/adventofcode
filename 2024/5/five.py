#! /usr/bin/env python

from itertools import combinations

import advent_of_code as aoc

test_data = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

def parse(data):
    rules, updates = data.split("\n\n")
    rules = {tuple(int(page) for page in rule.split("|")) for rule in rules.splitlines()}
    updates = [[int(page) for page in update.split(",")] for update in updates.splitlines()]
    return rules, updates


def ordered_updates(rules, updates):
    for update in updates:
        for a, b in combinations(update, 2):
            if (b, a) in rules:
                break  # violation
        else:
            yield update


def part1(data):
    rules, updates = parse(data)
    return sum(correct[len(correct)//2] for correct in ordered_updates(rules, updates))


assert (result := part1(test_data)) == 143, f"{result=}"
print("Part 1:", part1(aoc.input()))

def unordered_updates(rules, updates):
    for update in updates:
        for a, b in combinations(update, 2):
            if (b, a) in rules:
                yield update  # violation
                break


def reorder(rules, unordered):
    ordered = unordered[:]
    changed = True
    while changed:
        changed = False
        for a, b in combinations(ordered, 2):
            if (b, a) in rules:
                # swap them
                idx_a = ordered.index(a)
                idx_b = ordered.index(b)
                ordered[idx_a], ordered[idx_b] = b, a
                changed = True
                break
    return ordered


def part2(data):
    rules, updates = parse(data)
    return sum(
        reorder(rules, incorrect)[len(incorrect)//2]
        for incorrect in unordered_updates(rules, updates)
    )


assert (result := part2(test_data)) == 123, f"{result=}"
print("Part 2:", part2(aoc.input()))
