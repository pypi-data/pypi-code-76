# !/usr/bin/env python
# -*- coding:utf-8 -*-


from fameio.scripts.make_config import run as make_config
from fameio.scripts.make_config import DEFAULT_CONFIG as defaults_make_config
from fameio.scripts.convert_results import run as convert_results
from fameio.scripts.convert_results import DEFAULT_CONFIG as defaults_convert_results
from fameio.source.tools import arg_handling_make_config, arg_handling_convert_results


def makeFameRunConfig():
	input_file, run_config = arg_handling_make_config(defaults_make_config)
	make_config(input_file, run_config)


def convertFameResults():
	input_file, run_config = arg_handling_convert_results(defaults_convert_results)
	convert_results(input_file, run_config)
