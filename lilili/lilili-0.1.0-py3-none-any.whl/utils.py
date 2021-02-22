import json
import logging
import re
from typing import Dict, Optional

import requests
import yaml

from .db.defs import Spdx

logger = logging.getLogger(__name__)


def fetch_json(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict]:
    if headers is None:
        headers = {}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def normalize_license_name(name: str) -> str:
    """Normalize the license name.

    Parameters
    ----------
    name : str
        license name.

    Returns
    -------
    str
        Normalized license name.

    Examples
    --------
    >>> assert normalize_license_name("MIT License") == "mitlicense"
    >>> assert normalize_license_name("Apache License V2.0") == "apachelicense20"
    """
    name = name.lower()
    name = re.sub(r"v([\d.]+)", r"\1", name)
    name = re.sub(r"[- .]", "", name)
    return name


LICENSES = {
    spdx: [normalize_license_name(name) for name in spdx.value] for spdx in Spdx
}


def determine_spdx(name: str) -> Optional[Spdx]:
    """Determine the SPDX license.

    Parameters
    ----------
    name : str
        License name.

    Returns
    -------
    Optional[str]
        SPDX license.

    Examples
    --------
    >>> assert determine_spdx("MIT License") is Spdx.MIT
    >>> assert determine_spdx("THE MIT LICENSE") is Spdx.MIT
    """
    org_name = str(name)

    if type(name) != str:
        logger.warning(f"Unrecognized license name: {org_name}")
        return None

    name = normalize_license_name(name)
    for spdx, normalized_names in LICENSES.items():
        if name in normalized_names:
            return spdx

    if name is not None and name != "":
        logger.warning(f"Unrecognized license name: {org_name}")
    return None


def output_json(dic, file_path: Optional[str] = None) -> None:
    if file_path is None:
        file_path = "result.json"
    with open(file_path, mode="wt", encoding="utf-8") as f:
        json.dump(dic, f, indent=2, ensure_ascii=False)


def output_yaml(dic, file_path: Optional[str] = None) -> None:
    if file_path is None:
        file_path = "result.yml"
    with open(file_path, mode="wt", encoding="utf-8") as f:
        f.write(yaml.dump(dic, sort_keys=False))


def output(as_json: bool, as_yaml: bool, dic, file_path: Optional[str] = None) -> None:
    if as_json:
        output_json(dic, file_path)
    if as_yaml:
        output_yaml(dic, file_path)
    if not as_json and not as_yaml:
        print(dic)
