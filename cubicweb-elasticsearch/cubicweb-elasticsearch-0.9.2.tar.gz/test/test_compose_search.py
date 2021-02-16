# copyright 2016-2021 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import unittest
from elasticsearch_dsl import Search

from cubicweb.devtools import testlib
from cubicweb_elasticsearch.search_helpers import compose_search
from logilab.mtconverter import xml_escape


class ComposeSearchTestCase(testlib.TestCase):
    def compose_search(self, query):
        self.search = Search()
        return compose_search(self.search, query)

    def test_simple(self):
        self.assertTrue(self.compose_search("test").to_dict())

    def test_two_terms(self):
        self.assertTrue(self.compose_search("test this").to_dict())

    def test_one_quote(self):
        # only one quote is not a phrase type search
        self.assertTrue(self.compose_search("test 'this").to_dict())

    def test_two_with_quotes(self):
        self.assertTrue(self.compose_search('"test this"').to_dict())
        self.assertTrue(self.compose_search("'test this'").to_dict())
        self.assertTrue(self.compose_search(xml_escape("'test this'")).to_dict())

    # def test_three_with_quotes(self):
    #     self.assertTrue(self.compose_search('"test this" this_too').to_dict(),
    #                       Q('bool',
    #                         must=[Q('multi_match', query='test', fields=()).to_dict(),
    #                               Q('multi_match', query='this', fields=())],
    #                         should=).to_dict())

    def test_two_with_negate(self):
        self.assertTrue(self.compose_search("test -this").to_dict())

    def test_two_with_or(self):
        self.assertTrue(self.compose_search("test or this").to_dict())
        # self.assertTrue(self.compose_search('test ou this'),
        #                   self.search.query('bool',
        #                     should=[Q('multi_match', query='test', fields=()),
        # Q('multi_match', query='this', fields=())]).to_dict())

    def test_or_on_its_own(self):
        self.assertTrue(self.compose_search("or").to_dict())


if __name__ == "__main__":
    unittest.main()
