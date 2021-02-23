from pollination.ladybug_comfort.map import PmvMap, AdaptiveMap, UtciMap
from queenbee.plugin.function import Function


def test_pmv_map():
    function = PmvMap().queenbee
    assert function.name == 'pmv-map'
    assert isinstance(function, Function)


def test_adaptive_map():
    function = AdaptiveMap().queenbee
    assert function.name == 'adaptive-map'
    assert isinstance(function, Function)


def test_utci_map():
    function = UtciMap().queenbee
    assert function.name == 'utci-map'
    assert isinstance(function, Function)
