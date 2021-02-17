
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
from quartic_sdk.utilities.test_helpers import ASSET_LIST_GET
from quartic_sdk.core.entities import Asset
from quartic_sdk.core.entity_helpers.entity_list import EntityList


def test_entity_factory_multiple_strategy():
    """
    We test the EntityList creation strategy of EntityFactory for asset type
    """
    asset_entities = EntityFactory(Constants.ASSET_ENTITY, ASSET_LIST_GET, None)
    assert isinstance(asset_entities, EntityList)
    assert isinstance(asset_entities.first(), Asset)


def test_entity_factory_single_strategy():
    """
    We test the entity creation strategy of EntityFactory for asset type
    """
    asset_entity = EntityFactory(Constants.ASSET_ENTITY, ASSET_LIST_GET[0], None)
    assert isinstance(asset_entity, Asset)
