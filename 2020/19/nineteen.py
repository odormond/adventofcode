#! /usr/bin/env python3

import re
import os.path
import advent_of_code as adv

TEST = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""


def compile(rule, rules):
    rule, recursive = rule
    if recursive:
        a, b = map(str.split, rule.split(' | '))
        recursion_id = set(a).symmetric_difference(b).pop()
        if recursion_id in b:
            a = b
        recursion_point = a.index(recursion_id)
        left = ''.join(compile((atom, False), rules) for atom in a[:recursion_point])
        right = ''.join(compile((atom, False), rules) for atom in a[recursion_point + 1 :])
        if left and right:
            # sync counts
            return '(' + left + '){n}(' + right + '){n}'
        elif left:
            return '(' + left + ')+'
        return '(' + right + ')+'
    if '|' in rule:
        return (
            '('
            + '|'.join(
                sorted(compile((alternate, False), rules) for alternate in rule.split(' | '))
            )
            + ')'
        )
    elif ' ' in rule:
        return ''.join(compile((atom, False), rules) for atom in rule.split())
    elif rule[0] == '"':
        return rule[1:-1]
    else:
        return compile(rules[rule], rules)


def rules_to_regex(rules):
    rules = {
        id: (content, id in content.split()) for rule in rules for id, content in (rule.split(':'),)
    }
    regex = '^' + compile(rules["0"], rules) + '$'
    return ''.join(regex)


def parse_input(text):
    rules, messages = text.strip().split('\n\n')
    rule = rules_to_regex(rules.splitlines())
    messages = messages.splitlines()
    return rule, messages


rule, messages = parse_input(TEST)
assert {msg for msg in messages if re.match(rule, msg)} == {'ababbb', 'abbbab'}

TEST2 = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""

rule, messages = parse_input(TEST2)
assert {msg for msg in messages if re.match(rule, msg)} == {
    'bbabbbbaabaabba',
    'ababaaaaaabaaab',
    'ababaaaaabbbaba',
}
rule, messages = parse_input(
    TEST2.replace('8: 42', '8: 42 | 42 8').replace('11: 42 31', '11: 42 31 | 42 11 31')
)
assert {
    msg for msg in messages if any(re.match(rule.replace('n', str(i)), msg) for i in range(1, 10))
} == {
    'bbabbbbaabaabba',
    'babbbbaabbbbbabbbbbbaabaaabaaa',
    'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
    'bbbbbbbaaaabbbbaaabbabaaa',
    'bbbababbbbaaaaaaaabbababaaababaabab',
    'ababaaaaaabaaab',
    'ababaaaaabbbaba',
    'baabbaaaabbaaaababbaababb',
    'abbbbabbbbaaaababbbbbbaaaababb',
    'aaaaabbaabaaaaababaa',
    'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
    'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
}

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), str)
rule, messages = parse_input(data)
print("Part 1:", len([msg for msg in messages if re.match(rule, msg)]))

rule, messages = parse_input(
    data.replace('8: 42', '8: 42 | 42 8').replace('11: 42 31', '11: 42 31 | 42 11 31')
)
# print(rule.pattern)
# print('\n'.join(msg for msg in messages if rule.match(msg)))
print(
    "Part 2:",
    len(
        {
            msg
            for msg in messages
            if any(re.match(rule.replace('n', str(i)), msg) for i in range(1, 10))
        }
    ),
)
