from .MapElitesGenerator import MapElitesGenerator

from mario_vglc_grammars.Generation.Constrained import generate_from_start_to_end
from random import sample

class RandomMapElites(MapElitesGenerator):
    def generate_level(self, min_length):
        # TODO: combine the new value with the old with constrained generation
        level = []
        while len(level) < min_length:
            key = sample(self.bins.keys(), 1)[0]
            extension = self.bins[key]

            if len(level) == 0:
                level = extension
            else:
                level = generate_from_start_to_end(self.grammar, level, extension, 1)

        return level

    def generate_next_segment(self, min_length):
        level = []
        while len(level) < min_length:
            key = sample(self.bins.keys(), 1)[0]
            extension = self.bins[key]
            level.extend(extension)

        return level