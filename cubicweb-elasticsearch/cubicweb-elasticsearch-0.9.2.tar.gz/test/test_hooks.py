import unittest

from mock import patch

from cubicweb.devtools import testlib
from cubicweb.cwconfig import CubicWebConfiguration


class IndexHookTC(testlib.CubicWebTC):
    def setup_database(self):
        super(IndexHookTC, self).setup_database()
        self.orig_config_for = CubicWebConfiguration.config_for

        def config_for(appid):
            return self.config  # noqa

        CubicWebConfiguration.config_for = staticmethod(config_for)
        self.config[
            "elasticsearch-locations"
        ] = "http://nonexistant.elastic.search:9200"
        self.config["index-name"] = "unittest_index_name"

    @patch("elasticsearch.client.indices.IndicesClient.create")
    @patch("elasticsearch.client.indices.IndicesClient.exists")
    @patch("elasticsearch.client.Elasticsearch.index")
    def test_index_after_create_entity(self, create, exists, index):
        with self.admin_access.cnx() as cnx:
            indexer = cnx.vreg["es"].select("indexer", cnx)
            ce = cnx.create_entity
            p = ce("Person", age=12, name=u"Jean")
            cnx.commit()
            es = indexer.get_connection()
            self.assertTrue(es.index.called)
            args, kwargs = es.index.call_args
            for arg_name, expected_value in (("id", p.eid), ("doc_type", "_doc")):
                self.assertEqual(kwargs[arg_name], expected_value)


if __name__ == "__main__":
    unittest.main()
