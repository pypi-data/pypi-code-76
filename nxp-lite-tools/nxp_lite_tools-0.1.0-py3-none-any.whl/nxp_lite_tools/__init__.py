#!/usr/bin/env python3
#-*-coding:utf-8-*-

import os

def main():
    help = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'help')
    with open(help, 'r') as f:
        print(f.read())


if __name__ == "__main__":
    main()
