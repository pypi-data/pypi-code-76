from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from ..models import GWRLink


def test_gwrlink_list(
    db, admin_client, gwr_link_factory, deterministic_uuids, snapshot
):
    gwr_link_factory.create_batch(3)

    url = reverse("gwrlink-list")

    resp = admin_client.get(url)
    assert resp.status_code == HTTP_200_OK
    snapshot.assert_match(resp.json())


def test_gwrlink_retrieve(db, admin_client, deterministic_uuids, gwrlink, snapshot):
    url = reverse("gwrlink-detail", args=[gwrlink.pk])

    resp = admin_client.get(url)
    assert resp.status_code == HTTP_200_OK
    snapshot.assert_match(resp.json())


def test_gwrlink_create(db, admin_client, deterministic_uuids, snapshot):
    url = reverse("gwrlink-list")

    data = {
        "data": {
            "type": "gwr-links",
            "attributes": {
                "eproid": "foo",
                "local-id": "bar",
                "context": {"some-attr": "some value", "some-int-attr": 23},
            },
        }
    }

    resp = admin_client.post(url, data)
    assert resp.status_code == HTTP_201_CREATED
    assert GWRLink.objects.count() == 1
    gwrlink = GWRLink.objects.first()
    assert gwrlink.eproid == "foo"
    assert gwrlink.local_id == "bar"
    assert gwrlink.context == {"some-attr": "some value", "some-int-attr": 23}
    snapshot.assert_match(resp.json())


def test_gwrlink_patch(db, admin_client, deterministic_uuids, gwrlink, snapshot):
    url = reverse("gwrlink-detail", args=[gwrlink.pk])

    assert gwrlink.eproid != "foo"

    data = {
        "data": {
            "id": gwrlink.pk,
            "type": "gwr-links",
            "attributes": {
                "eproid": "foo",
                "local-id": "bar",
                "context": {"some-attr": "some value", "some-int-attr": 23},
            },
        }
    }

    resp = admin_client.patch(url, data)
    assert resp.status_code == HTTP_200_OK
    assert GWRLink.objects.count() == 1
    gwrlink = GWRLink.objects.get(pk=gwrlink.pk)
    assert gwrlink.eproid == "foo"
    assert gwrlink.local_id == "bar"
    assert gwrlink.context == {"some-attr": "some value", "some-int-attr": 23}
    snapshot.assert_match(resp.json())


def test_gwrlink_destroy(db, admin_client, deterministic_uuids, gwrlink, snapshot):
    url = reverse("gwrlink-detail", args=[gwrlink.pk])

    assert GWRLink.objects.count() == 1

    resp = admin_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert GWRLink.objects.count() == 0
