from pinecone.functions.model import postprocessor as pp_mod

from pinecone.utils import load_numpy, dump_numpy
import numpy

from unittest import mock
import unittest


class TestPostprocessor(unittest.TestCase):
    class Fixture(pp_mod.Postprocessor):
        def __init__(self, final_matches):
            super().__init__()
            self.final_matches = final_matches

        def transform(self, queries, matches):
            return self.final_matches

    def test_valid_case(self):
        result_sets = [mock.Mock()]
        result_sets[0].ids = [1, 2, 3]
        result_sets[0].scores = [4, 5, 6]
        result_sets[0].data = None

        self.pp = self.Fixture(result_sets)
        msg = mock.Mock()
        matches = [mock.Mock()]
        matches[0].ids = []
        matches[0].scores = []
        msg.WhichOneof.return_value = "query"
        msg.query.include_data = False
        msg.query.matches = matches
        msg.query.data = dump_numpy(numpy.random.rand(1,10))

        self.pp.handle_msg(msg)

        assert msg.query.matches[0].ids == [1, 2, 3]
        assert msg.query.matches[0].scores == [4, 5, 6]
