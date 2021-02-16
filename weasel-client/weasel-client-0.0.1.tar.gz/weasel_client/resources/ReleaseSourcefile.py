from __future__ import annotations

from datetime import datetime
from typing import Optional, Iterator

from weasel_client.resources.Resource import Resource


class ReleaseSourcefile(Resource):
    """
    Resource class for ReleaseSourcefile
    """
    _release: int
    _sourcefile: int
    _fully_qualified_name: str

    def __init__(
            self,
            APIClient,
            release: int,
            sourcefile: int,
            fully_qualified_name: str
    ):
        super().__init__(APIClient=APIClient)
        self._release = release
        self._sourcefile = sourcefile
        self._fully_qualified_name = fully_qualified_name

    def release(self) -> Resource:
        """
        Returns the associated release
        """
        return self._client.release_detail(pk=self._release)

    def sourcefile(self) -> Resource:
        """
        Returns the associated sourcefile
        """
        return self._client.sourcefile_detail(pk=self._sourcefile)

    def fully_qualified_name(self) -> str:
        """
        Returns the fully_qualified_name of the sourcefile in the specific release
        """
        return self._fully_qualified_name
