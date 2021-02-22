from unittest import mock

from aloe import step, world

from quartic_sdk import APIClient
from quartic_sdk.core.entities import Tag, Asset
from quartic_sdk.core.entity_helpers.entity_list import EntityList
from quartic_sdk.core.iterators.tag_data_iterator import TagDataIterator
from quartic_sdk.utilities.test_helpers import (
    APIHelperCallAPI,
    ASSET_LIST_GET,
    TAG_LIST_GET,
    TAG_DATA_POST
    )


@step("we have successfully set up client and mocked requests method")
def step_impl(context):
    """
    For the first step we setup the APIClient
    """
    world.client = APIClient("test_host", username="username", password="password")


@step("we call different internal methods")
def step_impl(context):
    """
    Now we call the different internal methods and save their values
    internally in the world parameter
    """

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(ASSET_LIST_GET)

        world.client_assets = world.client.assets()

    world.first_asset = world.client_assets.first()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(TAG_LIST_GET)

        world.first_asset_tags = world.first_asset.get_tags()

    world.first_tag = world.first_asset_tags.first()

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(TAG_DATA_POST)

        world.tag_data = world.first_tag.data(start_time=1,stop_time=2)

@step("the return matches the expectations")
def step_impl(context):
    """
    In this step we assert to ensure that the methods call the correct functions
    to ensure the correct variable types and the respective data created
    """
    assert isinstance(world.client_assets, EntityList)
    assert world.client_assets.first().id == 1

    assert isinstance(world.first_asset, Asset)
    assert world.first_asset.id == 1

    assert isinstance(world.first_tag, Tag)
    assert world.first_tag.id == 1

    assert isinstance(world.tag_data, TagDataIterator)
