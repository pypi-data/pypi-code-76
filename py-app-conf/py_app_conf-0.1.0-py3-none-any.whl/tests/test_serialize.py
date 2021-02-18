from typing import Type, Tuple

from pyappconf.model import BaseConfig
from tests.config import JSON_PATH, YAML_PATH, TOML_PATH
from tests.fixtures.model import model_object, model_classes


def test_to_json(model_object: BaseConfig):
    assert model_object.to_json(json_kwargs=dict(indent=2)) == JSON_PATH.read_text()


def test_to_yaml(model_object: BaseConfig):
    assert model_object.to_yaml() == YAML_PATH.read_text()


def test_to_toml(model_object: BaseConfig):
    assert model_object.to_toml() == TOML_PATH.read_text()


def test_from_json(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseConfig]]
):
    MyConfig, SubConfig = model_classes
    loaded_object = MyConfig.parse_json(JSON_PATH)
    assert model_object == loaded_object


def test_from_yaml(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseConfig]]
):
    MyConfig, SubConfig = model_classes
    loaded_object = MyConfig.parse_yaml(YAML_PATH)
    assert model_object == loaded_object


def test_from_toml(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseConfig]]
):
    MyConfig, SubConfig = model_classes
    loaded_object = MyConfig.parse_toml(TOML_PATH)
    assert model_object == loaded_object