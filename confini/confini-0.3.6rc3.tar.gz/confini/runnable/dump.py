# standard imports
import sys
import logging
import argparse

# local imports
from confini import Config

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


argparser = argparse.ArgumentParser()
argparser.add_argument('-z', action='store_true', help='Truncate values in output')
argparser.add_argument('-v', action='store_true', help='Be verbose')
argparser.add_argument('config_dir', type=str, help='Configuation directory to parse')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)


def main():
    c = Config(args.config_dir)
    c.process()
    for k in c.store.keys():
        v = c.get(k)
        if args.z or v == None:
            v = ''
        print('{}={}'.format(k, v))


if __name__ == "__main__":
    main()
