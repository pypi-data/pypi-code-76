from __future__ import annotations

from datetime import datetime
from typing import Optional, Iterator

from weasel_client.resources.Resource import Resource


class Release(Resource):
    """
    Resource class for releases
    """
    _technology: Resource
    _version: str
    _prev_release: int = None
    _published: str

    def __init__(
            self,
            APIClient,
            id: int,
            url: str,
            technology: Resource,
            version: str,
            published: str,
            prev_release: int = None
    ):
        super().__init__(APIClient=APIClient, id=id, url=url)
        self._technology = technology
        self._version = version
        self._prev_release = prev_release
        self._published = published

    def technology(self) -> Resource:
        """
        Returns the release's technology
        """
        return self._technology

    def version(self) -> str:
        """
        Returns the release's version string
        """
        return self._version

    def prev_release(self) -> Optional[Release]:
        """
        Returns the release's previous release
        """
        if self._prev_release is not None:
            return self._client.release_detail(pk=self._prev_release)
        else:
            return None

    def published(self) -> datetime:
        """
        Returns the release's published timestamp
        :return:
        """
        return datetime.fromisoformat(self._published)

    def zipfile(self):
        """
        # Todo
        Should return the zipfile
        """
        pass

    def filelist(self) -> Iterator[Resource]:
        """
        Returns /releases/<release-ID>/filelist/ for the current release
        """
        yield from self._client.sourcefile_list(pk=self._id)

    def installations(self) -> Iterator[Resource]:
        """
        Returns /releases/<release-ID>/installations/ for the current release
        """
        yield from self._client.release_installations(pk=self._id)

    def vulnerabilities(self) -> Iterator[Resource]:
        """
        Returns /releases/<release-ID>/vulnerabilities/ for the current release
        """
        yield from self._client.release_vulnerabilities(pk=self._id)

    @staticmethod
    def from_id(APIClient, id: int) -> Optional[Release]:
        """
        Fetches a release-object with a given ID
        :param APIClient: client for API-requests
        :param id: id of the object to fetch
        """
        return APIClient.release_detail(pk=id)
