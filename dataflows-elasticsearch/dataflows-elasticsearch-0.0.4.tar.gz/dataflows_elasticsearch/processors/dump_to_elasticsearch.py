import datetime
import decimal
import os

import logging
from elasticsearch import Elasticsearch
from tableschema_elasticsearch import Storage

from dataflows.processors.dumpers.dumper_base import DumperBase
from dataflows import ResourceWrapper


class ESDumper(DumperBase):

    def __init__(self, *, indexes,
                 mapper_cls=None,
                 index_settings=None,
                 engine='env://DATAFLOWS_ELASTICSEARCH',
                 reindex=False,
                 options={},
                 elasticsearch_options={}):
        super(ESDumper, self).__init__(options=options)
        self.index_to_resource = indexes
        self.mapper_cls = mapper_cls
        self.index_settings = index_settings
        self.connection_info = engine
        self.reindex = reindex
        self.converted_resources = {}
        self.elasticsearch_options = elasticsearch_options

    def initialize(self):
        super(ESDumper, self).initialize()
        if isinstance(self.connection_info, str):
            if self.connection_info.startswith('env://'):
                env_var = self.connection_info[6:]
                self.connection_info = os.environ.get(env_var)
                assert self.connection_info is not None, \
                    "Couldn't connect to ES Instance - " \
                    "Please set your '%s' environment variable" % env_var
            self.engine = Elasticsearch(hosts=[self.connection_info], **self.elasticsearch_options)
        else:
            assert isinstance(self.connection_info, Elasticsearch)
            self.engine = self.connection_info
        try:
            if not self.engine.ping():
                logging.exception('Failed to connect to database %s', self.engine)
        except Exception:
            logging.exception('Failed to connect to database %s', self.engine)
            raise

        self.converted_resources = {}
        for k, v in self.index_to_resource.items():
            for w in v:
                w['index_name'] = k
                self.converted_resources[w.get('resource-name', w.get('resource_name'))] = w

    def process_resource(self, resource: ResourceWrapper):
        res = resource.res
        resource_name = res.name
        if resource_name not in self.converted_resources:
            return resource
        else:
            primary_key = res.schema.primary_key
            converted_resource = self.converted_resources[resource_name]
            index_name = converted_resource['index_name']
            doc_type = converted_resource.get('doc-type', converted_resource.get('doc_type'))
            storage = Storage(self.engine)
            logging.info('Writing to ES %s -> %s/%s (reindex: %s)',
                         resource_name, index_name, doc_type, self.reindex)
            storage.create(index_name, [(doc_type, res.descriptor['schema'])],
                           always_recreate=False, reindex=self.reindex,
                           mapping_generator_cls=self.mapper_cls,
                           index_settings=self.index_settings)

            return storage.write(index_name, doc_type, self.normalizer(resource),
                                 primary_key, as_generator=True)

    def normalizer(self, resource: ResourceWrapper):
        for row in resource:
            yield self.normalize(row, resource)

    def normalize(self, row, resource: ResourceWrapper = None):
        if isinstance(row, dict):
            return dict(
                (k, self.normalize(v))
                for k, v in row.items()
            )
        elif isinstance(row, (str, int, float, bool, datetime.date)):
            return row
        elif isinstance(row, decimal.Decimal):
            return float(row)
        elif isinstance(row, (list, set)):
            return [self.normalize(x) for x in row]
        elif row is None:
            return None
        assert False, "Don't know how to handle row (%s) %r" % (type(row), row)
