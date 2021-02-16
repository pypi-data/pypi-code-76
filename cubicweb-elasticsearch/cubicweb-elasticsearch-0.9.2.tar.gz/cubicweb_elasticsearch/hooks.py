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

"""cubicweb-elasticsearch specific hooks and operations"""

from cubicweb.server import hook
from cubicweb.predicates import score_entity

from cubicweb_elasticsearch.es import indexable_types


def entity_indexable(entity):
    """ returns boolean to indicate if entity is indexable """
    return (
        entity.cw_etype in indexable_types(entity._cw.vreg.schema)
        or entity.cw_adapt_to("IFullTextIndexSerializable").custom_indexable_attributes
    )


class ContentUpdateIndexES(hook.Hook):
    """detect content change and updates ES indexing"""

    __regid__ = "elasticsearch.contentupdatetoes"
    __select__ = hook.Hook.__select__ & score_entity(entity_indexable)
    events = ("after_update_entity", "after_add_entity", "after_delete_entity")
    category = "es"

    def __call__(self):
        op_type = "delete" if self.event == "after_delete_entity" else "index"
        IndexEsOperation.get_instance(self._cw).add_data(
            {
                "op_type": op_type,
                "entity": self.entity,
            }
        )


class RelationsUpdateIndexES(hook.Hook):
    """detect relations changes and updates ES indexing"""

    __regid__ = "elasticsearch.relationsupdatetoes"
    events = ("after_add_relation", "before_delete_relation")
    category = "es"

    def __call__(self):
        # XXX add a selector for object and subject
        for entity in (
            self._cw.entity_from_eid(self.eidfrom),
            self._cw.entity_from_eid(self.eidto),
        ):
            if entity_indexable(entity):
                IndexEsOperation.get_instance(self._cw).add_data(
                    {
                        "op_type": "index",
                        "entity": entity,
                    }
                )


class IndexEsOperation(hook.DataOperationMixIn, hook.Operation):
    """ mixin class to process ES indexing as a postcommit event """

    containercls = list

    def postcommit_event(self):
        queue = self.cnx.vreg["es"].select("es.opqueue", req=self.cnx)
        queue.process_operations(self.get_data())
