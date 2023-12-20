#! /usr/bin/env python

from collections import defaultdict
import advent_of_code as adv

test_data_1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

test_data_2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


class Module:
    def __init__(self, name):
        self.name = name
        self.outputs = []

    def set_outputs(self, outputs):
        self.outputs = list(outputs)

    def set_inputs(self, inputs):
        pass

    def pulse(self, inp, signal, queue):
        for out in self.outputs:
            queue.append((self, out, signal))


class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = 0

    def pulse(self, inp, signal, queue):
        if signal == 1:
            return
        self.state = (self.state + 1) % 2
        super().pulse(inp, self.state, queue)


class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = {}

    def set_inputs(self, inputs):
        self.state = {inp: 0 for inp in inputs}

    def pulse(self, inp, signal, queue):
        self.state[inp] = signal
        signal = 0 if all(self.state.values()) else 1
        super().pulse(inp, signal, queue)


class Broadcaster(Module):
    pass


class Sink(Module):
    def pulse(self, inp, signal, queue):
        pass


def parse(data):
    modules = {}
    module_outputs = {}
    module_inputs = defaultdict(list)
    for line in data.splitlines():
        inp, outs = line.split(' -> ')
        if inp == 'broadcaster':
            name = inp
            modules[name] = Broadcaster(name)
        elif inp[0] == '%':
            name = inp[1:]
            modules[name] = FlipFlop(name)
        elif inp[0] == '&':
            name = inp[1:]
            modules[name] = Conjunction(name)
        module_outputs[name] = outs.split(', ')
        for out in module_outputs[name]:
            module_inputs[out].append(name)

    for sink in {o for m in module_outputs.values() for o in m} - set(modules):
        modules[sink] = Sink(sink)
        module_outputs[sink] = []
        module_inputs[sink] = []

    for name, module in modules.items():
        module.set_outputs(modules[m] for m in module_outputs[name])
        module.set_inputs(modules[m] for m in module_inputs[name])

    return modules['broadcaster']


def part1(data):
    broadcaster = parse(data)
    signals = [0, 0]
    for i in range(1000):
        queue = []
        signals[0] += 1
        broadcaster.pulse(None, 0, queue)
        while queue:
            inp, out, signal = queue.pop(0)
            signals[signal] += 1
            out.pulse(inp, signal, queue)
    return signals[0] * signals[1]


assert (result := part1(test_data_1)) == 32000000, f"{result=}"
assert (result := part1(test_data_2)) == 11687500, f"{result=}"
print("Part 1:", part1(adv.input()))


"""
broadcaster
 -> %kt -> jv
           %mt -> jv
                  %zp -> %rc -> %hj -> %vc -> jv
                                              %hf -> %nm -> %dh -> jv
                                                                   %mc -> jv
                                                                          %lv -> jv
                                                                                 %tg -> jv
                                                            jv
 -> 111110100011 = 4003
    &jv -> %hj (jv += 10000 (16))
           %rc (jv += 1000 (8))
           %kt (jv += 1)
           &ln
           %zp (jv += 100 (4))
           %hf (jv += 1000000 (64)) -> 4096

    %pd -> pr
           %jp -> %mx -> %cl -> %hm -> %qb -> %bf -> %vx -> %ns -> pr
                                                                   %pn -> pr
                                                                          %cb -> pr
                                                                                 %tk -> pr
                                                     pr
                                              pr
                         pr
                  pr
 -> 111101100111 = 3943
    &pr -> %pd (pr += 1)
           %vx (pr += 10000000 (128))
           &vn
           %cl (pr += 1000 (8))
           %hm (pr += 10000 (16))  -> 4096

    %xv -> %nd -> %dg -> %tm -> %mh -> %mk -> %pb -> %tp -> %pf -> %mf -> %gv -> jm
                                                                                 %km -> jm
                                                                          jm
                                                                   jm
                                                            jm
                                       jm
                         jm
           jm

 -> 111110010101 = 3989
    &jm -> %pb (jm += 1000000 (64))
           %tm (jm += 1000 (8))
           &zx
           %mk (jm += 100000 (32))
           %xv (jm += 1)
           %nd (jm += 10 (2))      -> 4096

    %rg -> qs
           %vq -> %bs -> %sc -> %mv -> qs
                                       %gl -> %kf -> %dx -> %ts -> %ng -> qs
                                                                          %lh -> qs
                                                                                 %dl -> qs
                                                                   qs
                         qs
                  qs
 -> 111100010111 = 3863
    &qs -> %kf (qs += 1000000 (64)) -> 3927
           &dr
           %sc (qs += 1000 (8))        -> 3935
           %rg (qs += 1)                  -> 3936
           %gl (qs += 100000 (32))           -> 3968
           %dx (qs += 10000000 (128))           -> 4096 = 0


&jv -> &ln -> &kj
&pr -> &vn -> &kj -> rx
&jm -> &zx -> &kj
&qs -> &dr -> &kj
"""

print("Part 2:", 4003 * 3943 * 3989 * 3863)
