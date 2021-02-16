import unittest

from mock import patch

from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_elasticsearch.es import indexable_entities


class UtilTestCase(CubicWebTC):
    @patch("cubicweb.server.session.Connection.drop_entity_cache")
    def test_indexable_entities(self, drop):
        """check indexable_entities yield entities as expected"""
        with self.admin_access.cnx() as cnx:
            print(type(cnx))
            p1 = cnx.create_entity("Person", name=u"p1")
            p2 = cnx.create_entity("Person", name=u"p3")
            p3 = cnx.create_entity("Person", name=u"p3")
            drop.reset_mock()
            self.assertEqual(
                [p.eid for p in indexable_entities(cnx, "Person")],
                [p1.eid, p2.eid, p3.eid],
            )
            self.assertEqual(drop.call_count, 1)
            drop.reset_mock()
            # now try again with chunksize=2 to make sure we have split
            # rset in 2
            self.assertEqual(
                [p.eid for p in indexable_entities(cnx, "Person", chunksize=2)],
                [p1.eid, p2.eid, p3.eid],
            )
            self.assertEqual(drop.call_count, 2)


if __name__ == "__main__":
    unittest.main()
