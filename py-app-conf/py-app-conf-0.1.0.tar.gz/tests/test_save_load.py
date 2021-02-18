from pyappconf.model import AppConfig, ConfigFormats
from tests.config import CUSTOM_CONFIG_OUT_PATH
from tests.fixtures.model import get_model_object, get_model_classes


def _save_load_test(custom_settings: AppConfig):
    mod = get_model_object(settings=custom_settings)
    mod.save()

    OrigConfig, SubConfig = get_model_classes()

    class MyConfig(OrigConfig):
        _settings = custom_settings

    obj = MyConfig.load()
    assert mod == obj


def test_save_load_toml():
    custom_settings = AppConfig(
        app_name="MyApp", custom_config_path=CUSTOM_CONFIG_OUT_PATH
    )
    _save_load_test(custom_settings)


def test_save_load_yaml():
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_path=CUSTOM_CONFIG_OUT_PATH,
        default_format=ConfigFormats.YAML,
    )
    _save_load_test(custom_settings)


def test_save_load_json():
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_path=CUSTOM_CONFIG_OUT_PATH,
        default_format=ConfigFormats.JSON,
    )
    _save_load_test(custom_settings)