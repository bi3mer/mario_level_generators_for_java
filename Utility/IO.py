from os.path import isdir,join
from os import listdir, remove, mkdir

def get_directories(agent):
    return join(agent, 'toPython'), join(agent, 'toJava')

def clear_directory(dir_path):
    for filename in listdir(dir_path):
        remove(join(dir_path, filename))

def set_up_directories(agent):
    input_dir, output_dir = get_directories(agent)

    if not isdir(agent):
        mkdir(agent)
    
    if not isdir(input_dir):
        mkdir(input_dir)
    else:
        clear_directory(input_dir)

    if not isdir(output_dir):
        mkdir(output_dir)
    else:
        clear_directory(output_dir)
