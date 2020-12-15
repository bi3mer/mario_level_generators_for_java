from mario_vglc_grammars.Generation.Unconstrained import generate
from mario_vglc_grammars.IO import *
from .Generator import Generator

from typing import overload

class GrammarGenerator(Generator):
    def __init__(self, grammar, level):
        self.grammar = grammar
        levels = None
        if level == 'all':
            levels = get_super_mario_bros()
        else:
            levels = [get_single_super_mario_bros(f'mario-{level}.txt')]

        for lvl in levels:
            self.grammar.add_sequence(lvl)
        
        self.start_input = levels[0][:8]

    def generate_level(self, min_length):
        return generate(self.grammar, self.start_input, min_length)

    def generate_next_segment(self, min_length):
        return generate(self.grammar, self.start_input, min_length)