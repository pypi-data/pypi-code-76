from typing import TypedDict

import immutables
from sym.cli.helpers.config.base import ConfigBase

from sym.flow.cli.models import AuthToken, Organization


class ConfigSchema(TypedDict, total=False):
    org: str
    client_id: str
    email: str
    auth_token: AuthToken


class Config(ConfigBase[ConfigSchema]):
    @classmethod
    def get_org(cls) -> immutables.Map:
        config = cls.instance()
        return immutables.Map(
            Organization(slug=config["org"], client_id=config["client_id"])
        )

    @classmethod
    def get_access_token(cls) -> str:
        return cls.instance()["auth_token"]["access_token"]


def store_login_config(email: str, org: Organization, auth_token: AuthToken) -> str:
    cfg = Config.instance()
    cfg["email"] = email
    cfg["org"] = org["slug"]
    cfg["client_id"] = org["client_id"]
    cfg["auth_token"] = auth_token
    return str(cfg.file)
