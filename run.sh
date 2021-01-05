#!/bin/bash


trap "kill 0" EXIT

pypy3 give_Commands.py --mapelites --agent NO_ENEMY & 
pypy3 give_Commands.py --mapelites --agent NO_HIGH_JUMP & 
pypy3 give_Commands.py --mapelites --agent NO_JUMP &
pypy3 give_Commands.py --mapelites --agent NO_SPEED &
pypy3 give_Commands.py --mapelites --agent NO_FLAW &  

wait