from mario_vglc_grammars.Utility import columns_into_level_string
from mario_vglc_grammars.Generation.Constrained import generate_from_start_to_end
from mario_vglc_grammars.IO.GetLevels import rows_into_columns
from mario_vglc_grammars.Grammar.NGram import NGram
from mario_vglc_grammars.IO import get_super_mario_bros
import os

# f = open(os.path.join('data', 'levels', f'230.txt'))
f = open(os.path.join('data', 'levels', f'124.txt'))
start = rows_into_columns(f.readlines())
f.close()

# f = open(os.path.join('data', 'levels', f'121.txt'))
f = open(os.path.join('data', 'levels', f'121.txt'))
end = rows_into_columns(f.readlines())
f.close()

grammar = NGram(3)
levels = get_super_mario_bros()
for lvl in levels:
    grammar.add_sequence(lvl)

lvl, path_length = generate_from_start_to_end(
    grammar, 
    start, 
    end, 
    0,
    include_path_length=True)

link = []
end_of_start_index = len(start)
start_of_end_index = len(lvl) - len(end)

print("path length: " + str(path_length))
print(len(start))
print(len(end))
print(len(lvl))
# print(end_of_start_index, start_of_end_index)
# for i in range(end_of_start_index, start_of_end_index - 1):
#     link.append(lvl[i])

# print(len(link), path_length)
# print(lvl)
print(columns_into_level_string(lvl))
print()
print(columns_into_level_string(start + end))
print()
print(columns_into_level_string(start))
print()
print(columns_into_level_string(end))