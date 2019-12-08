#! /usr/bin/env python

from itertools import product

import advent_of_code as adv


class Halt(Exception):
    pass


class Computer:
    def __init__(self, memory, inputs=[], mode=0):
        self.memory = memory
        self.inputs = inputs
        self.outputs = []
        self.pc = 0

    def op_1(self, modes):
        """add"""
        a = self.load(0, modes)
        b = self.load(1, modes)
        self.save(a + b, 2)
        return 4

    def op_2(self, modes):
        """mul"""
        a = self.load(0, modes)
        b = self.load(1, modes)
        self.save(a * b, 2)
        return 4

    def op_3(self, modes):
        """input"""
        self.save(self.input(), 0)
        return 2

    def op_4(self, modes):
        """output"""
        self.output(self.load(0, modes))
        return 2

    def op_5(self, modes):
        """jump if true"""
        if self.load(0, modes) != 0:
            self.pc = self.load(1, modes)
            return 0
        return 3

    def op_6(self, modes):
        """jump if false"""
        if self.load(0, modes) == 0:
            self.pc = self.load(1, modes)
            return 0
        return 3

    def op_7(self, modes):
        """less than"""
        if self.load(0, modes) < self.load(1, modes):
            self.save(1, 2)
        else:
            self.save(0, 2)
        return 4

    def op_8(self, modes):
        """equals to"""
        if self.load(0, modes) == self.load(1, modes):
            self.save(1, 2)
        else:
            self.save(0, 2)
        return 4

    def op_99(self, modes):
        """halt"""
        raise Halt

    def load(self, parameter, modes):
        try:
            mode = int(modes[parameter])
        except IndexError:
            mode = 0
        if mode == 0:
            return self.memory[self.memory[self.pc+1+parameter]]
        elif mode == 1:
            return self.memory[self.pc+1+parameter]

    def save(self, value, parameter):
        self.memory[self.memory[self.pc+1+parameter]] = value

    def input(self):
        return self.inputs.pop(0)

    def output(self, value):
        self.outputs.append(value)

    def run(self):
        try:
            while True:
                op = self.memory[self.pc]
                modes = str(op//100)[::-1]
                op = op % 100
                step = getattr(self, f'op_{op}')(modes)
                self.pc += step
        except Halt:
            pass


for program, result in (
    ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
):
    computer = Computer(program)
    computer.run()
    assert computer.memory == result


program = adv.input(2, adv.to_list_of_int)
computer = Computer(program[0:1] + [12, 2] + program[3:])
computer.run()

assert computer.memory[0] == 2894520


target_value = 19690720
for noun, verb in product(range(100), repeat=2):
    computer = Computer(program[0:1] + [noun, verb] + program[3:])
    computer.run()
    if computer.memory[0] == target_value:
        assert 100 * noun + verb == 9342
        break


TEST = adv.input(5, adv.to_list_of_int)
computer = Computer(TEST[:], [1])
computer.run()
print("Part one:", computer.outputs[-1])


for program, inputs, outputs in (
    ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], ([0], [8]), ([0], [1])),
    ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], ([0], [8]), ([1], [0])),
    ([3, 3, 1108, -1, 8, 3, 4, 3, 99], ([0], [8]), ([0], [1])),
    ([3, 3, 1107, -1, 8, 3, 4, 3, 99], ([0], [8]), ([1], [0])),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], ([0], [2]), ([0], [1])),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], ([0], [2]), ([0], [1])),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], ([0], [8], [16]), ([999], [1000], [1001])),
):
    for input_, output in zip(inputs, outputs):
        computer = Computer(program[:], input_)
        computer.run()
        assert computer.outputs == output


TEST = adv.input(5, adv.to_list_of_int)
computer = Computer(TEST[:], [5])
computer.run()
print("Part two:", computer.outputs[-1])
