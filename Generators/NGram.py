from .GrammarGenerator import GrammarGenerator
from mario_vglc_grammars.Grammar import NGram as NG

class NGram(GrammarGenerator):
    def __init__(self, n, level):
        super().__init__(NG(n), level)
