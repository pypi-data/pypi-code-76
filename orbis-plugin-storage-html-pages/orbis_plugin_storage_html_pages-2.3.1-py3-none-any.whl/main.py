# -*- coding: utf-8 -*-

from orbis_eval.core import app
from orbis_eval.libs import files
from .build_html import build as build_html

from .libs import sort_queue
from .libs import get_colors
from .libs import get_values
from .libs import get_annotation_colors

import os

import logging

logger = logging.getLogger(__name__)


class Main(object):

    def __init__(self, rucksack):

        super(Main, self).__init__()
        self.rucksack = rucksack
        self.config = self.rucksack.open['config']
        self.data = self.rucksack.open['data']
        self.pass_name = self.rucksack.open['config']['file_name'].split(".")[0]
        self.folder = os.path.join(app.paths.output_path, "html_pages", self.pass_name)
        self.queue = sort_queue(self.rucksack.get_keys())

    def run(self):
        self.build(self.folder, self.queue, self.rucksack, self.config)

    def build(self, folder, queue, rucksack, config):

        logger.info("Building HTML pages")

        timestamp = files.get_timestamp()
        folder_dir = os.path.join(folder + f"-{timestamp}")
        files.create_folder(folder_dir)
        pages = {}

        for item_key in queue:
            logger.info(f"Building Page: {item_key}")
            item = rucksack.itemview(item_key)

            try:
                next_item = queue[queue.index(item_key) + 1]
            except IndexError:
                next_item = None

            try:
                previous_item = queue[queue.index(item_key) - 1]
            except IndexError:
                previous_item = None

            previous_item = previous_item if previous_item != item_key else None

            key = item['index']
            sf_colors = get_colors(get_values(item, "key"))
            type_colors = get_colors(get_values(item, "entity_type"))
            annotations_colors = get_annotation_colors(item["gold"], item["computed"])
            html, html_blocks = build_html(config, rucksack, item, next_item, previous_item, sf_colors, type_colors,
                                           annotations_colors)

            pages[key] = html_blocks

            file_dir = os.path.join(folder_dir, str(key) + ".html")
            logger.debug(file_dir)

            with open(file_dir, "w") as open_file:
                open_file.write(html)

        logger.info("Finished building HTML pages")
        return pages
