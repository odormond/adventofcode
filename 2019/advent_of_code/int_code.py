#! /usr/bin/env python

import asyncio
from itertools import product, permutations


class Halt(Exception):
    pass


class Computer:
    def __init__(self, memory, inputs=None, outputs=None):
        self.memory = memory[:]
        self.inputs = inputs or asyncio.Queue()
        self.outputs = outputs or asyncio.Queue()
        self.pc = 0
        self.relative_base = 0

    async def op_1(self, modes):
        """add"""
        a = self.load(0, modes)
        b = self.load(1, modes)
        self.save(a + b, 2, modes)
        return 4

    async def op_2(self, modes):
        """mul"""
        a = self.load(0, modes)
        b = self.load(1, modes)
        self.save(a * b, 2, modes)
        return 4

    async def op_3(self, modes):
        """input"""
        self.save(await self.inputs.get(), 0, modes)
        return 2

    async def op_4(self, modes):
        """output"""
        await self.outputs.put(self.load(0, modes))
        return 2

    async def op_5(self, modes):
        """jump if true"""
        if self.load(0, modes) != 0:
            self.pc = self.load(1, modes)
            return 0
        return 3

    async def op_6(self, modes):
        """jump if false"""
        if self.load(0, modes) == 0:
            self.pc = self.load(1, modes)
            return 0
        return 3

    async def op_7(self, modes):
        """less than"""
        if self.load(0, modes) < self.load(1, modes):
            self.save(1, 2, modes)
        else:
            self.save(0, 2, modes)
        return 4

    async def op_8(self, modes):
        """equals to"""
        if self.load(0, modes) == self.load(1, modes):
            self.save(1, 2, modes)
        else:
            self.save(0, 2, modes)
        return 4

    async def op_9(self, modes):
        self.relative_base += self.load(0, modes)
        return 2

    async def op_99(self, modes):
        """halt"""
        raise Halt

    def load(self, parameter, modes):
        try:
            mode = int(modes[parameter])
        except IndexError:
            mode = 0
        if mode == 0:  # Position mode
            addr = self.memory[self.pc+1+parameter]
        elif mode == 1:  # Immediate mode
            addr = self.pc+1+parameter
        elif mode == 2:  # Relative mode
            addr = self.relative_base + self.memory[self.pc+1+parameter]
        self.check_memsize(addr)
        return self.memory[addr]

    def save(self, value, parameter, modes):
        try:
            mode = int(modes[parameter])
        except IndexError:
            mode = 0
        if mode == 0:  # Position mode
            addr = self.memory[self.pc+1+parameter]
        elif mode == 2:  # Relative mode
            addr = self.relative_base + self.memory[self.pc+1+parameter]
        self.check_memsize(addr)
        self.memory[addr] = value

    def check_memsize(self, addr):
        assert addr >= 0
        mem_size = len(self.memory)
        if addr >= mem_size:
            self.memory[mem_size:addr+1] = [0] * (addr + 1 - mem_size)

    async def run(self):
        try:
            while True:
                op = self.memory[self.pc]
                modes = str(op//100)[::-1]
                op = op % 100
                step = await getattr(self, f'op_{op}')(modes)
                self.pc += step
        except Halt:
            pass
