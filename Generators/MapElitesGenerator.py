from .Generator import Generator

from mario_vglc_grammars.IO.GetLevels import rows_into_columns
from mario_vglc_grammars.Grammar.NGram import NGram
from mario_vglc_grammars.IO import *
import os

class MapElitesGenerator(Generator):
    def __init__(self, n, level):
        # initialize map elites
        self.bins = {}

        f = open(os.path.join('data', 'data.csv'))
        f.readline()
        lines = f.readlines()
        f.close()

        for i, row in enumerate(lines):
            f = open(os.path.join('data', 'levels', f'{i}.txt'))
            segment = f.readlines()
            f.close()

            self.bins[(row[0], row[1])] = rows_into_columns(segment)

        # initialize grammar
        self.grammar = NGram(n)
        levels = None
        if level == 'all':
            levels = get_super_mario_bros()
        else:
            levels = [get_single_super_mario_bros(f'mario-{level}.txt')]

        for lvl in levels:
            self.grammar.add_sequence(lvl)
        
        self.start_input = levels[0][:8]
            