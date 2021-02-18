from dataclasses import dataclass

from sym.cli.data.global_options_base import GlobalOptionsBase

from sym.flow.cli.helpers.constants import DEFAULT_API_URL, DEFAULT_AUTH_URL


@dataclass
class GlobalOptions(GlobalOptionsBase):
    api_url: str = DEFAULT_API_URL
    auth_url: str = DEFAULT_AUTH_URL

    def to_dict(self):
        return {
            "debug": self.debug,
            "api_url": self.api_url,
            "auth_url": self.auth_url,
        }
