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

import logging

from elasticsearch.exceptions import ConnectionError
from urllib3.exceptions import ProtocolError
from elasticsearch_dsl.connections import connections

from rql import parse as rql_parse
from rql.utils import rqlvar_maker

INDEXABLE_TYPES = None

# customization mechanism, in your cube, add your type as a key, and a list of
# additionnal attributes

log = logging.getLogger(__name__)


def indexable_types(schema, custom_skip_list=None):
    """
    introspect indexable types
    """
    global INDEXABLE_TYPES
    if INDEXABLE_TYPES is not None:
        return INDEXABLE_TYPES
    indexable_types = []
    skip_list = ["TrInfo", "EmailAddress"]
    if custom_skip_list:
        skip_list = skip_list + custom_skip_list
    for eschema in schema.entities():
        if eschema.type in skip_list:
            continue
        if not eschema.final:
            # check eschema.fulltext_relations() ? (skip wf_info_for ?
            # )
            if list(eschema.indexable_attributes()):
                indexable_types.append(eschema.type)
    INDEXABLE_TYPES = indexable_types
    return indexable_types


def fulltext_indexable_rql(etype, cnx, eid=None):
    """
    Generate RQL with fulltext_indexable attributes for a given entity type

    :eid:
       defaults to None, set it to an eid to get RQL for a single element (used in hooks)
    """
    varmaker = rqlvar_maker()
    V = next(varmaker)
    rql = ["WHERE %s is %s" % (V, etype)]
    if eid:
        rql.append("%s eid %i" % (V, eid))
    var = next(varmaker)
    selected = []
    cw_entity = cnx.vreg["etypes"].etype_class(etype)(cnx)
    for attr in cw_entity.cw_adapt_to(
        "IFullTextIndexSerializable"
    ).fulltext_indexable_attributes:
        var = next(varmaker)
        rql.append("%s %s %s" % (V, attr, var))
        selected.append(var)
    return "Any %s,%s %s" % (V, ",".join(selected), ",".join(rql))


def indexable_entities(cnx, etype, chunksize=100000):
    """yield indexable entities of type `etype`

    This function uses `fulltext_indexable_rql` to build the appropriate RQL
    query for `etype` and then adds ``ORDERBY`` / ``LIMIT`` clauses to build
    rsets of at most `chunksize` length.

    Instead of doing::

        rql = fulltext_indexable_rql(etype, cnx)
        rset = cnx.execute(rql)
        for entity in rset.entities():
            # do something with entity

    You can therefore use this drop-in "memory efficient" alternative:

        for entity in indexable_entities(cnx, etype):
            # do something with entity
    """
    rql = fulltext_indexable_rql(etype, cnx)
    rqlst = rql_parse(rql).children[0]
    rqlst.set_limit(chunksize)
    mainvar = next(rqlst.get_selected_variables())
    rqlst.add_sort_var(mainvar)
    last_eid = 0
    while True:
        rqlst.save_state()
        rqlst.add_constant_restriction(mainvar, "eid", last_eid, "Int", ">")
        rql = rqlst.as_string()
        rqlst.recover()
        cnx.debug(u"RQL: {}".format(rql))
        rset = cnx.execute(rql)
        if not rset:
            break
        for entity in rset.entities():
            yield entity
            entity.cw_clear_all_caches()
        cnx.drop_entity_cache()
        last_eid = rset[-1][0]


def create_index(es, index_name, settings=None):
    """Create ``index_name`` if it doesn't already exist in ES


    Parameters
    ----------

    :es:
      the elastic search connection

    :index_name:
      the index name

    :settings:
      mapping and analyzer definitions

    """
    try:
        if index_name and not es.indices.exists(index=index_name):
            es.indices.create(index=index_name, body=settings)
    except (ConnectionError, ProtocolError):
        log.debug("Failed to index in hook, could not connect to ES")


def get_connection(config):
    """
    Get connection with config object, creates a persistent connexion and
    """
    try:
        return connections.get_connection()
    except KeyError:
        locations = config["elasticsearch-locations"]
        if locations:
            # TODO sanitize locations
            es = connections.create_connection(
                hosts=locations.split(","),
                verify_certs=config["elasticsearch-verify-certs"],
                ssl_show_warn=config["elasticsearch-ssl-show-warn"],
                timeout=20,
            )
            return es
        # TODO else ? raise KeyError - return None is OK?
