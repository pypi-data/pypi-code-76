# -*- coding: utf-8 -*-
import os
from io import open
import click
import yaml
import logging

from fastutils import logutils

from .login import LogInput
from .logfilter import LogFilter
from .logout import LogOutput
from .logparser import LogParser

DEFAULT_LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s\t%(process)d\t%(thread)d\t%(levelname)s\t%(pathname)s\t%(lineno)d\t%(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        },
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": "server.log",
            "maxBytes": 1024*1024*128,
            "backupCount": 36,
            "encoding": "utf-8",
        }
    },
    "loggers": {
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "logfile"],
        "propagate": True,
    }
}

logger = logging.getLogger(__name__)

def deep_merge(data1, data2):
    for key2, value2 in data2.items():
        value1 = data1.get(key2, None)
        if isinstance(value1, dict) and isinstance(value2, dict):
            deep_merge(value1, value2)
        else:
            data1[key2] = value2
        

def load_input(settings):
    input_settings = settings.get("input", {}) or {}
    try:
        input_object = LogInput.init(input_settings)
        if not input_object:
            logger.error(u"Error: input data type error.")
            os.sys.exit(1)
        return input_object
    except RuntimeError as err:
        logger.error(u"Error: init input failed, message={message}.".format(message=str(err)))
        os.sys.exit(2)

def load_output(settings):
    output_setting = settings.get("output", {}) or {}
    try:
        output = LogOutput.init(output_setting)
        return output
    except Exception as err:
        logger.error("Error: init output failed, message={message}.".format(message=str(err)))
        os.sys.exit(2)

def load_parser(settings):
    parser_setting = settings.get("parser", {}) or {}
    if not parser_setting:
        return None
    try:
        parser = LogParser.init(parser_setting)
        return parser
    except Exception as err:
        logger.error("Error: init parser failed, message={message}.".format(message=str(err)))
        os.sys.exit(1)

def load_filters(settings):
    filters = []
    filters_setting = settings.get("filters", []) or []
    if filters_setting:
        for filter_setting in filters_setting:
            try:
                filter = LogFilter.init(filter_setting)
                if not filter:
                    logger.error("Error: filter config error.")
                filters.append(filter)
            except RuntimeError as error:
                logger.error("Error: init filter failed, message={message}。".format(message=str(error)))
                os.sys.exit(1)
    return filters

@click.group()
@click.option("-c", "--config", required=True, help=u"Config file path. The config file must in yaml format.")
@click.pass_context
def main(ctx, config):
    """Parse log file as input and export the data to database as output.
    """
    # read settings from config file
    with open(config, "r", encoding="utf-8") as fobj:
        settings = yaml.safe_load(fobj)
    if not settings:
        settings = {}
    
    # setup logging
    logutils.setup(**settings)

    # other settings
    ctx.ensure_object(dict)
    ctx.obj["config"] = config
    ctx.obj["settings"] = settings

@main.command()
@click.pass_context
def server(ctx):
    """Start log handler server.
    """
    settings = ctx.obj["settings"]
    input = load_input(settings)
    output_object = load_output(settings)
    parser = load_parser(settings)
    filters = load_filters(settings)
    input.set_handler(output_object, filters=filters, parser=parser)
    input.loop()

@main.command()
@click.argument("text", nargs=1, required=True)
@click.pass_context
def test(ctx, text):
    """Parse the example text and print out parse result.
    """
    settings = ctx.obj["settings"]
    parser = load_parser(settings)
    if parser:
        info = parser.line_handler(text, keep_not_matched_lines=False)
        text = yaml.dump(info, allow_unicode=True)
        print(text)
    else:
        print("No parser configed...")

@main.command()
@click.option("-i", "--include-blank-lines", is_flag=True, help="Parse empty lines or not. Default to NO parse.")
@click.option("-e", "--encoding", default="utf-8", help="Encoding of the input. Default to UTF-8.")
@click.argument("filename", nargs=1, required=False)
@click.pass_context
def scan(ctx, include_blank_lines, encoding, filename):
    """Try example settings on a test file.
    """
    settings = ctx.obj["settings"]
    scan_input_settings = {
        "type": "file",
        "ignore-blank-lines": not include_blank_lines,
        "filename": filename,
        "encoding": encoding,
    }
    settings["input"] = scan_input_settings
    input_object = load_input(settings)
    output = load_output(settings)
    parser = load_parser(settings)
    filters = load_filters(settings)
    input_object.set_handler(output, filters=filters, parser=parser)
    input_object.loop()

if __name__ == "__main__":
    main()
