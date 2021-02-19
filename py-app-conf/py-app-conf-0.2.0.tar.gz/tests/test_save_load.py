from pathlib import Path
from typing import Type, Tuple

from pydantic import BaseModel

from pyappconf.model import AppConfig, ConfigFormats, BaseConfig
from tests.config import CUSTOM_CONFIG_OUT_PATH
from tests.fixtures.model import (
    get_model_object,
    get_model_classes,
    model_classes,
    model_object,
)


def _save_load_test(custom_settings: AppConfig):
    mod = get_model_object(settings=custom_settings)
    mod.save()
    assert str(mod.settings.config_location).endswith(
        custom_settings.default_format.value
    )

    OrigConfig, SubConfig = get_model_classes()

    class MyConfig(OrigConfig):
        _settings = custom_settings

    assert str(MyConfig._settings.config_location).endswith(
        custom_settings.default_format.value
    )
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


def assert_model_loaded_with_extension(
    mod: BaseConfig, model_object: BaseConfig, format: ConfigFormats
):
    assert mod.settings.custom_config_path == CUSTOM_CONFIG_OUT_PATH
    assert mod.settings.default_format == format

    mod.settings = model_object.settings
    assert mod == model_object


def test_load_toml_with_custom_path(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, _ = model_classes
    mod = MyConfig.load(Path(str(CUSTOM_CONFIG_OUT_PATH) + ".toml"))
    assert_model_loaded_with_extension(mod, model_object, ConfigFormats.TOML)


def test_load_yaml_with_custom_path(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, _ = model_classes
    mod = MyConfig.load(Path(str(CUSTOM_CONFIG_OUT_PATH) + ".yaml"))
    assert_model_loaded_with_extension(mod, model_object, ConfigFormats.YAML)


def test_load_json_with_custom_path(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, _ = model_classes
    mod = MyConfig.load(Path(str(CUSTOM_CONFIG_OUT_PATH) + ".json"))
    assert_model_loaded_with_extension(mod, model_object, ConfigFormats.JSON)