from mario_vglc_grammars.Utility import columns_into_level_string
from Utility.IO import get_directories, set_up_directories

from os import remove, listdir
from subprocess import Popen
from atexit import register
from pathlib import Path
from os.path import join
from sys import exit

class CommandProcedure:
    def __init__(self, agent):
        self.agent = agent
        set_up_directories(agent)
        self.input_dir, self.output_dir = get_directories(agent)

        self.proc = Popen(['java', '-jar', 'mario_simulator.jar', agent])
        register(self.__del__)

    def __del__(self):
        self.proc.kill()
        self.proc.terminate()

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
        percent_complete = -1

        while percent_complete == -1:
            files = listdir(self.input_dir)

            if len(files) == 1:
                if '_done' in files[0]:
                    percent_complete = float(files[0].split('_')[0])
                else:
                    print(f'Unknown result type: {files[0]}')
                    exit(-1)

                remove(join(self.input_dir, files[0]))

        return percent_complete
