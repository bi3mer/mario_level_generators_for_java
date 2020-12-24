import argparse
import sys

from CommandProcedures import TestMapElites

agent_help_str = '''Define agent to use:
    1. NO_ENEMY
    2. NO_HIGH_JUMP
    3. NO_JUMP
    4. NO_SPEED
    5. NO_FLAW
'''

def build_argument_parser():
    parser = argparse.ArgumentParser(description='Mario Level Generation.')
    parser.add_argument(
        '--mapelites', 
        action='store_true', 
        help='run a map elites test. Default agent is A*.')

    parser.add_argument(
        '--attempts-per-level', 
        type=int,
        default=10, 
        help='Set the number of times the java side will attempt to beat the level')

    parser.add_argument(
        '--max-level-time',
        type=int,
        default=10,
        help='The maximum time that Java can try to solve a level per attempt.'
    )
    
    parser.add_argument('--agent', help=agent_help_str)

    return parser

def get_agent(args):
    if args.agent != None:
        if args.agent == 'NO_ENEMY' or args.agent == 'NO_HIGH_JUMP' or \
           args.agent == 'NO_JUMP' or args.agent == 'NO_SPEED' or \
           args.agent == 'NO_FLAW':
           return args.agent
        else:
            print(f'{args.agent} is an invalid agent type. View help below.\n')
            print(agent_help_str)
            sys.exit(0)

    return 'NO_FLAW'

def main():
    '''
    Basic setup to build the two directories for Python and Java to chat if 
    they don't already exist
    '''
    parser = build_argument_parser()
    args = parser.parse_args()
    agent = get_agent(args)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    elif args.mapelites == True:
        runner = TestMapElites(agent)
        runner.run()

if __name__ == '__main__':
    main()