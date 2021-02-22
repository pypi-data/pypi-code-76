from pollination.honeybee_radiance.translate import CreateRadianceFolder

from queenbee.plugin.function import Function


def test_create_radiance_folder():
    function = CreateRadianceFolder().queenbee
    assert function.name == 'create-radiance-folder'
    assert isinstance(function, Function)
