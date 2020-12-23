from pathlib import Path
import os

def get_directories():
    return os.path.join(Path.home(), 'toPython'), \
           os.path.join(Path.home(), 'toJava')

def clear_directory(dir_path):
    for filename in os.listdir(dir_path):
        os.remove(os.path.join(dir_path, filename))

def set_up_directories():
    input_dir, output_dir = get_directories()
    
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
    else:
        clear_directory(input_dir)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    else:
        clear_directory(output_dir)
