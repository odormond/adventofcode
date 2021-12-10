#! /usr/bin/env python

import re
from pathlib import Path
import advent_of_code as adv

test_data = adv.to_list_of_str("""\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""")
data = adv.input(Path(__file__).parent.name, adv.to_list_of_str)

CORRUPTION_SCORE = {
    '': 0,
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
CORRUPT_RE = re.compile(r'\([\]}>]|\[[)}>]|\{[)\]>]|<[)\]}]')

def find_first_corrupt_char_and_to_complete(line):
    while line:
        if match := CORRUPT_RE.search(line):
            return line[match.end()-1], None
        orig = line
        for empty in ('()', '[]', '{}', '<>'):
            line = line.replace(empty, '')
        if line == orig:
            return '', line
    return '', ''


def syntax_error_score(data):
    return sum(CORRUPTION_SCORE[find_first_corrupt_char_and_to_complete(line)[0]] for line in data)


assert syntax_error_score(test_data) == 26397
print("Part 1:", syntax_error_score(data))


AUTOCOMPLETION_SCORE = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

def autocomplete_score(data):
    scores = []
    for line in data:
        corrupt, to_complete = find_first_corrupt_char_and_to_complete(line)
        if corrupt:
            continue
        score = 0
        for char in reversed(to_complete):
            score = score * 5 + AUTOCOMPLETION_SCORE[char]
        scores.append(score)
    scores = sorted(scores)
    assert len(scores) % 2 == 1
    return scores[len(scores)//2]


assert autocomplete_score(test_data) == 288957
print("Part 2:", autocomplete_score(data))
