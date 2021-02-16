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

"""cubicweb-elasticsearch entity's classes"""

import collections

from functools import partial

from urllib3.exceptions import ProtocolError

from elasticsearch.exceptions import ConnectionError, NotFoundError

from logilab.common.decorators import cachedproperty

from cubicweb import view, neg_role
from cubicweb.predicates import is_instance

from cubicweb.appobject import AppObject

from cubicweb_elasticsearch import es


def deep_update(d1, d2):
    for key, value in d2.iteritems():
        if isinstance(value, collections.Mapping):
            d1[key] = deep_update(d1.get(key, {}), value)
        else:
            d1[key] = d2[key]
    return d1


class EsRegistry(AppObject):
    __registry__ = "es"


class Indexer(EsRegistry):
    __regid__ = "indexer"
    adapter = "IFullTextIndexSerializable"
    settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "default": {
                        "filter": ["my_ascii_folding", "lowercase", "french_snowball"],
                        "tokenizer": "standard",
                    }
                },
                "filter": {
                    "my_ascii_folding": {
                        "preserve_original": True,
                        "type": "asciifolding",
                    },
                    "french_snowball": {"type": "snowball", "language": "French"},
                },
            },
        }
    }

    @property
    def index_name(self):
        return self._cw.vreg.config["index-name"]

    def get_connection(self):
        self.create_index()
        return es.get_connection(self._cw.vreg.config)

    def create_index(self, index_name=None, custom_settings=None):
        index_name = index_name or self.index_name
        if custom_settings is None:
            settings = self.settings
        else:
            settings = {}
            deep_update(settings, self.settings)
            deep_update(settings, custom_settings)
        es_cnx = es.get_connection(self._cw.vreg.config)
        if es_cnx is not None:
            es.create_index(es_cnx, index_name, settings)

    def es_index(self, entity, params=None):
        es_cnx = self.get_connection()
        if es_cnx is None or not self.index_name:
            self.error("no connection to ES (not configured) skip ES indexing")
            return
        serializable = entity.cw_adapt_to(self.adapter)
        json = serializable.serialize()
        if not json:
            return
        es_cnx.index(
            index=self.index_name,
            id=serializable.es_id,
            doc_type=serializable.es_doc_type,
            body=json,
            params=params,
        )

    def es_delete(self, entity):
        es_cnx = self.get_connection()
        if es_cnx is None or not self.index_name:
            self.error("no connection to ES (not configured) skip ES deletion")
            return
        serializable = entity.cw_adapt_to(self.adapter)
        es_cnx.delete(
            index=self.index_name,
            id=serializable.es_id,
            doc_type=serializable.es_doc_type,
        )


class IFullTextIndexSerializable(view.EntityAdapter):
    """Adapter to serialize an entity to a bare python structure that may be
    directly serialized to e.g. JSON.
    """

    __regid__ = "IFullTextIndexSerializable"
    __select__ = is_instance("Any")
    custom_indexable_attributes = ()
    skip_indexable_attributes = ()

    @property
    def es_id(self):
        return self.entity.eid

    @property
    def es_doc_type(self):
        return "_doc"

    @cachedproperty
    def fulltext_indexable_attributes(self):
        eschema = self._cw.vreg.schema[self.entity.cw_etype]
        attrs = ["creation_date", "modification_date", "cwuri"]
        attrs.extend(
            [
                r.type
                for r in eschema.indexable_attributes()
                if r.type not in self.skip_indexable_attributes
            ]
        )
        for rschema, tschema in eschema.attribute_definitions():
            if rschema.type == "eid":
                continue
            # XXX
            if tschema.type in ("Int", "Float"):
                attrs.append(rschema.type)
        attrs.extend(self.custom_indexable_attributes)
        return attrs

    def process_attributes(self):
        data = {}
        for attr in self.fulltext_indexable_attributes:
            data[attr] = getattr(self.entity, attr)
        return data

    def serialize(self, complete=True):
        entity = self.entity
        if complete:
            entity.complete()
        data = {
            "cw_etype": entity.cw_etype,
            "eid": entity.eid,
            "cwuri": entity.cwuri,
        }
        # TODO take a look at what's in entity.cw_relation_cache
        data.update(self.process_attributes())
        return data


class File(IFullTextIndexSerializable):
    __select__ = IFullTextIndexSerializable.__select__ & is_instance("File")

    def serialize(self, complete=True):
        """this could be a generic implementation of fulltext_containers indexation, but for

        now we can not return more than one parent json which is fine
        for Files
        """
        for rschema, role in self._cw.vreg.schema["File"].fulltext_containers():
            for parent in self.entity.related(
                rschema.type, role=neg_role(role)
            ).entities():
                return parent.cw_adapt_to("IFullTextIndexSerializable").serialize(
                    complete
                )
        return {}


class ESTransactionQueue(EsRegistry):
    __regid__ = "es.opqueue"

    @cachedproperty
    def default_indexer(self):
        return self._cw.vreg["es"].select("indexer", self._cw)

    def purge_useless_operations(self, es_operations):
        """remove operations from `es_operations` that will have no effect.

        For instance:
        - if an entity is indexed several times, just index it once.
        - if an entity is indexed then deleted, simply remove the
          *index* operation.
        Since there are only two kind of operations ('delete' and 'index'),
        the general rule is that the last operation wins and therefore the
        first one is useless. The only corner case is when a delete operation
        is triggered before an index one. In that specific case, emit a warning
        and keep delete operation only.
        """
        done = collections.OrderedDict()
        for es_operation in reversed(es_operations):
            entity = es_operation["entity"]
            op_type = es_operation["op_type"]
            if entity.eid not in done:
                done[entity.eid] = es_operation
            else:
                prev_op_type = done[entity.eid]["op_type"]
                if op_type == "delete" and prev_op_type == "index":
                    self.warning(
                        "a delete operation on %s#%s inserted before" "an index one",
                        entity.cw_etype,
                        entity.eid,
                    )
                    done[entity.eid] = es_operation
        return done.values()

    def process_operation(self, es_operation):
        indexer = es_operation.get("indexer", self.default_indexer)
        entity = es_operation["entity"]
        if self._cw.deleted_in_transaction(entity.eid):
            es_method = indexer.es_delete
        elif es_operation["op_type"] == "index":
            es_method = partial(indexer.es_index, params={"refresh": "true"})
        elif es_operation["op_type"] == "delete":
            es_method = indexer.es_delete
        else:
            self.info(
                "skipping unknown operation type %s on %s",
                es_operation["op_type"],
                entity.eid,
            )
            return
        try:
            es_method(entity)
        except (ConnectionError, ProtocolError, NotFoundError) as exc:
            self.warning(
                "[ES] Failed to %s %s#%s (%s)",
                es_operation["op_type"],
                entity.cw_etype,
                entity.eid,
                exc,
            )

    def process_operations(self, es_operations):
        es_operations = self.purge_useless_operations(es_operations)
        for es_operation in es_operations:
            self.process_operation(es_operation)
        return es_operations
