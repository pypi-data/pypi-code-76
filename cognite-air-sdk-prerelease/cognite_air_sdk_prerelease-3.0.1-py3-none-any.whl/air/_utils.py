import json
import os
from pathlib import Path
from typing import Dict

from ruamel.yaml import YAML

from cognite.air.utils import strip_patch_from_version


def _load_yaml(path: Path) -> Dict:
    yaml = YAML(typ="safe").load(path)
    assert isinstance(yaml, dict)
    return yaml


def _read_local_config() -> Dict:
    path_of_this_file = Path(__file__).parent.absolute()
    print(path_of_this_file)
    return _load_yaml(path_of_this_file / Path("config.yaml"))


def retrieve_field_definitions():
    fields = _read_local_config().get("fields")
    output = []
    for i in fields.keys():
        output.append({**{"id": i}, **fields[i]})
    return json.dumps(output)


def retrieve_model_name():
    cwd = os.getcwd()
    print(cwd)
    model_name = Path(cwd).parent.parent.parts[-1]
    print(model_name)
    return model_name


def retrieve_model_version():
    model_version = _read_local_config().get("modelSettings").get("modelVersion")
    return strip_patch_from_version(model_version)
