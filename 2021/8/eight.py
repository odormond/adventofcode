#! /usr/bin/env python

from pathlib import Path
import advent_of_code as adv

test_data = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
test_data2 = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""
data = adv.input(Path(__file__).parent.name, str)


def parse(text):
    unique, output = text.split(' | ')
    digits = unique.split()
    output = output.split()
    return digits, output


digits_by_segment_count = {2: '1', 3: '7', 4: '4', 7: '8', }

assert sum(1 for line in test_data2.strip().splitlines() for digit in parse(line)[1] if len(digit) in digits_by_segment_count) == 26

print("Part 1:", sum(1 for line in data.strip().splitlines() for digit in parse(line)[1] if len(digit) in digits_by_segment_count))


def guess_layout(digits):
    digits = [''.join(sorted(digit)) for digit in sorted(digits, key=len)]
    one, seven, four, _, _, _, _, _, _, eight = digits
    two_three_five = set(digits[3:6])
    zero_six_nine = set(digits[6:9])
    for digit in zero_six_nine:
        if len(set(digit) - set(seven)) == 4:
            six = digit
    zero_nine = zero_six_nine - {six}
    for digit in two_three_five:
        if len(set(digit) - set(seven)) == 2:
            three = digit
    two_five = two_three_five - {three}
    for zero_or_nine in zero_nine:
        for two_or_five in two_five:
            if set(two_or_five).issubset(set(zero_or_nine)):
                five = two_or_five
                nine = zero_or_nine
    two = (two_five - {five}).pop()
    zero = (zero_nine - {nine}).pop()

    return {
        zero: '0',
        one: '1',
        two: '2',
        three: '3',
        four: '4',
        five: '5',
        six: '6',
        seven: '7',
        eight: '8',
        nine: '9',
    }


def read_output(digits, output):
    layout = guess_layout(digits)
    return int(''.join(layout[''.join(sorted(digit))] for digit in output))


assert read_output(*parse(test_data)) == 5353
assert sum(read_output(*parse(line)) for line in test_data2.strip().splitlines()) == 61229
print("Part 2:", sum(read_output(*parse(line)) for line in data.strip().splitlines()))
