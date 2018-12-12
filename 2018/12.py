#! /usr/bin/env python3

from advent import Inputs

problem = [l.strip() for l in Inputs(2018).get(12).iter_lines(decode_unicode=True)]

initial_state = problem.pop(0).split(': ')[1]
problem.pop(0)
transitions = {state: new for state, new in (t.split(' => ') for t in problem)}


def pad(state, offset):
    # start = state.index('#')
    # end = state.rindex('#')
    # offset -= start
    # state = state[start:end+1]
    while state[:4] != '....':
        state = '.' + state
        offset += 1
    while state[-4:] != '....':
        state += '.'
    return state, offset


def evolve(state, transitions, generations):
    offset = 0
    for g in range(generations):
        prev_offset = offset
        prev_state = state
        state, offset = pad(state, offset)
        state = ''.join(transitions.get(state[w:w+5], '.') for w in range(len(state)-4))
        offset -= 2
        if prev_state == state:
            offset = (offset-prev_offset) * (generations-g-1) + offset
            break
    return offset, state


offset, state = evolve(initial_state, transitions, 20)
print("Part one:", sum(i-offset for i, pot in enumerate(state) if pot == '#'))


n_generations = 50000000000
try:
    offset, state = evolve(initial_state, transitions, n_generations)
except ValueError:
    offset = 0
    state = ''
print("Part two:", sum(i-offset for i, pot in enumerate(state) if pot == '#'))
