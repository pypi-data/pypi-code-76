# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_gwrlink_list 1"] = {
    "data": [
        {
            "attributes": {
                "context": {},
                "eproid": "run-too-successful",
                "local-id": "decision-create",
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "type": "gwr-links",
        },
        {
            "attributes": {
                "context": {},
                "eproid": "lot-song-light",
                "local-id": "education-art-apply",
            },
            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
            "type": "gwr-links",
        },
        {
            "attributes": {
                "context": {},
                "eproid": "generation-maybe",
                "local-id": "capital-loss-learn",
            },
            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
            "type": "gwr-links",
        },
    ],
    "links": {
        "first": "http://testserver/api/v1/linker/link?page%5Bnumber%5D=1",
        "last": "http://testserver/api/v1/linker/link?page%5Bnumber%5D=1",
        "next": None,
        "prev": None,
    },
    "meta": {"pagination": {"count": 3, "page": 1, "pages": 1}},
}

snapshots["test_gwrlink_retrieve 1"] = {
    "data": {
        "attributes": {
            "context": {},
            "eproid": "note-act-source",
            "local-id": "safe-follow-glass",
        },
        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
        "type": "gwr-links",
    }
}

snapshots["test_gwrlink_create 1"] = {
    "data": {
        "attributes": {
            "context": {"some-attr": "some value", "some-int-attr": 23},
            "eproid": "foo",
            "local-id": "bar",
        },
        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
        "type": "gwr-links",
    }
}

snapshots["test_gwrlink_patch 1"] = {
    "data": {
        "attributes": {
            "context": {"some-attr": "some value", "some-int-attr": 23},
            "eproid": "foo",
            "local-id": "bar",
        },
        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
        "type": "gwr-links",
    }
}
