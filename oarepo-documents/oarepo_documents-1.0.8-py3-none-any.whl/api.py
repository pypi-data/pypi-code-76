# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# invenio-app-ils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""ILS Document APIs."""

import uuid

import requests
from crossref.restful import Works
from flask import current_app, Response, request
from invenio_base.utils import obj_or_import_string
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_pidstore.errors import PersistentIdentifierError, PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from oarepo_actions.decorators import action

from .document_json_mapping import schema_mapping
from .minter import document_minter


class DocumentRecordMixin:
    """Class for document record."""
    DOI_PID_TYPE = 'doi'
    DOCUMENT_MINTER = document_minter
    DOCUMENT_INDEXER = RecordIndexer
    @classmethod
    @action(detail=False, method="post", url_path="document/<string:first_part>/<string:second_part>")
    def document_by_doi(cls, record_class, first_part=None, second_part=None, **kwargs):
        """Get metadata from DOI."""
        doi = first_part + '/' + second_part
        try:
            pid = PersistentIdentifier.get(cls.DOI_PID_TYPE, doi)
            record = cls.get_record(pid.object_uuid)
            return Response(status=302, headers={"Location": record.canonical_url})
        except PIDDoesNotExistError:
            pass

        existing_document = getMetadataFromDOI(doi)

        record_uuid = uuid.uuid4()
        data = schema_mapping(existing_document, doi)
        minter = cls.DOCUMENT_MINTER
        if hasattr(minter, '_get_current_object'):
            minter = minter._get_current_object()
        if isinstance(minter, str):
            minter = obj_or_import_string(current_pidstore.minters[minter])
        minter(record_uuid, data)
        record = cls.create(data=data, id_=record_uuid)
        indexer = cls.DOCUMENT_INDEXER()
        indexer.index(record)
        PersistentIdentifier.create(cls.DOI_PID_TYPE, doi, object_type='rec',
                                    object_uuid=record_uuid,
                                    status=PIDStatus.REGISTERED)

        db.session.commit()
        return Response(status=302, headers={"Location": record.canonical_url})

class CrossRefClient(object):
    """Class for CrossRefClient."""

    def __init__(self, accept='text/x-bibliography; style=apa', timeout=3):
        """
        # Defaults to APA biblio style.

        # Usage:
        s = CrossRefClient()
        print s.doi2apa("10.1038/nature10414")
        """
        self.headers = {'accept': accept}
        self.timeout = timeout

    def query(self, doi, q={}):
        #Get query.
        if doi.startswith("http://"):
            url = doi
        else:
            url = "http://dx.doi.org/" + doi

        r = requests.get(url, headers=self.headers)
        return r

    def doi2apa(self, doi):
        self.headers['accept'] = 'text/x-bibliography; style=apa'
        return self.query(doi).text

    def doi2turtle(self, doi):
        self.headers['accept'] = 'text/turtle'
        return self.query(doi).text

    def doi2json(self, doi):
        self.headers['accept'] = 'application/vnd.citationstyles.csl+json'
        return self.query(doi).json()

    def doi2xml(self, doi):
        self.headers['accept'] = 'application/rdf+xml'
        return self.query(doi).text



def getMetadataFromDOI(id):
    works = Works()
    metadata = works.doi(id)

    if metadata is None:
        s = CrossRefClient()
        metadata = s.doi2json(id)
    metadata.pop('id', None)
    return metadata

