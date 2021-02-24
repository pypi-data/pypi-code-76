# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test files resource integration."""

from io import BytesIO

import pytest


@pytest.mark.skip()
def test_files_publish_flow(client, es_clear, location, headers):
    """Test record creation."""
    h = headers
    # Create a draft
    res = client.post("/mocks", headers=h, json={
        'metadata': {'title': 'Test'}
    })
    assert res.status_code == 201
    id_ = res.json['id']

    # Initialize files upload
    res = client.post(f"/mocks/{id_}/draft/files", headers=h, json=[
        {'key': 'test.pdf'}
    ])
    assert res.status_code == 201
    assert res.json['entries'][0]['key'] == 'test.pdf'
    assert res.json['entries'][0]['status'] == 'pending'

    # Upload a file
    res = client.put(
        f"/mocks/{id_}/draft/files/test.pdf/content",
        headers={'content-type': 'application/octet-stream'},
        data=BytesIO(b'testfile'),
    )
    assert res.status_code == 200

    # Commit the file
    res = client.post(f"/mocks/{id_}/draft/files/test.pdf/commit", headers=h)
    assert res.status_code == 200
    assert res.json['key'] == 'test.pdf'
    assert res.json['status'] == 'completed'

    # Publish the record
    res = client.post(f"/mocks/{id_}/draft/actions/publish", headers=h)
    assert res.status_code == 202

    # Check published files
    res = client.get(f"/mocks/{id_}/files", headers=h)
    assert res.status_code == 200
    assert res.json['key'] == 'test.pdf'
    assert res.json['status'] == 'completed'

    # Edit the record
    res = client.post(f"/mocks/{id_}/draft", headers=h)
    assert res.status_code == 201

    # Publish again
    res = client.post(f"/mocks/{id_}/draft/actions/publish", headers=h)
    assert res.status_code == 202

    # Check published files
    res = client.get(f"/mocks/{id_}/files", headers=h)
    assert res.status_code == 200
    assert res.json['key'] == 'test.pdf'
    assert res.json['status'] == 'completed'


@pytest.mark.skip()
def test_metadata_only_record(client, es_clear, location, headers):
    """Test record with files disabled."""
    h = headers
    # Create a draft
    res = client.post("/mocks", headers=h, json={
        'metadata': {'title': 'Test'}
    })
    assert res.status_code == 201
    id_ = res.json['id']

    # Disable files
    res = client.put(f"/mocks/{id_}/draft/files", headers=h, json={
        'enabled': False,
    })
    assert res.status_code == 200
    assert res.json['enabled'] is False
    assert 'entries' not in res.json

    # Publish the record
    res = client.post(f"/mocks/{id_}/draft/actions/publish", headers=h)
    assert res.status_code == 202

    # Check published files
    res = client.get(f"/mocks/{id_}/files", headers=h)
    assert res.status_code == 200
    assert res.json['enabled'] is False
    assert 'entries' not in res.json

    # Edit the record
    res = client.post(f"/mocks/{id_}/draft", headers=h)
    assert res.status_code == 201

    # Publish again
    res = client.post(f"/mocks/{id_}/draft/actions/publish", headers=h)
    assert res.status_code == 202

    # Check published files
    res = client.get(f"/mocks/{id_}/files", headers=h)
    assert res.status_code == 200
    assert res.json['enabled'] is False
    assert 'entries' not in res.json
