"""Minecraft Runner - A python script for working with servers.

This module is for managing the state of the container itself.
"""

from pydantic import BaseModel, Field
from typing import Iterable

from ..config import config
from ..util import shell


class Container(BaseModel):
    """A pythonic API object for interacting with a container."""

    name: str = Field(default=config["DEFAULT"].get('name'))
    image: str = Field(default=config["DEFAULT"].get('image'))
    port: int = Field(default=int(config["DEFAULT"].get('port')))

    def show(self) -> Iterable[str]:
        """Return a generator yielding lines from `podman ps` output."""
        return shell(f'podman ps -f name={self.name}')


containers = {
    name: Container(
        name=name,
        image=config[name].get('image'),
        port=int(config[name].get('port'))
    ) for name in config.sections()
}
