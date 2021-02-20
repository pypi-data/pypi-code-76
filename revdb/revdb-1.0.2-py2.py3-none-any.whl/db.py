from typing import Any, Type, TypeVar

import requests
from mongoengine import connect as mongo_connect
from mongoengine.base import BaseDocument

URLS_V1 = {
    "stg": "https://jstorage-stg.revtel-api.com/v1/settings",
    "prod": "https://jstorage.revtel-api.com/v1/settings",
}

URLS_V2 = {
    "stg": "https://jstorage-stg.revtel-api.com/v2/settings",
    "prod": "https://jstorage.revtel-api.com/v2/settings",
}


def connect(api_key: str, stage: str = "stg", alias: str = "default") -> None:
    try:
        url = URLS_V1[stage]
    except KeyError as e:
        raise ValueError("stage should be in [stg, prod]") from e

    resp = requests.get(
        url, headers={"Content-Type": "application/json", "x-api-key": api_key}
    )
    resp.raise_for_status()

    resp_json = resp.json()
    mongo_connect(resp_json["id"], host=resp_json["db_host"], alias=alias)


def connect_v2(client_secret: str, stage: str = "stg", alias: str = "default") -> None:
    try:
        url = URLS_V2[stage]
    except KeyError as e:
        raise ValueError("stage should be in [stg, prod]") from e

    full_url = f"{url}?client_secret={client_secret}"
    resp = requests.get(full_url)
    resp.raise_for_status()

    resp_json = resp.json()

    mongo_connect(resp_json["id"], host=resp_json["db_host"], alias=alias)


DOC = TypeVar("DOC", bound=BaseDocument)


def make_model_class(base: Type[DOC], **meta: Any) -> Type[DOC]:
    return type(base.__name__, (base,), {"meta": meta})
