#!/usr/bin/env python

"""Tests for `acdh_arche_pyutils.client` module."""

import unittest
from acdh_arche_pyutils.utils import (
    camel_to_snake,
    create_query_sting
)
from acdh_arche_pyutils.client import ArcheApiClient


class Test_pyutils_client(unittest.TestCase):
    """Tests for `acdh_arche_pyutils.utils` module."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.endpoint = "https://arche-curation.acdh-dev.oeaw.ac.at/api/"
        self.arche_client = ArcheApiClient(self.endpoint)
        self.top_col = self.arche_client.top_col_ids()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_parse_url(self):
        self.assertEqual(self.arche_client.endpoint, self.endpoint)

    def test_002_get_description(self):
        description = self.arche_client.description
        self.assertEqual(type(description), dict)

    def test_003_convert_camel_case(self):
        strings = [
            'CamelCase',
            'camel_Case',
            'camel_case',
        ]
        should_be = 'camel_case'
        for x in strings:
            self.assertEqual(camel_to_snake(x), should_be)

    def test_004_populate_client_props(self):
        for x in ['id', 'parent', 'modification_date']:
            self.assertTrue(hasattr(self.arche_client, x))

    def test_005_base_url_match(self):
        a_cl = self.arche_client
        self.assertEqual(a_cl.endpoint, a_cl.fetched_endpoint)

    def test_006_create_query_sting(self):
        query_params = {
            "p[0]": "http://www.w3.org/syntax-ns#type",
            "v[0]": "https://schema#TopCollection"
        }
        should_be = 'p[0]=http://www.w3.org/syntax-ns%23type&v[0]=https://schema%23TopCollection'
        self.assertEqual(create_query_sting(query_params), should_be)

    def test_007_top_cols(self):
        self.assertEqual(type(self.top_col), list)
        self.assertEqual(len(self.top_col[0]), 2)
