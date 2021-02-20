import json
import locale
import os

import pytest
import yaml


@pytest.fixture(autouse=True)
def setup_locale():
    locale.setlocale(locale.LC_ALL, "en_GB.utf8")
    os.environ["LANG"] = "en_GB.utf8"


def get_test_data(name: str) -> str:
    resources_folder = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../unit-resources")
    return open(f"{resources_folder}/{name}", "r").read()


def get_test_data_json(name: str):
    return json.loads(get_test_data(name))


def get_test_data_yaml(name: str):
    return yaml.safe_load(get_test_data(name))
