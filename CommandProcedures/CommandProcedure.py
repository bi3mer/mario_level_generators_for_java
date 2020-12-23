from mario_vglc_grammars.Utility import columns_into_level_string
from Utility.IO import get_directories, set_up_directories

from os import remove, listdir
from pathlib import Path
from os.path import join
from sys import exit

class CommandProcedure:
    def __init__(self):
        set_up_directories()
        self.input_dir, self.output_dir = get_directories()

    def create_argument_file(self, name):
        Path(join(self.output_dir, name)).touch()
        
    def create_command(self, arguments):
        args = '_'.join(arguments)
        cmd = f'cmd_agent_{self.agent}_{args}'
        self.create_argument_file(cmd)

    def send_level(self, level):
        # create temp file to tell java to wait
        self.create_argument_file('lock')

        # write level file
        f = open(join(self.output_dir, 'level.txt'), 'w')
        f.write(columns_into_level_string(level))
        f.close()

        # delete level file which tells java it's okay to read the level file
        remove(join(self.output_dir, 'lock'))

    def get_level_sent_result(self):
        result = None

        while result == None:
            files = listdir(self.input_dir)

            if len(files) == 1:
                if 'true' in files[0]:
                    result = True
                elif 'false' in files[0]:
                    result = False
                else:
                    print(f'Unknown result type: {files[0]}')
                    exit(-1)

                remove(join(self.input_dir, files[0]))


        return result
