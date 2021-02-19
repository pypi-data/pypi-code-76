from pathlib import Path
from unittest.mock import patch

from pyappconf.model import BaseConfig, AppConfig
from tests.fixtures.model import model_object, get_model_object


@patch("sys.platform", "linux")
def test_config_base_location_linux(model_object: BaseConfig):
    assert (
        model_object.settings.config_base_location
        == Path("~").expanduser() / ".config" / "MyApp" / "config"
    )


@patch("sys.platform", "linux")
def test_config_location_linux(model_object: BaseConfig):
    assert (
        model_object.settings.config_location
        == Path("~").expanduser() / ".config" / "MyApp" / "config.toml"
    )


def test_custom_config_location():
    expect_path = Path("/woo")
    obj = get_model_object(
        settings=AppConfig(app_name="MyApp", custom_config_path=expect_path)
    )
    assert obj.settings.config_base_location == expect_path
