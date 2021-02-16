import unittest

from logilab.common.registry import yes

from cubicweb.devtools import testlib

from cubicweb_elasticsearch.entities import ESTransactionQueue


class MockQueue(ESTransactionQueue):
    __select__ = yes(10)
    es_operations = []

    def process_operation(self, es_operation):
        self.es_operations.append(
            (
                es_operation["op_type"],
                es_operation["entity"].cw_etype,
                es_operation["entity"].eid,
            )
        )

    def process_operations(self, es_operations):
        MockQueue.es_operations = []
        super(MockQueue, self).process_operations(es_operations)


class IndexHookTC(testlib.CubicWebTC):
    def test_esqueue_index(self):
        """ensure queue gets filled with "index" operations"""
        with self.admin_access.cnx() as cnx:
            with self.temporary_appobjects(MockQueue):
                ce = cnx.create_entity
                p = ce("Person", age=12, name=u"Jean")
                cnx.commit()
            self.assertEqual(
                MockQueue.es_operations,
                [
                    ("index", "Person", p.eid),
                ],
            )

    def test_esqueue_index_multiple(self):
        """ensure queue gets filled with "index" operations"""
        with self.admin_access.cnx() as cnx:
            with self.temporary_appobjects(MockQueue):
                ce = cnx.create_entity
                p = ce("Person", age=12, name=u"Jean")
                p2 = ce("Person", age=13, name=u"Jeanne")
                cnx.commit()
            self.assertCountEqual(
                MockQueue.es_operations,
                [
                    ("index", "Person", p.eid),
                    ("index", "Person", p2.eid),
                ],
            )

    def test_esqueue_delete(self):
        """ensure queue gets filled with "index" operations"""
        with self.temporary_appobjects(MockQueue):
            with self.admin_access.cnx() as cnx:
                ce = cnx.create_entity
                p = ce("Person", age=12, name=u"Jean")
                p2 = ce("Person", age=13, name=u"Jeanne")
                cnx.commit()
            with self.admin_access.cnx() as cnx:
                cnx.execute("DELETE Person P")
                cnx.commit()
            self.assertCountEqual(
                MockQueue.es_operations,
                [
                    ("delete", "Person", p.eid),
                    ("delete", "Person", p2.eid),
                ],
            )


if __name__ == "__main__":
    unittest.main()
