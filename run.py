from pathlib import Path
import traceback 
import os

from mario_vglc_grammars.Utility import columns_into_rows
from Generators import *

def build_qd(args):
    raise NotImplementedError('QD not implemented')


def build_generator(cmd):
    args = cmd.split('_')[3:]
    generator = None

    if 'backoffngram' in cmd:
        generator = BackoffNGram(int(args[0]), args[1])
    elif 'ngram' in cmd:
        generator = NGram(int(args[0]), args[1])
    elif 'qd' in cmd:
        raise NotImplementedError()
        # generator = build_qd(args[0], int(args[1]))
    else:
        raise Exception(f'Unknown generator requested in command: {cmd}')

    return generator

def main():
    '''
    Basic setup to build the two directories for Python and Java to chat if 
    they don't already exist
    '''
    input_dir = os.path.join(Path.home(), 'toPython')
    outputDir = os.path.join(Path.home(), 'toJava')
    
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)

    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)

    generator = None

    '''
    Commands:
        cmd_generate_[length]
            This file name tells us to use teh current generator to build a level
            of the given length. The length must be greater than 0, else it will
            not be accepted and an error will be sent to Java. Another potential
            error is that a generator has not been assigned.

        cmd_new_[type]_[args*]
            This command signifies that a new generator should be instantiated 
            for use. The type can be any of the following:
                - ngram
                - backoffngram
                - qd

            Each of these come with their own arguments. N-Gram and Backoff-N-Gram
            both take the same arguments. The first argument is [n] which 
            represents the size of the grammar. The next argument is [level] 
            which can either be a single mario level, such as 1-1, or be "all"
            which represents the entire corpus being used.
            
                            cmd_new_ngram_[n]_[level]
                            cmd_new_backoffngram_[n]_[level]

            While the n-gram can be created on the spot, the QD is going to be
            best served if we build the table offline. The first argument is
            the [level] which has the same functionality as the n-gram. Except
            now its going to be part of determining whether a folder exists or
            not. The second argument is how many [iterations] are run. At the 
            moment the command doesn't allow for specifing the objective 
            function used but it could in the future.

                            cmd_new_qd_[level]_[iterations]
            
        When there is an error that any of the commands run into, a file named 
        "error" will be put in the toJava directory. This side is expected to 
        have output a helpful error message and the Java side should tell the 
        user that an error occurred on the Python side and to check the logs.
    '''
    while True:
        for file_name in os.listdir(input_dir):
            try:
                if file_name.startswith('cmd_generate'):
                    length = int(file_name.split('_')[-2])
                    level = generator.generate_level(length)
                    
                    # signal to Java that we're writing the level right now
                    lock_file_path = os.path.join(outputDir, 'lock')
                    Path(lock_file_path).touch()

                    # write the level
                    f = open(os.path.join(outputDir, 'level'), 'w')
                    f.write(columns_into_rows(level))
                    f.close()

                    # signal to Java that we're done and it can proceed
                    os.remove(lock_file_path)

                elif file_name.startswith('cmd_new'):
                    generator = build_generator(file_name)
                else:
                    print(f'Unknown Input: {file_name}')
            except Exception as e:
                print(f'Exception encountered for: {file_name}')
                traceback.print_exc()
                print(e)

                Path(os.path.join(outputDir, 'error')).touch()

            print(f'Removing {file_name}')
            os.remove(os.path.join(input_dir, file_name))

if __name__ == '__main__':
    main()