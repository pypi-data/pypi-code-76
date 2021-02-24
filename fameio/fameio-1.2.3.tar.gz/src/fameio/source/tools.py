# !/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse

import logging as log


LOG_LEVELS = {'critical': log.CRITICAL,
              'error': log.ERROR,
              'warn': log.WARNING,
              'warning': log.WARNING,
              'info': log.INFO,
              'debug': log.DEBUG,
              }


def log_and_raise(message):
    """ Raises a critical error and logs with given `error_message` """
    log.critical(message)
    raise Exception(message)


def set_up_logger(level, file_name):
    """Sets up logger which always writes to the console and if provided also to `file_name`"""
    log_formatter = log.Formatter("%(asctime)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    root_logger = log.getLogger()
    root_logger.setLevel(level)

    if file_name:
        file_handler = log.FileHandler(file_name, mode="w")
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

    console_handler = log.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


def arg_handling_make_config(defaults):
    """Handles command line arguments and returns `input_file` and `run_config` for make_config routine"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        required=True,
                        help=("Provide path to configuration file"
                              "Example: -f <path/to/configuration/file.yaml>'"),
                        )

    add_loglevel_argument(parser, defaults["log_level"], LOG_LEVELS)
    add_output_argument(parser, defaults["output_file"])
    add_logfile_argument(parser)

    args = parser.parse_args()

    input_file = args.file
    level = LOG_LEVELS.get(args.log.lower())
    output_file = args.output
    log_file = args.logfile

    run_config = {"log_level": level,
                  "output_file": output_file,
                  "log_file": log_file,
                  }

    return input_file, run_config


def arg_handling_convert_results(defaults):
    """Handles command line arguments and returns `input_file` and `run_config` for convert_results routine"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        required=True,
                        help=("Provide path to protobuf file"
                              "Example: -f <path/to/result/file.pb>'"),
                        )

    add_loglevel_argument(parser, defaults["log_level"], LOG_LEVELS)
    add_logfile_argument(parser)
    add_select_agents_argument(parser)

    args = parser.parse_args()

    input_file = args.file
    level = LOG_LEVELS.get(args.log.lower())
    log_file = args.logfile
    agents_to_extract = args.agents

    run_config = {"log_level": level,
                  "log_file": log_file,
                  "agents_to_extract": agents_to_extract,
                  }

    return input_file, run_config


def add_select_agents_argument(parser):
    """Adds argument handling for selecting agent types which get converted"""
    parser.add_argument("-a",
                        "--agents",
                        nargs="*",
                        type=str,
                        help=("Provide list of agents to extract. "
                              "Example --agents MyAgent1 MyAgent2 default='None'"),
                        )


def add_logfile_argument(parser):
    """Adds argument handling for setting the logfile"""
    parser.add_argument("-lf",
                        "--logfile",
                        help=("Provide logging file. "
                              "Example --logfile <path/to/log/file.log>', default='None'"),
                        )


def add_output_argument(parser, defaults):
    """Adds argument handling for setting the outputfile"""
    parser.add_argument("-o",
                        "--output",
                        default=defaults,
                        help=("Provide path to config.pb file. "
                              "Example --output <path/to/config.pb>', default='config.pb'"),
                        )


def add_loglevel_argument(parser, defaults, levels):
    """Adds argument handling for setting the log_level"""
    parser.add_argument("-l",
                        "--log",
                        default=defaults,
                        choices=list(levels.keys()),
                        help=("Provide logging level. "
                              "Example --log debug', default='info'"),
                        )


def get_valid_key(key, valid_keys):
    """Returns an entry from given `valid_keys` with an case insensitive match of `key`"""
    for valid_key in valid_keys:
        if key.lower() == valid_key.lower():
            return valid_key
    log_and_raise("Key `{}` not in list of valid keys `{}`.".format(key, valid_keys))
