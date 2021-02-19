from typing import Type, Dict, List, Tuple, Sequence, Optional

import pytest
from pydantic import BaseModel

from pyappconf.model import BaseConfig, AppConfig
from tests.config import ENV_PATH


def get_model_classes() -> Tuple[Type[BaseConfig], Type[BaseModel]]:
    class SubConfig(BaseModel):
        a: str
        b: float

    class MyConfig(BaseConfig):
        string: str
        integer: int
        custom: SubConfig
        dictionary: Dict[str, SubConfig]
        str_list: List[str]
        int_tuple: Tuple[int, ...]

        default_string: str = "woo"
        default_custom: SubConfig = SubConfig(a="yeah", b=5.6)

        _settings: AppConfig = AppConfig(app_name='MyApp')

        class Config:
            env_prefix = 'MYAPP_'
            env_file = ENV_PATH


    return MyConfig, SubConfig


def get_model_object(exclude_keys: Optional[Sequence[str]] = None, **kwargs) -> BaseConfig:
    MyConfig, SubConfig = get_model_classes()

    all_kwargs = dict(
        string="a",
        integer=5,
        custom=SubConfig(a="b", b=8.5),
        dictionary={"yeah": SubConfig(a="c", b=9.6)},
        str_list=["a", "b", "c"],
        int_tuple=(1, 2, 3),
    )
    if exclude_keys is not None:
        all_kwargs = {key: value for key, value in all_kwargs.items() if key not in exclude_keys}
    all_kwargs.update(kwargs)

    # conf = MyConfig(**{'myapp_' + key: value for key, value in all_kwargs.items()})
    conf = MyConfig(**all_kwargs)
    return conf


@pytest.fixture(scope="session")
def model_classes() -> Tuple[Type[BaseConfig], Type[BaseModel]]:
    return get_model_classes()


@pytest.fixture(scope="session")
def model_object() -> BaseConfig:
    return get_model_object()
