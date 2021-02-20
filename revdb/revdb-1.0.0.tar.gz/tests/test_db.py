from unittest.mock import patch

from mongoengine import DynamicDocument
from mongoengine import connect as mongo_connect
from mongoengine.connection import _get_db

from revdb import connect, connect_v2, make_model_class

PATCH_PATH = "requests.get"


class DocumentBase(DynamicDocument):  # type: ignore
    meta = {"abstract": True}


def test_make() -> None:
    child_doc = make_model_class(
        DocumentBase, db_alias="child_alias", collection="child_collection"
    )
    mongo_connect("child_db", host="server.example.com", alias="child_alias")
    assert issubclass(child_doc, DocumentBase)
    assert child_doc._get_collection_name() == "child_collection"
    assert child_doc._get_db().name == "child_db"


def test_connect() -> None:
    with patch(PATCH_PATH) as requests:
        requests.return_value.json.return_value = {
            "id": "test-id",
            "db_host": "fakehost.com",
        }
        connect(api_key="testkey", alias="test_host")

        assert _get_db("test_host").name == "test-id"

        try:
            connect(api_key="testkey", alias="test_host", stage="error_stage")
        except ValueError as e:
            assert str(e) == "stage should be in [stg, prod]"


def test_connect_v2() -> None:
    with patch(PATCH_PATH) as requests:
        requests.return_value.json.return_value = {
            "id": "test-v2",
            "db_host": "fakehost.com",
        }
        connect_v2(client_secret="testkey", alias="test_v2")

        assert _get_db("test_v2").name == "test-v2"

        try:
            connect_v2(client_secret="testkey", alias="test_host", stage="error_stage")
        except ValueError as e:
            assert str(e) == "stage should be in [stg, prod]"
