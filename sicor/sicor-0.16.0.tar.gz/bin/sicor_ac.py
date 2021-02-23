#!/usr/bin/env python

from sicor import ac, __version__
from sicor.tables import get_tables
import argparse


def sicor_ac_parser():
    """Return parser for sicor_ac.py program."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-g", "--granule_path", action="store", type=str, required=False, default=None,
                        help="Path to S2 granule product folder.")
    parser.add_argument("-o", "--out_dir", action="store", type=str, required=False, default=None,
                        help="Path to output directory.")
    parser.add_argument("-l", "--log_dir", action="store", type=str, required=False, default=None,
                        help="Path to directory where log can be written.")
    parser.add_argument("-s", "--settings", action="store", type=str, required=False, default=None,
                        help="Path to settings json file.")

    parser.add_argument("-e", "--export_options_to", action="store", required=False, default=None, type=str,
                        help="Export options json file to given path. Other options are ignored.")
    parser.add_argument("-v", "--version", action="store_true", required=False, default=False,
                        help="Print version.")

    return parser


if __name__ == "__main__":

    parser = sicor_ac_parser()
    args = parser.parse_args()

    if args.export_options_to is not None:
        print("Download or find needed tables for atmospheric correction.")
        get_tables(
            sicor_table_path=None,
            export_options_to=args.export_options_to
        )
        print("Please check options and set the at least the following to your liking:")
        print('    ["ECMWF"/"path_db"] path to your ECMWF database.')
        print('    ["RTFO"/[type]/"atm_tables_fn"] path to your ac tables, these might already be ok.')
        print('    ["uncertainties"/"snr_model"] path to your snr model, included in sicor repository.')
        print('Done.')

    elif args.version is True:
        print("SICOR version: %s" % str(__version__))
    else:
        if None in [args.granule_path, args.out_dir, args.log_dir, args.settings]:
            parser.error("All ac related options need to be set: -g -o -l -s.")
        else:
            ac(granule_path=args.granule_path,
               settings=args.settings,
               logdir=args.log_dir,
               coregistration=None,
               out_dir=args.out_dir)
