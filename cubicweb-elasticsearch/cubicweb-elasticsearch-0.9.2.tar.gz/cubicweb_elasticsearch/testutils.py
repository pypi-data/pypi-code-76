import unittest

try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection

from elasticsearch_dsl.connections import connections

from cubicweb.predicates import is_instance

from cubicweb_elasticsearch.entities import IFullTextIndexSerializable


class BlogEntryFTIAdapter(IFullTextIndexSerializable):
    __select__ = IFullTextIndexSerializable.__select__ & is_instance("BlogEntry")
    custom_indexable_attributes = ("title", "content")


class BlogFTIAdapter(IFullTextIndexSerializable):
    __select__ = IFullTextIndexSerializable.__select__ & is_instance("Blog")
    custom_indexable_attributes = ("title",)


class PersonFTIAdapter(IFullTextIndexSerializable):
    __select__ = IFullTextIndexSerializable.__select__ & is_instance("Person")

    @property
    def es_id(self):
        return self.entity.age


class RealESTestMixin(object):
    @classmethod
    def setUpClass(cls):
        try:
            HTTPConnection("localhost:9200").request("GET", "/")
        except:  # noqa
            raise unittest.SkipTest("No ElasticSearch on localhost, skipping test")
        super(RealESTestMixin, cls).setUpClass()

    def setup_database(self):
        super(RealESTestMixin, self).setup_database()
        self.config.global_set_option(
            "elasticsearch-locations", "http://localhost:9200"
        )
        self.config.global_set_option("index-name", "unittest_index_name")

    def tearDown(self):
        try:
            with self.admin_access.cnx() as cnx:
                indexer = cnx.vreg["es"].select("indexer", cnx)
                es = indexer.get_connection()
                es.indices.delete(self.config["index-name"])
        finally:
            # remove default connection if there's one
            try:
                connections.remove_connection("default")
            except KeyError:
                pass
            super(RealESTestMixin, self).tearDown()
