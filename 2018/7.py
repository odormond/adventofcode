#! /usr/bin/env python3

import functools
import re

from advent import Inputs


INSTRUCTION_RE = re.compile(r'Step (.) must be finished before step (.) can begin.')

instructions = [INSTRUCTION_RE.match(i).groups() for i in Inputs(2018).get(7).iter_lines(decode_unicode=True)]


@functools.total_ordering
class Step:
    def __init__(self, name):
        self.name = name
        self.duration = ord(name) - ord('A') + 61
        self.blocker = set()
        self.blockee = set()
        self.completed = False
        self.assigned = False

    def blocks(self, other):
        self.blockee.add(other)
        other.blocker.add(self)

    def complete(self):
        for b in self.blockee:
            b.blocker.remove(self)
        self.completed = True

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


def compile_steps(instructions):
    graph = {}
    for blocker, blockee in instructions:
        step = graph.setdefault(blocker, Step(blocker))
        step.blocks(graph.setdefault(blockee, Step(blockee)))
    return list(graph.values())


steps = compile_steps(instructions)

order = []
frees = sorted(s for s in steps if not s.blocker)
while frees:
    order.append(frees.pop(0))
    order[-1].complete()
    frees = sorted(s for s in steps if not s.blocker and not s.completed)

print("Part one:", ''.join(map(str, order)))


steps = compile_steps(instructions)

order = []
workers = [None] * 5
time = 0
while any(not s.completed for s in steps):
    for w, step in enumerate(workers):
        if step is not None and step.finished_at == time:
            step.complete()
            order.append(step)
            workers[w] = None
    for w, step in enumerate(workers):
        frees = sorted(s for s in steps if not s.blocker and not s.assigned)
        if step is None and frees:
            step = frees.pop(0)
            step.assigned = True
            step.finished_at = time + step.duration
        workers[w] = step
    time += 1

print(f"Part two: {''.join(map(str, order))} {time-1}s")
