from .GrammarGenerator import GrammarGenerator
from mario_vglc_grammars.Grammar import NGram as NG

class RecursiveNGram(GrammarGenerator):
    def __init__(self, n, level):
        super().__init__(NG(n), level)

    def dda_update(self, columns):
        return super().dda_update(columns)