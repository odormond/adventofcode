#! /usr/bin/env python3

from advent import Inputs


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def print(self, indent=''):
        print(f'{indent}{self.metadata}')
        for child in self.children:
            child.print(indent + '  ')

    def sum_metadata(self):
        return sum(self.metadata) + sum(c.sum_metadata() for c in self.children)

    def value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            return sum(self.children[i-1].value() for i in self.metadata if 0 <= i-1 < len(self.children))

    def __repr__(self):
        return f'N({self.children}, {self.metadata})'


data = [int(n) for n in Inputs(2018).get(8).text.split()]

stack = []
while data:
    n_children, n_metadata, *data = data
    if n_children:
        stack.append(Node(n_children, n_metadata))
    else:
        metadata, data = data[:n_metadata], data[n_metadata:]
        stack.append(Node([], metadata))
        progress = True
        while progress:
            progress = False
            for i, node in enumerate(reversed(stack)):
                if isinstance(node.children, list):
                    continue
                elif node.children == i:
                    stack, node.children = stack[:-i], stack[-i:]
                    node.metadata, data = data[:node.metadata], data[node.metadata:]
                    progress = True
                break


root = stack[0]

print("Part one:", root.sum_metadata())

print("Part two:", root.value())
