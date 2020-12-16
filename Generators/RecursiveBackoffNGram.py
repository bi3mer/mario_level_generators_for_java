from typing import overload
from .GrammarGenerator import GrammarGenerator
from mario_vglc_grammars.Grammar import BackoffNGram as BG

class RecursiveBackoffNGram(GrammarGenerator):
    def __init__(self, n, level):
        weights = [0 for i in range(n)]
        weights[0] = 1
        super().__init__(BG(n, weights), level)

    def dda_update(self, columns):
        raise NotImplementedError()