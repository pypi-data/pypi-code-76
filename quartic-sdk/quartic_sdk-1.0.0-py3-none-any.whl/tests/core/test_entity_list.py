
import pytest
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.entity_helpers.entity_list import EntityList
from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
from quartic_sdk.utilities.test_helpers import ASSET_LIST_GET, TAG_LIST_GET, SINGLE_ASSET_GET

asset_entity_list = EntityFactory(Constants.ASSET_ENTITY, ASSET_LIST_GET, None)
test_asset_entity = EntityFactory(Constants.ASSET_ENTITY, ASSET_LIST_GET[0], None)
test_new_asset_entity = EntityFactory(Constants.ASSET_ENTITY, SINGLE_ASSET_GET, None)
test_tag_entity = EntityFactory(Constants.TAG_ENTITY, TAG_LIST_GET[0], None)


def test_entity_list_validate_type():
    """
    We test the `_validate_type` method in EntityList
    """
    assert asset_entity_list._validate_type(test_asset_entity)
    assert not asset_entity_list._validate_type(test_tag_entity)

def test_entity_list_get():
    """
    Test get method of entitylist
    """
    assert asset_entity_list.get("id", 1) == test_asset_entity

def test_entity_list_all():
    """
    Test all method of entitylist
    """
    assert len(asset_entity_list.all()) == 1

def test_entity_list_count():
    """
    Test count method of entitylist
    """
    assert asset_entity_list.count() == 1

def test_entity_list_add():
    """
    Test add method of entitylist for correct and incorrect class types
    """
    added_entity_list = asset_entity_list
    added_entity_list.add(test_new_asset_entity)
    assert added_entity_list.count() == 2
    with pytest.raises(Exception):
        added_entity_list.add(test_tag_entity)

def test_entity_list_first():
    """
    Test first method of entitylist
    """
    assert asset_entity_list.first() == test_asset_entity
