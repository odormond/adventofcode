#! /usr/bin/env python3

import re
import sys

from advent import Inputs

source = Inputs(2018).get(20).text.strip()
sys.setrecursionlimit(10000)


#source = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
#source = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
source = open('20-1.txt').read().strip()


class Alternatives:
    def __init__(self):
        self.branches = [Sequence()]
    
    def branch(self):
        self.branches.append(Sequence())

    def add(self, element):
        self.branches[-1].add(element)

    def __len__(self):
        lengths = [len(b) for b in self.branches]
        l = max(lengths) // (1 if min(lengths) > 0 else 2)
        print(lengths, '->', l)
        return l


class Sequence:
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def __len__(self):
        return sum(len(e) for e in self.elements)


stack = [Sequence()]
for char in source[1:-1]:
    if char in 'NESW':
        stack[-1].add(char)
    elif char == '(':
        a = Alternatives()
        stack[-1].add(a)
        stack.append(a)
    elif char == '|':
        stack[-1].branch()
    elif char == ')':
        stack.pop()


print("Part one:", max(map(len, stack)))
