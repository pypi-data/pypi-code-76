import unittest

from mock import patch

from cubicweb.devtools import testlib
from cubicweb.cwconfig import CubicWebConfiguration

from cubicweb_elasticsearch.testutils import (
    BlogFTIAdapter,
    BlogEntryFTIAdapter,
    PersonFTIAdapter,
)


class IFullTextIndexSerializableTC(testlib.CubicWebTC):
    def setup_database(self):
        super(IFullTextIndexSerializableTC, self).setup_database()
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
    def test_index_entity(self, index, exists, create):
        """Only update indexable attributes while call entity.complete()
        on IFullTextIndexSerializable.serialze()
        """
        with self.admin_access.repo_cnx() as cnx:
            with self.temporary_appobjects(BlogFTIAdapter, BlogEntryFTIAdapter):
                blog = cnx.create_entity("Blog", title=u"Blog")
                cnx.commit()
                self.assertTrue(index.called)
                args, kwargs = index.call_args
                # blog title is a in custom_indexable_attributes
                self.assertEqual(kwargs["doc_type"], "_doc")
                self.assertEqual(kwargs["body"]["cw_etype"], "Blog")
                self.assertEqual(kwargs["body"]["title"], u"Blog")
                index.reset_mock()
                # create a BlogEntry
                bentry = cnx.create_entity(
                    "BlogEntry",
                    title=u"program",
                    content=u"Le nouveau programme",
                    entry_of=blog,
                )
                cnx.commit()
                self.assertEqual(index.call_count, 2)
                for args, kwargs in index.call_args_list:
                    if kwargs["doc_type"] == "_doc":
                        break
                else:
                    self.fail("index not called for the BlogEntry")
                for arg_name, expected_value in (
                    ("content", u"Le nouveau programme"),
                    ("cwuri", bentry.cwuri),
                    ("title", "program"),
                ):
                    self.assertEqual(kwargs["body"][arg_name], expected_value)
                self.assertFalse("content_format" in kwargs["body"])
                # update BlogEntry
                bentry.cw_set(title=u"Programme")
                index.reset_mock()
                cnx.commit()
                self.assertTrue(index.called)
                args, kwargs = index.call_args
                for arg_name, expected_value in (
                    ("id", bentry.eid),
                    ("doc_type", "_doc"),
                ):
                    self.assertEqual(kwargs[arg_name], expected_value)
                for arg_name, expected_value in (
                    ("content", u"Le nouveau programme"),
                    ("cwuri", bentry.cwuri),
                    ("title", u"Programme"),
                ):
                    self.assertEqual(kwargs["body"][arg_name], expected_value)
                self.assertFalse("content_format" in kwargs["body"])

    @patch("elasticsearch.client.indices.IndicesClient.create")
    @patch("elasticsearch.client.indices.IndicesClient.exists")
    @patch("elasticsearch.client.Elasticsearch.index")
    def test_custom_es_id_attr(self, create, exists, index):
        """check custom es_eid_attr is used in es document"""
        with self.admin_access.repo_cnx() as cnx:
            with self.temporary_appobjects(PersonFTIAdapter):
                cnx.create_entity("Person", age=123456, name=u"Jean")
                cnx.commit()
                indexer = cnx.vreg["es"].select("indexer", cnx)
                es = indexer.get_connection()
                self.assertTrue(es.index.called)
                args, kwargs = es.index.call_args
                # make sure age was used as custom es document id
                self.assertEqual(kwargs["id"], 123456)


class SerializationTests(testlib.CubicWebTC):
    def test_person_serialization(self):
        with self.admin_access.cnx() as cnx:
            jean = cnx.create_entity("Person", age=12, name=u"Jean")
            serializer = jean.cw_adapt_to("IFullTextIndexSerializable")
            self.assertEqual(
                serializer.serialize(),
                {
                    "name": u"Jean",
                    "age": 12,
                    "cw_etype": u"Person",
                    "eid": jean.eid,
                    "cwuri": jean.cwuri,
                    "creation_date": jean.creation_date,
                    "modification_date": jean.modification_date,
                },
            )


if __name__ == "__main__":
    unittest.main()
