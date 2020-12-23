from mario_vglc_grammars.Utility import columns_into_level_string
from mario_vglc_grammars.Generation.Constrained import generate_from_start_to_end
from mario_vglc_grammars.IO.GetLevels import rows_into_columns
from mario_vglc_grammars.Grammar.NGram import NGram
from mario_vglc_grammars.IO import *
from mario_vglc_grammars.Utility import update_progress

from .CommandProcedure import CommandProcedure

import json

class TestMapElites(CommandProcedure):
    def __init__(self):
        super().__init__()

         # initialize map elites
        self.bins = {}

        f = open(os.path.join('data', 'validated.csv'))
        lines = f.readlines()
        f.close()

        for i, row in enumerate(lines):
            row = row.split(',')
            if 'true' in row[3]:
                path = os.path.join('data', 'levels', f'{i}.txt')
                if os.path.exists(path):
                    f = open(path)
                    segment = f.readlines()
                    f.close()

                    self.bins[(int(row[0]), int(row[1]))] = rows_into_columns(segment)

        # initialize grammar
        self.grammar = NGram(3)
        levels = get_super_mario_bros()
        for lvl in levels:
            self.grammar.add_sequence(lvl)

    def test_entry(self, entry, entry_is_valid):
        str_entry = str(entry)
        if str_entry not in entry_is_valid:
            entry_is_valid[str_entry] = {}
            entry_is_valid[str_entry]['neighbors'] = {}

        # we already tested when we created validated.csv
        entry_is_valid[str_entry]['playable'] = True 

    def test_two_entries(self, entry_one, entry_two, entry_is_valid):
        str_entry_one = str(entry_one)
        str_entry_two = str(entry_two)
        
        if str_entry_one not in entry_is_valid:
            entry_is_valid[str_entry_one] = {}
            entry_is_valid[str_entry_one]['neighbors'] = {}

        level = generate_from_start_to_end(
            self.grammar, 
            self.bins[entry_one], 
            self.bins[entry_two], 
            0)

        self.send_level(columns_into_level_string(level))
        entry_is_valid[str_entry_one]['neighbors'][str_entry_two] = self.get_level_sent_result()
    
    def run(self):
        # this shouldn't be hard-coded but oh well. 
        RESOLUTION = 50
        entry_is_valid = {}
        keys = set(self.bins.keys())

        i = 0
        for entry in keys:
            update_progress(i/len(keys))
            i += 1

            self.test_entry(entry, entry_is_valid)

            # note that this isn't the complete list of neighbors but as long 
            # as we test to the right and up every bin will be tested. The
            # implementation I'm going with is pretty lazy with code duplication
            # but we only duplicate once so it isn't the end of the world.
            #
            # look for coordinate to the right
            neighbor = (entry[0] + 1, entry[1])
            while neighbor not in self.bins:
                neighbor = (neighbor[0] + 1, neighbor[1])
                if neighbor[0] > RESOLUTION:
                    break

            if neighbor[0] <= RESOLUTION and neighbor in self.bins:
                    
                self.test_entry(neighbor, entry_is_valid)
                self.test_two_entries(entry, neighbor, entry_is_valid)

            # look for coordinate above.
            neighbor = (entry[0], entry[1] + 1)
            while neighbor not in self.bins:
                neighbor = (neighbor[0], neighbor[1] + 1)
                if neighbor[1] > RESOLUTION:
                    break

            if neighbor[1] <= RESOLUTION and neighbor in self.bins:
                self.test_entry(neighbor, entry_is_valid)
                self.test_two_entries(entry, neighbor, entry_is_valid)

        f = open('results.json', 'w')
        f.write(json.dumps(entry_is_valid, indent=2))
        f.close()

        update_progress(1)
