# -*- coding: utf-8 -*-
"""cubicweb-ctl plugin providing the index-in-es command

:organization: Logilab
:copyright: 2016-2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
from __future__ import print_function

import os.path as osp

from elasticsearch.helpers import parallel_bulk

from cubicweb.cwctl import CWCTL, init_cmdline_log_threshold
from cubicweb.cwconfig import CubicWebConfiguration as cwcfg
from cubicweb.toolsutils import Command

from cubicweb_elasticsearch.es import indexable_types, indexable_entities

HERE = osp.dirname(osp.abspath(__file__))


class IndexInES(Command):
    """Index content in ElasticSearch.

    <instance id>
      identifier of the instance

    """

    name = "index-in-es"
    min_args = max_args = 1
    arguments = "<instance id>"
    options = [
        (
            "dry-run",
            {
                "action": "store_true",
                "default": False,
                "short": "N",
                "help": "set to True if you want to skip the insertion in ES",
            },
        ),
        (
            "debug",
            {
                "action": "store_true",
                "default": False,
                "short": "D",
                "help": ("shortcut for --loglevel=debug"),
            },
        ),
        (
            "loglevel",
            {
                "short": "l",
                "type": "choice",
                "metavar": "<log level>",
                "default": None,
                "choices": ("debug", "info", "warning", "error"),
            },
        ),
        (
            "etypes",
            {
                "type": "csv",
                "default": "",
                "help": "only index given etypes [default:all indexable types]",
            },
        ),
        (
            "index-name",
            {
                "type": "string",
                "default": "",
                "help": (
                    "override index-name if you want to use a different ID"
                    "[default: uses index-name from all-in-one.conf]"
                ),
            },
        ),
        (
            "except-etypes",
            {
                "type": "string",
                "default": "",
                "help": "all indexable types except given etypes" "[default: []]",
            },
        ),
        (
            "chunksize",
            {
                "type": "int",
                "default": 100000,
                "help": "max number of entities to fetch at once (deafult: 100000)",
            },
        ),
    ]

    def run(self, args):
        """run the command with its specific arguments"""
        appid = args.pop(0)
        if self["debug"]:
            self["loglevel"] = "debug"
        config = cwcfg.config_for(appid, debugmode=self["loglevel"])
        if self["loglevel"]:
            init_cmdline_log_threshold(config, self["loglevel"])
        with config.repository().internal_cnx() as cnx:
            schema = cnx.vreg.schema
            indexer = cnx.vreg["es"].select("indexer", cnx)
            es = indexer.get_connection()
            indexer.create_index()
            if self.config.index_name:
                cnx.info("create ES index {}".format(self.config.index_name))
                indexer.create_index(index_name=self.config.index_name)
            if es:
                if self.config.etypes:
                    etypes = self.config.etypes
                else:
                    etypes = indexable_types(
                        schema, custom_skip_list=self.config.except_etypes
                    )
                    assert self.config.except_etypes not in etypes
                if not self.config.etypes:
                    cnx.debug(u"found indexable types: {}".format(",".join(etypes)))
                for _ in parallel_bulk(
                    es,
                    self.bulk_actions(
                        etypes,
                        cnx,
                        index_name=self.config.index_name,
                        dry_run=self.config.dry_run,
                    ),
                    raise_on_error=False,
                    raise_on_exception=False,
                ):
                    pass
            else:
                cnx.info(u"no elasticsearch configuration found, skipping")

    def bulk_actions(self, etypes, cnx, index_name=None, dry_run=False):
        if index_name is None:
            index_name = cnx.vreg.config["index-name"]
        for etype in etypes:
            for idx, entity in enumerate(
                indexable_entities(cnx, etype, chunksize=self.config.chunksize), 1
            ):
                try:
                    serializer = entity.cw_adapt_to("IFullTextIndexSerializable")
                    json = serializer.serialize(complete=False)
                except Exception:
                    cnx.error(
                        "[{}] Failed to serialize entity {} ({})".format(
                            index_name, entity.eid, etype
                        )
                    )
                    continue
                if not dry_run and json:
                    # Entities with
                    # fulltext_containers relations return their container
                    # IFullTextIndex serializer , therefor the "id" and
                    # "doc_type" in kwargs bellow must be container data.
                    data = {
                        "_op_type": "index",
                        "_index": index_name or cnx.vreg.config["index-name"],
                        "_id": serializer.es_id,
                        "_source": json,
                    }
                    self.customize_data(data)
                    yield data
            cnx.info(u"[{}] indexed {} {} entities".format(index_name, idx, etype))

    def customize_data(self, data):
        pass


CWCTL.register(IndexInES)
