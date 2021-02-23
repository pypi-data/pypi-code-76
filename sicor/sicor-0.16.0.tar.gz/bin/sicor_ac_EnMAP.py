#!/usr/bin/env python
"""Command line program to run sicor for EnMAP Level-1B products."""

import argparse
import pprint
import sys
import dill

from enpt.io.reader import L1B_Reader
from enpt.options.config import EnPTConfig, config_for_testing_dlr

from sicor import __version__
from sicor.options import get_options
from sicor.sicor_enmap import *


def sicor_ac_enmap_parser():
    """Return argument parser for sicor EnMAP."""

    parser = argparse.ArgumentParser(
        prog='sicor_ac_EnMAP.py',
        description='=' * 70 + '\n' + 'SICOR EnMAP console argument parser. ',
        epilog="use '>>> sicor_ac_EnMAP.py -h' for detailed documentation and usage hints.")

    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument("-in", "--input", action="store", required=True, type=str,
                        help="Path to EnMAP Level-1B product (root dir).")
    parser.add_argument("-set", "--settings", action="store", required=True, type=str,
                        help="Path to retrieval options json file. ")
    parser.add_argument("-out", "--output", action="store", required=True, type=str,
                        help="Path to output directory (will be created if nonexistent).")
    parser.add_argument("-un", "--unknowns", action="store", required=False, type=str,
                        help="True, if uncertainties due to unknown forward model parameters should be added to "
                             "S_epsilon; default: False")

    return parser


if __name__ == "__main__":
    args = sicor_ac_enmap_parser().parse_args()
    logger = logging.Logger("EnMAP")
    fmt_suffix = None
    formatter_ConsoleH = logging.Formatter('%(asctime)s' + (' [%s]' % fmt_suffix if fmt_suffix else '') +
                                           ':   %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    consoleHandler_out = logging.StreamHandler(stream=sys.stdout)
    consoleHandler_out.setFormatter(formatter_ConsoleH)
    logger.addHandler(consoleHandler_out)

    logger.info("Sicor AC for EnMAP started.")
    logger.info("Input = %s" % args.input)
    logger.info("Output = %s" % args.output)
    logger.info("Settings = %s" % args.settings)
    logger.info("Unknowns = %s" % args.unknowns)

    options = get_options(args.settings, validation=False)
    logger.info("Loading settings: \n" + pprint.pformat(options))

    # Read EnMAP Level-1B Product from file system
    logger.info("Reading EnMAP Level-1B Product from file system...")
    config = EnPTConfig(**config_for_testing_dlr)
    RD = L1B_Reader(config=config)
    L1_obj = RD.read_inputdata(args.input, compute_snr=False)
    L1_obj.get_preprocessed_dem()
    enmap_l1b = L1_obj

    logger.info("Performing atmospheric correction...")
    enmap_l2a_vnir, enmap_l2a_swir, res = sicor_ac_enmap(enmap_l1b, options, unknowns=args.unknowns, logger=logger)

    logger.info("Writing products to output path...")
    with open(args.output, "wb") as fl:
        dill.dump([enmap_l2a_vnir, enmap_l2a_swir, res], fl)

    logger.info("EEooFF")
