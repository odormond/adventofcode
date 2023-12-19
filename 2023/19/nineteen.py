#! /usr/bin/env python

from functools import reduce
from operator import mul
import advent_of_code as adv

test_data = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

def parse(data):
    raw_workflows, raw_parts = data.split('\n\n')
    workflows = {}
    for line in raw_workflows.splitlines():
        name, rules = line.split('{')
        rules = [r.split(':') for r in rules[:-1].split(',')]
        workflows[name] = rules
    parts = []
    for raw_part in raw_parts.splitlines():
        part = {}
        for system in raw_part[1:-1].split(','):
            name, value = system.split('=')
            part[name] = int(value)
        parts.append(part)
    return workflows, parts


def part1(data):
    workflows, parts = parse(data)
    accepted = []
    for part in parts:
        name = 'in'
        running = True
        while running:
            for rule in workflows[name]:
                if len(rule) == 1:
                    rule = rule[0]
                    if rule == 'A':
                        accepted.append(part)
                        running = False
                        break
                    if rule == 'R':
                        running = False
                        break
                    name = rule
                    break
                condition, destination = rule
                if eval(condition, {}, part):
                    if destination == 'A':
                        accepted.append(part)
                        running = False
                        break
                    if destination == 'R':
                        running = False
                        break
                    name = destination
                    break
    return sum(sum(a.values()) for a in accepted)


assert (result := part1(test_data)) == 19114, f"{result=}"
print("Part 1:", part1(adv.input()))


def parse(data):
    raw_workflows, raw_parts = data.split('\n\n')
    workflows = {}
    for line in raw_workflows.splitlines():
        name, raw_rules = line.split('{')
        rules = []
        for rule in raw_rules[:-1].split(','):
            if ':' in rule:
                condition, destination = rule.split(':')
                var = condition[0]
                op = condition[1]
                limit = int(condition[2:])
                rules.append((var, op, limit, destination))
            else:
                rules.append(rule)
        workflows[name] = rules
    return workflows


def part2(data):
    workflows = parse(data)
    part = {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)}
    accepted = []
    rejected = []
    queue = [('in', part)]
    while queue:
        name, part = queue.pop(0)
        rules_queue = workflows[name][:]
        while rules_queue:
            rule = rules_queue.pop(0)
            if rule == 'R':
                rejected.append(part)
                break
            if rule == 'A':
                accepted.append(part)
                break
            if isinstance(rule, str):
                queue.append((rule, part))
                break
            var, op, limit, destination = rule
            low, hi = part[var]
            if (op == '<' and hi < limit) or (op == '>' and low > limit):
                if destination == 'R':
                    rejected.append(part)
                    break
                if destination == 'A':
                    accepted.append(part)
                    break
                queue.append((destination, part))
                break
            elif (op == '<' and low < limit):
                passing_part = {**part, var: (low, limit)}
                part[var] = (limit, hi)
                if destination == 'R':
                    rejected.append(passing_part)
                    pass
                elif destination == 'A':
                    accepted.append(passing_part)
                else:
                    queue.append((destination, passing_part))
            elif (op == '>' and hi > limit):
                passing_part = {**part, var: (limit+1, hi)}
                part[var] = (low, limit+1)
                if destination == 'R':
                    rejected.append(passing_part)
                    pass
                elif destination == 'A':
                    accepted.append(passing_part)
                else:
                    queue.append((destination, passing_part))
    return sum(
        (reduce(mul, (hi - low for (low, hi) in part.values())) for part in accepted),
    )

assert (result := part2(test_data)) == 167409079868000, f"{result=}"
print("Part 2:", part2(adv.input()))
