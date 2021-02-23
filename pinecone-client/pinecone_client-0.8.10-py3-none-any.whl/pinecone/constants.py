#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import os
from pinecone.utils import get_version


__all__ = ["CLIENT_VERSION", "Config"]

PACKAGE_VERSION = get_version()
CLIENT_VERSION = "0.1"


class _CONFIG:
    def __init__(self):
        self.reset()

    def reset(self, **kwargs):
        self._environment = kwargs.get("environment")
        self._api_key = kwargs.get("api_key")
        self._controller_host = kwargs.get("controller_host")
        self._hub_host = kwargs.get("hub_host")
        self._hub_registry = kwargs.get("hub_registry")
        self._base_image = kwargs.get("base_image")

    @property
    def ENVIRONMENT(self):
        return self._environment or os.getenv("PINECONE_ENVIRONMENT") or "beta"

    @property
    def API_KEY(self):
        return self._api_key or os.getenv("PINECONE_API_KEY")

    @property
    def CONTROLLER_HOST(self):
        return (
            self._controller_host
            or os.getenv("PINECONE_CONTROLLER_HOST")
            or "https://controller.{0}.pinecone.io".format(self.ENVIRONMENT)
        )

    @property
    def HUB_HOST(self):
        return (
            self._hub_host
            or os.getenv("PINECONE_HUB_HOST")
            or "https://hub-api.{0}.pinecone.io".format(self.ENVIRONMENT)
        )

    @property
    def HUB_REGISTRY(self):
        return (
            self._hub_registry
            or os.getenv("PINECONE_HUB_REGISTRY")
            or "https://hub.{0}.pinecone.io".format(self.ENVIRONMENT)
        )

    @property
    def BASE_IMAGE(self):
        return (
            self._base_image
            or os.getenv("PINECONE_BASE_IMAGE")
            or "hub.{0}.pinecone.io/pinecone/base:{1}".format(self.ENVIRONMENT, PACKAGE_VERSION)
        )


Config = _CONFIG()
