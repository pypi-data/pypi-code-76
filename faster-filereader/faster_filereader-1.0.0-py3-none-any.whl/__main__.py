#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Oct 26 14:22:46 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: __main__.py -*-
# -*- purpose: -*-

'''
Module docstring
'''

import sys
import os
import time
import argparse

from typing import Dict

import faster


if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser(description='Faster module call routines')
    parser.add_argument('action', type=str,
                        default='', choices=('more', 'stats', 'test'),
                        help="Action to perform")
    parser.add_argument('--nmax', type=int,
                        default=faster.const.max_number_of_events_in_file, nargs='?',
                        help='maximum number of event to read')
    parser.add_argument('files', type=str,
                        nargs='*', help="Faster files to read")
    args = parser.parse_args()

    if args.action == 'test':
        print("# Starting test ...")
        modpath = os.path.abspath(faster.event.__file__)[:-8]
        print(f"# Module's path is '{modpath}'")
        fpath = "".join([modpath, "test/test_0001.fast"])
        n_event_read = 0
        start_time = time.time()
        with faster.FileReader(fpath,
                               faster.const.max_number_of_events_in_file) as fasterfile:
            for evt in fasterfile:
                the_type = evt.type
                the_time = evt.time
                the_data = evt.data
                n_event_read += 1
            # end for
        # end with
        end_time = time.time()
        print(f"# Elasped time: {end_time-start_time:5.3f} seconds")
        print("# Read {0} of 60211 events from the test file".format(n_event_read))
        print("#...done\n")
    elif args.action == 'more':
        # list files to browse
        if len(args.files) < 1:
            print("Need a list of faster files to read")
            sys.exit(1)
        n_display = 0
        try:
            for f in args.files:
                for e in faster.FileReader(f, args.nmax):
                    print(str(e))
                    n_display += 1
                    if n_display >= 10:
                        k = input()
                        if k == 'q':
                            sys.exit(0)
                        else:
                            n_display = 0
        except KeyboardInterrupt:
            sys.exit(1)
    elif args.action == "stats":
        # Do stats on files
        if len(args.files) < 1:
            print("Need a list of faster files to read")
            sys.exit(1)
        number_of_events = 0
        types: Dict[str, int] = {}
        labels: Dict[str, int] = {}
        types_in_groups: Dict[str, int] = {}
        labels_in_groups: Dict[str, int] = {}
        timestamps_limits = {'min': 0, 'max': -1}
        print("(")
        for f in args.files:
            for evt in faster.FileReader(f, args.nmax):
                timestamps_limits['max'] = evt.time
                if timestamps_limits['min'] == 0:
                    timestamps_limits['min'] = evt.time
                number_of_events += 1
                # compute the event type once and for all
                types[evt.type] = types.get(evt.type, 0) + 1
                labels[evt.label] = labels.get(evt.label, 0) + 1
                if evt.type == 'group':
                    for subevt in evt.data['events']:
                        types_in_groups[subevt.type] = types_in_groups.get(subevt.type, 0) + 1
                        labels_in_groups[subevt.label] = labels_in_groups.get(subevt.label, 0) + 1
                    # end for subevt
                # end for event
            print("   {")
            print(f"    'number_of_events_to_read':'{args.nmax}',")
            print(f"    'file_name':'{f}',")
            print(f"    'number_of_events': {number_of_events},")
            print(f"    'first_event_time': {timestamps_limits['min']}, 'last_event_time': {timestamps_limits['max']}")
            print("    'types': {")
            for t in sorted(types):
                print(f"        '{t}': {types[t]},")
            print('      },')
            print("    'labels': {")
            for t in sorted(labels):
                print(f"        '{t}': {labels[t]},")
            print('      },')
            print("    'in_groups': {")
            print("         'types': {")
            for t in sorted(types_in_groups):
                print(f"           '{t}': {types_in_groups[t]},")
            print('       },')
            print("         'labels': {")
            for t in sorted(labels_in_groups):
                print(f"           '{t}': {labels_in_groups[t]},")
            print('       },')
        print(")")
    else:
        print(faster.__doc__)
    # end if, else
