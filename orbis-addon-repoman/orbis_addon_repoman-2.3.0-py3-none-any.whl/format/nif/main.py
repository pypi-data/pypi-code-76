# -*- coding: utf-8 -*-

from . import convert

import logging
logger = logging.getLogger(__name__)


def run(file_destination, corpus_dir, file_name, corpus_url, download_time):

    if file_name.endswith("ttl"):
        convert.Convert().convert(file_destination, corpus_dir, file_name, corpus_url, download_time)
    else:
        convert.Convert().convert(file_destination, corpus_dir, file_name, corpus_url, download_time)
