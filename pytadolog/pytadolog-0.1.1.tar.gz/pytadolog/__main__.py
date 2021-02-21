#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Main module for running TadoLogger from commandline.'''
import argparse
import datetime as dt
import logging

from . import TadoLogger


def main():
    '''Launch the TadoLogger.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outdir', help='path to output directory')
    parser.add_argument('--update-period', type=int,
                        help='time in seconds between updates',
                        default=30
                        )
    parser.add_argument('--last-day',
                        help='last day of week as 3 letter string',
                        default='sun',
                        )
    parser.add_argument('--disable-multiproc', action='store_false',
                        help="use single process for web query and csv saving",
                        dest='multiprocessing',
                        )
    parser.add_argument('-d', '--debug',
                        help='log debugging statements to file',
                        action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.WARNING,
                        )
    parser.add_argument('-v', '--verbose',
                        help='log info statements to file',
                        action='store_const', dest='loglevel', const=logging.INFO,
                        )
    args = parser.parse_args()
    with TadoLogger(args.outdir,
                    args.update_period,
                    args.last_day,
                    args.multiprocessing,
                    args.loglevel,
                    ) as tl:
        tl.start()
    print(f'Logging ended at {dt.datetime.now()}')


if __name__ == '__main__':
    main()
