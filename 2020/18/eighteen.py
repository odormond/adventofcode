#! /usr/bin/env python3

from collections import namedtuple
import re
import os.path
import advent_of_code as adv


PARENTHESE_RE = re.compile(r'\([^()]*\)')


BinOp = namedtuple("BinOp", "left right op")


def tokenize(expr):
    tokens = []
    num = ''
    for c in expr + ' ':  # Ensure any last token is pushed out
        if c == ' ':
            if num:
                tokens.append(int(num))
                num = ''
        elif c in '()+*':
            if num:
                tokens.append(int(num))
                num = ''
            tokens.append(c)
        elif c in '1234567890':
            num += c
        else:
            raise ValueError(f"Unparsable symbol: {c}")
    return tokens


def eval_l_to_r(expr):
    expr = expr[:]
    while len(expr) > 1:
        for i in range(1, len(expr) - 1):
            a, op, b = expr[i - 1 : i + 2]
            if isinstance(a, int) and isinstance(b, int) and op in '+*':
                expr[i - 1 : i + 2] = [a + b if op == '+' else a * b]
                break
            elif isinstance(op, int) and a == '(' and b == ')':
                expr[i - 1 : i + 2] = [op]
                break
        else:
            raise ValueError(f"Failed to simplify expression: {expr}")
    return expr[0]


def eval_p_to_m(expr):
    expr = expr[:]
    while len(expr) > 1:
        for i in range(1, len(expr) - 1):
            a, op, b = expr[i - 1 : i + 2]
            if isinstance(a, int) and isinstance(b, int):
                if op == '+':
                    expr[i - 1 : i + 2] = [a + b]
                    break
                elif (
                    op == '*'
                    and (i == 1 or expr[i - 2] != '+')
                    and (i == len(expr) - 2 or expr[i + 2] != '+')
                ):
                    expr[i - 1 : i + 2] = [a * b]
                    break
            elif isinstance(op, int) and a == '(' and b == ')':
                expr[i - 1 : i + 2] = [op]
                break
        else:
            raise ValueError(f"Failed to simplify expression: {expr}")
    return expr[0]


TESTS = (
    ('1 + 2 * 3 + 4 * 5 + 6', 71, 231),
    ('1 + (2 * 3) + (4 * (5 + 6))', 51, 51),
    ('2 * 3 + (4 * 5)', 26, 46),
    ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445),
    ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240, 669060),
    ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632, 23340),
)
for expr, l_to_r, p_to_m in TESTS:
    expr = tokenize(expr)
    assert eval_l_to_r(expr) == l_to_r
    assert eval_p_to_m(expr) == p_to_m

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_str)
print("Part 1:", sum(eval_l_to_r(tokenize(expr)) for expr in data))
print("Part 2:", sum(eval_p_to_m(tokenize(expr)) for expr in data))
