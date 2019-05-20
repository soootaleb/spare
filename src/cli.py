from commands import *
from functions import get_commands

import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        help()
    else:

        cmds = get_commands()
        user_cmd = sys.argv[1]

        for cmd in cmds:
            if cmd[0] == user_cmd:
                cmd[1](sys.argv[2:])
        help()