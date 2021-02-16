from __future__ import print_function

import sys
import unittest
from io import StringIO

from mock import patch

from elasticsearch_dsl.faceted_search import FacetedResponse
from elasticsearch_dsl.search import Search

from cubicweb.devtools import testlib
from cubicweb.cwconfig import CubicWebConfiguration
from cubicweb_elasticsearch import ccplugin
from cubicweb_elasticsearch.es import indexable_types, fulltext_indexable_rql


# TODO - find a way to configure ElasticSearch as non threaded while running tests
# so that the traces show the full stack, not just starting from connection.http_*
class ExportElasticSearchTC(testlib.AutoPopulateTest):
    # ignore ComputedRelations
    ignored_relations = set(
        (
            "narrower_concept",
            "hidden_label",
            "preferred_label",
            "alternative_label",
        )
    )

    def setup_database(self):
        super(ExportElasticSearchTC, self).setup_database()
        self.orig_config_for = CubicWebConfiguration.config_for
        config_for = lambda appid, *args, **kwargs: self.config  # noqa
        CubicWebConfiguration.config_for = staticmethod(config_for)
        self.config[
            "elasticsearch-locations"
        ] = "http://nonexistant.elastic.search:9200"
        self.config["index-name"] = "unittest_index_name"
        self.tested_etype = "Person"

    def to_test_etypes(self):
        with self.admin_access.repo_cnx() as cnx:
            types = indexable_types(cnx.repo)
        return types

    def tearDown(self):
        CubicWebConfiguration.config_for = self.orig_config_for
        super(ExportElasticSearchTC, self).tearDown()

    def test_indexable_types(self):
        with self.admin_access.repo_cnx() as cnx:
            self.assertIn(self.tested_etype, self.to_test_etypes())
            self.assertIn(self.tested_etype, indexable_types(cnx.vreg.schema))

    @patch("elasticsearch.client.Elasticsearch.index", unsafe=True)
    @patch("elasticsearch.client.Elasticsearch.bulk", unsafe=True)
    @patch("elasticsearch.client.indices.IndicesClient.exists", unsafe=True)
    @patch("elasticsearch.client.indices.IndicesClient.create", unsafe=True)
    def test_ccplugin(self, create, exists, bulk, index):
        # TODO disable hook!!! then remove index mock
        with self.admin_access.repo_cnx() as cnx:
            with cnx.allow_all_hooks_but("es"):
                self.auto_populate(10)
        bulk.reset_mock()
        cmd = [self.appid, "--dry-run"]
        sys.stdout = out = StringIO()
        try:
            ccplugin.IndexInES(None).main_run(cmd)
        finally:
            sys.stdout = sys.__stdout__
        self.assertEqual("", out.getvalue())
        create.assert_not_called()
        bulk.assert_not_called()

        # TODO try wrong option
        # cmd = [self.appid, '--wrong-option', 'yes']

        cmd = [self.appid]
        sys.stdout = StringIO()
        try:
            ccplugin.IndexInES(None).main_run(cmd)
        finally:
            sys.stdout = sys.__stdout__
        with self.admin_access.repo_cnx() as cnx:
            self.assertTrue(
                cnx.execute("Any X WHERE X is %(etype)s" % {"etype": self.tested_etype})
            )
        # TODO - put this somewhere where it tests on the first get_connection
        # create.assert_called_with(ignore=400,
        #                          index='unittest_index_name',
        #                          body=INDEX_SETTINGS)
        bulk.assert_called()
        # TODO ? check called data

    @patch("elasticsearch.client.indices.IndicesClient.create", unsafe=True)
    @patch("elasticsearch.client.indices.IndicesClient.exists", unsafe=True)
    @patch("elasticsearch.client.Elasticsearch.index", unsafe=True)
    def test_es_hooks_create(self, index, exists, create):
        with self.admin_access.cnx() as cnx:
            cnx.create_entity(self.tested_etype, name=u"Jean Valjean", age=14)
            cnx.commit()
            index.assert_called()

    @patch("elasticsearch.client.indices.IndicesClient.create", unsafe=True)
    @patch("elasticsearch.client.indices.IndicesClient.exists", unsafe=True)
    @patch("elasticsearch.client.Elasticsearch.index", unsafe=True)
    def test_es_hooks_modify(self, index, exists, create):
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity(self.tested_etype, name=u"Jean Valjean")
            cnx.commit()
            index.reset_mock()
            entity.cw_set(name=u"Victor Hugo")
            cnx.commit()
            index.assert_called()


def mock_execute_150(*args, **kwargs):
    return mock_execute(100)


def mock_execute_15(*args, **kwargs):
    return mock_execute(15)


def mock_execute_1(*args, **kwargs):
    return mock_execute(1)


def mock_execute(count):
    def _result(i):
        return {
            "_source": {
                "cwuri": "http://example.org/{}".format(i),
                "eid": i,
                "cw_etype": "Person",
                "name": "Jean Valjean",
            },
            "_type": "Person",
            "_score": 1,
        }

    search = Search(doc_type="_doc", index="unittest_index_name")
    return FacetedResponse(
        search,
        {
            "hits": {
                "hits": [_result(i) for i in range(count)],
                "total": {"value": count, "relation": "eq"},
            }
        },
    )


def mock_cnx(*args, **kwargs):
    return True


class ElasticSearchViewsTC(testlib.CubicWebTC):

    # TODO generate X tests ranging the number of results from 1 to 150
    @patch("elasticsearch_dsl.search.Search.execute", new=mock_execute_1)
    @patch("elasticsearch_dsl.connections.connections.get_connection", new=mock_cnx)
    def test_search_view_1(self):
        with self.new_access("anon").web_request() as req:
            # self._cw.form.get('search'))
            self.view("esearch", req=req, template=None)

    @patch("elasticsearch_dsl.search.Search.execute", new=mock_execute_15)
    @patch("elasticsearch_dsl.connections.connections.get_connection", new=mock_cnx)
    def test_search_view_15(self):
        with self.new_access("anon").web_request() as req:
            # self._cw.form.get('search'))
            self.view("esearch", req=req, template=None)

    @patch("elasticsearch_dsl.search.Search.execute", new=mock_execute_150)
    @patch("elasticsearch_dsl.connections.connections.get_connection", new=mock_cnx)
    def skip_test_search_view_150(self):
        with self.new_access("anon").web_request() as req:
            # self._cw.form.get('search'))
            self.view("esearch", req=req, template=None)


class ElasticsearchTC(testlib.CubicWebTC):
    def test_1(self):
        with self.admin_access.cnx() as cnx:
            etype = "Person"
            rql = fulltext_indexable_rql(etype, cnx)
            self.assertIn("age", rql)
            self.assertNotIn("eid", rql)
            self.assertEqual(rql.count("modification_date"), 1)


if __name__ == "__main__":
    unittest.main()
