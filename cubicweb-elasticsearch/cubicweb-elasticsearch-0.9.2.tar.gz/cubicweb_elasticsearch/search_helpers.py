# -*- coding: utf-8 -*-
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

from elasticsearch_dsl import Q, query as dsl_query

from logilab.mtconverter import xml_escape


def compose_search(
    search, query=None, fields=(), fuzzy=False, phrase=True, common=True
):
    """
    Compose a elasticsearch-dsl query from queries :

    * simple term
    * simple terms (OR)
    * negation (add - in front of a term)
    * explicit OR
    * quoted terms (AND)

    search:
        search object (used to set doc_type and index_name outside of
        compose_search)
    query:
        text of the query to be composed (can contain quotes)
    fields:
        restrict and boost search on certain fields eg. ('title^2', 'alltext')
    fuzzy:
        add a fuzzy search element to part of the query generated
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html
    """
    # FIXME TODO - restructure entier code base, have a proper lexer
    for char in ('"', "'", xml_escape('"'), xml_escape("'")):
        # TODO - implement phrase + term
        if len(query.split(char)) == 3:
            # TODO add this to most important queries, instead of single query ?
            return search.query(
                "bool",
                must=Q(
                    "multi_match",
                    query=query.split(char)[1],
                    type="phrase",
                    fields=fields,
                ),
            )
    must = []
    must_not = []
    should = []
    cutoff_frequency = 0.001
    # https://www.elastic.co/guide/en/elasticsearch/reference/2.4/query-dsl-minimum-should-match.html
    minimum_should_match = "1"
    # proximity booster - phrase with slop=50

    # TODO find a better way to do this
    if not phrase and not common:  # invalid combination
        phrase = common = True
    if phrase:
        phrase_query = Q(
            "multi_match", query=query, type="phrase", slop=50, fields=fields
        )
        should.append(phrase_query)
    # highfrequency/lowfrequency query
    # https://www.elastic.co/blog/stop-stopping-stop-words-a-look-at-common-terms-query
    if common:
        common_query = dsl_query.Common(
            alltext={
                "query": query,
                "cutoff_frequency": cutoff_frequency,
                "low_freq_operator": "and",
                "minimum_should_match": {"high_freq": "70%"},
            }
        )
        should.append(common_query)

    elements = query.split()
    elements_lowercase = [e.lower() for e in elements]
    if "or" in elements_lowercase and len(elements) >= 3:
        for element in query.split("or"):
            should.append(Q("multi_match", query=element.strip(), fields=fields))
        elements = []
    for element in elements:
        if element.startswith("-"):
            must_not.append(Q("multi_match", query=element[1:], fields=fields))

        else:
            if fuzzy:
                should.append(dsl_query.Fuzzy(alltext=element))
    bool_query = dsl_query.Bool(
        must=must,
        must_not=must_not,
        should=should,
        minimum_should_match=minimum_should_match,
    )
    search.query = bool_query
    return search
