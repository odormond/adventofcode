#! /usr/bin/env python3

import os.path
import advent_of_code as adv

TEST1 = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

TEST2 = """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


def parse_rules(rules):
    parsed = {}
    for rule in rules:
        name, chunks = rule.split(': ')
        values = []
        for chunk in chunks.split(' or '):
            low, hi = map(int, chunk.split('-'))
            values.extend(range(low, hi + 1))
        parsed[name] = set(values)
    return parsed


def parse_input(text):
    rules, mine, others = map(str.splitlines, text.strip().split('\n\n'))
    rules = parse_rules(rules)
    mine = [int(i) for i in mine[1].split(',')]
    others = [[int(i) for i in ticket.split(',')] for ticket in others[1:]]
    return rules, mine, others


def error_rate(rules, tickets):
    rate = 0
    for ticket in tickets:
        for value in ticket:
            if all(value not in values for values in rules.values()):
                rate += value
    return rate


def is_valid(rules, ticket):
    return all(any(value in values for values in rules.values()) for value in ticket)


def identify_fields(rules, tickets):
    fields = [None] * len(tickets[0])
    candidates = list(rules.items())
    while candidates:
        name, values = candidates.pop(0)
        matches = []
        for i in range(len(tickets[0])):
            if fields[i] is not None:
                continue
            vals = {ticket[i] for ticket in tickets}
            if vals.issubset(values):
                matches.append(i)
        if len(matches) == 1:
            fields[matches[0]] = name
        else:
            candidates.append((name, values))
    return fields


rules, mine, others = parse_input(TEST1)
assert error_rate(rules, others) == 71
assert [ticket for ticket in others if is_valid(rules, ticket)] == [[7, 3, 47]]

rules, mine, others = parse_input(TEST2)
tickets = [ticket for ticket in others if is_valid(rules, ticket)]
assert identify_fields(rules, tickets) == ['row', 'class', 'seat']

rules, mine, others = adv.input(int(os.path.basename(os.path.dirname(__file__))), parse_input)
print("Part 1:", error_rate(rules, others))

tickets = [ticket for ticket in others if is_valid(rules, ticket)]
fields = identify_fields(rules, tickets)
checksum = 1
for i, field in enumerate(fields):
    if field.startswith('departure'):
        checksum *= mine[i]

print("Part 2:", checksum)
