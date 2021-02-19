# -*- coding: utf-8 -*-

import os
import requests

from orbis_eval.core import app
from orbis_eval.plugins.aggregation.dbpedia_entity_types import Main as dbpedia_entity_types
from orbis_eval.core.base import AggregationBaseClass


import logging
logger = logging.getLogger("Babelfly")


class Main(AggregationBaseClass):

    def environment(self):
        keys = {
            'BABELFLY_API_KEY': "",
            'BABELFLY_SERVICE_URL': ""
        }
        return keys

    def query(self, item):
        # service_url = 'https://babelfy.io/v1/disambiguate'
        service_url = self.environment_variables['BABELFLY_SERVICE_URL'] or 'https://babelfy.io/v1/disambiguate'
        key = self.environment_variables['BABELFLY_API_KEY']
        annotation_type = 'NAMED_ENTITIES'

        data = {
            'text': item['corpus'],
            'annType': annotation_type,
            'key': key
        }

        try:
            response = requests.post(service_url, data=data).json()
            logger.debug(f"Babelfly response: {response}")
        except Exception as exception:
            logger.error(f"Query failed: {exception}")
            response = None
        return response

    def map_entities(self, response, item):

        if not response:
            return None

        corpus = item['corpus']
        file_entities = []
        for item in response:
            # logger.warning(f"47: {item}")
            item["key"] = item["DBpediaURL"]
            item["entity_type"] = dbpedia_entity_types.get_dbpedia_type(item["key"])
            item["entity_type"] = dbpedia_entity_types.normalize_entity_type(item["entity_type"])
            item["document_start"] = int(item["charFragment"]["start"])
            item["document_end"] = int(item["charFragment"]["end"] + 1)
            item["surfaceForm"] = corpus[item["document_start"]:item["document_end"]]
            file_entities.append(item)
        return file_entities

if __name__ == '__main__':
    key = os.environ['BABELFLY_API_KEY']
