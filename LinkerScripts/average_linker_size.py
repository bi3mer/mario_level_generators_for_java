from mario_vglc_grammars.Utility import columns_into_level_string
from mario_vglc_grammars.Generation.Constrained import generate_from_start_to_end
from mario_vglc_grammars.IO.GetLevels import rows_into_columns
from mario_vglc_grammars.Grammar.NGram import NGram
from mario_vglc_grammars.IO import *
from mario_vglc_grammars.Utility import update_progress

class AverageLinkerSize():
    def __init__(self):

        self.linkers = []

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


    def __in_bounds(self, coordinate):
        RESOLUTION = 50
        return coordinate[0] >= 0 and coordinate[0] <= RESOLUTION and \
               coordinate[1] >= 0 and coordinate[1] <= RESOLUTION
    
    def run(self):
        # this shouldn't be hard-coded but oh well. 
        DIRECTIONS = ((0,1), (0,-1), (1, 0), (-1, 0))

        keys = set(self.bins.keys())

        i = 0
        total = len(keys) * 4
        for entry in keys:
            for dir in DIRECTIONS:
                neighbor = (entry[0] + dir[0], entry[1] + dir[1])
                while neighbor not in self.bins:
                    neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
                    if not self.__in_bounds(neighbor):
                        break

                if self.__in_bounds(neighbor) and neighbor in self.bins:
                    __, link_size = generate_from_start_to_end(
                        self.grammar, 
                        self.bins[entry], 
                        self.bins[neighbor], 
                        0,
                        include_path_length=True)

                    self.linkers.append(link_size)

                i += 1
                update_progress(i/total)
        
        print()
        print()
        print(f'min:  {min(self.linkers)}')
        print(f'mean: {sum(self.linkers) / len(self.linkers)}')
        print(f'max:  {max(self.linkers)}')


if __name__ == '__main__':
    a = AverageLinkerSize()
    a.run()