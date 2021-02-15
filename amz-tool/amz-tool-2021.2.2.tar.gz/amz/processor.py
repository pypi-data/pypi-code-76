# Helper for process handling - fancy wrapper around subprocess

import time
import subprocess as sp

from amz.loading import Loading


# Classifies into normal commands, python commands
def classify_cmds(command):
    # Acquire prefix code
    try:
        cmd_prefix = command[:4]
    except IndexError:
        return -1, None
    # Check python command
    if cmd_prefix == 'pyx>':
        return 1, command[4:]
    # Check Re-sudo command
    if cmd_prefix == 'rsu>':
        return 2, command[4:]
    # Else it's a normal command
    return 0, command


def run_cmd(command, name='', prestr='', verbose=False):

    l = Loading(name if name != '' else f'Executing `{command}`', input_prestr=prestr)
    cmd_type, cmd_exec = classify_cmds(command)

    if cmd_type == 0:
        p = sp.run(cmd_exec, shell=True, stdout=None if verbose else sp.PIPE, stderr=None if verbose else sp.PIPE)
        l.end(p.returncode)
    elif cmd_type == 1:
        try:
            exec(cmd_exec)
            l.end(0)
        except:
            l.end(1)
    elif cmd_type == 2:
        p = sp.run(f"sudo -p '{prestr}Need [sudo] access again: ' echo '{prestr}Thanks!'", shell=True)
        l.end(0)
    else:  # cmd_type == -1:
        print(f"Invalid Command - {command}")

    # Give some rest
    time.sleep(0.1)
