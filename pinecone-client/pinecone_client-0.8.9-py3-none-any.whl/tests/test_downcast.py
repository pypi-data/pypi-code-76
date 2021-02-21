from unittest import mock
import unittest

from pinecone import utils
from pinecone.functions.index import vector

import numpy as np
import uuid

def test_downcast_function_numeric():
    dtypes = [np.float32, np.float64, np.int, np.int64]
    for dtype in dtypes:
        data = np.arange(10).astype(dtype)
        downcast_data = vector.VectorIndex.downcast_data(data)
        assert(downcast_data.dtype == np.float32)
        assert(downcast_data.shape == data.shape)
        for i in range(len(data)):
            assert(int(data[i]) == int(downcast_data[i]))


def test_downcast_function_string():
    data = np.array([str(i) for i in range(10)])
    try:
        downcast_data = vector.VectorIndex.downcast_data(data)
        assert False  # shouldn't get here
    except Exception as e:
        assert e.__class__ == TypeError


class TestVectorShape(unittest.TestCase):
    class Fixture(vector.VectorIndex):
        def __init__(self, d):
            super().__init__()
            self.d = d
            self.add_call_count = 0
            self.query_call_count = 0

        def dimension(self):
            return self.d

        def add_data(self, data, ids):
            self.add_call_count += 1

        def query(self, vectors, k, include_data):
            self.query_call_count += 1
            return []

    def setUp(self):
        self.d = d = 128
        self.invalid_data = [np.array(1, dtype=np.float32),  # scalar
                             np.ones(d - 1),  # d != (d - 1)
                             np.ones((1, d - 1)),  # (1, d) != (1, d -1)
                             np.ones((3, 1, d))]   # rank 3
        self.valid_data = [np.ones(d),  # d
                           np.ones((1, d)),  # n, d
                           np.ones((2, d))]  # n, d

    def test_index_vector_shape_rank_invalid(self):
        for data in self.invalid_data:
            msg = mock.Mock()
            msg.WhichOneof.return_value = 'index'
            msg.index.data = utils.dump_numpy(data)
            msg.index.ids = [str(uuid.uuid4())]
            f = self.Fixture(self.d)
            with self.assertRaises(ValueError):
                f.handle_msg(msg)
            self.assertEqual(f.add_call_count, 0)

    def test_index_vector_shape_rank_valid(self):
        for data in self.valid_data:
            msg = mock.Mock()
            msg.WhichOneof.return_value = 'index'
            msg.index.data = utils.dump_numpy(data)
            msg.index.ids = [str(uuid.uuid4())]
            f = self.Fixture(self.d)
            f.handle_msg(msg)
            self.assertEqual(f.add_call_count, 1)


    def test_query_vector_shape_rank_invalid(self):
        for data in self.invalid_data:
            msg = mock.Mock()
            msg.WhichOneof.return_value = 'query'
            msg.query.data = utils.dump_numpy(data)
            f = self.Fixture(self.d)
            with self.assertRaises(ValueError):
                f.handle_msg(msg)
            self.assertEqual(f.query_call_count, 0)

    def test_query_vector_shape_rank_valid(self):
        for data in self.valid_data:
            msg = mock.Mock()
            msg.WhichOneof.return_value = 'query'
            msg.query.data = utils.dump_numpy(data)

            f = self.Fixture(self.d)
            f.handle_msg(msg)
            self.assertEqual(f.query_call_count, 1)
