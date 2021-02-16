#!/usr/bin/env python3
import sys
import os
import argparse

from ..execution import execute_file
from ..env import Environment

def main():
    parser = argparse.ArgumentParser(description='Execute Declair experiment definition file.')
    parser.add_argument('file', help='experiment definition to execute')
    parser.add_argument('-e', '--env',
                        help='environment file to use (default: check default candidate files)')
    
    args = parser.parse_args()
    env = Environment.from_file(args.env) if args.env else None

    # We want to make sure imports from the current working directory work
    # fine, since the required project package might not be pip-installed
    sys.path.insert(0, os.getcwd())

    execute_file(args.file, env)

if __name__ == '__main__':
    main()
