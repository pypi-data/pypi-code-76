# -*- coding: utf-8 -*-

from .factory.factory_converter import create

import logging

logger = logging.getLogger(__name__)


def run(file_destination, corpus_dir, file_name, corpus_url, download_time):
    converters = create(file_destination)
    if len(converters) == 1:
        converters[0]['convert'].convert(file_destination, corpus_dir, file_name, corpus_url, download_time)
    elif len(converters) > 1:
        for number, converter in enumerate(converters, start=1):
            print(f"{converter['description']}")
        print('Use only one type of json files in a directory. Corpus not generated!')
    else:
        print('No valid json format found in this directory. Corpus not generated!')
