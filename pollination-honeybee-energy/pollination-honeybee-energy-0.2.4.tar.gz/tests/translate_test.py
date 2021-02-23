from pollination.honeybee_energy.translate import ModelToOsm
from queenbee.plugin.function import Function


def test_model_to_osm():
    function = ModelToOsm().queenbee
    assert function.name == 'model-to-osm'
    assert isinstance(function, Function)
