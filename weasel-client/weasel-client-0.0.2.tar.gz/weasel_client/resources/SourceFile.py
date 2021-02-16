from __future__ import annotations

from typing import Iterator, Optional

from weasel_client.resources.Resource import Resource


class SourceFile(Resource):
    """
    Resource class for SourceFiles
    """
    _file_data = None
    _hash_sha1 = None
    _hash_sha256 = None
    _hash_md5 = None
    _hash_ssdeep = None

    def __init__(
            self,
            APIClient,
            id,
            url,
            hash_sha1,
            hash_sha256,
            hash_md5,
            hash_ssdeep
    ):
        super().__init__(APIClient=APIClient, id=id, url=url)
        self._hash_sha1 = hash_sha1
        self._hash_sha256 = hash_sha256
        self._hash_md5 = hash_md5
        self._hash_ssdeep = hash_ssdeep

    def file(self):
        """
        # Todo
        Should return the file content
        """
        pass

    def hash_sha1(self):
        """
        Returns the sha1-hash in HEX format
        """
        return self._hash_sha1

    def hash_sha256(self):
        """
        Returns the sha256-hash in HEX format
        """
        return self._hash_sha256

    def hash_md5(self):
        """
        Returns the md5-hash in HEX format
        """
        return self._hash_md5

    def hash_ssdeep(self):
        """
        Returns the ssdeep-hash
        """
        return self._hash_ssdeep

    def releases(self) -> Iterator[Resource]:
        """
        Returns the associated releases
        """
        yield from self._client.sourcefile_releases(pk=self._id)

    @staticmethod
    def by_hash(APIClient, type: str, hash: str) -> Iterator[SourceFile]:
        """
        Fetches a SourceFile-object with a given hash
        :param APIClient: client for API-requests
        :param type: md5|sha1|sha256|ssdeep
        :param hash: hash in HEX format
        """
        return APIClient.sourcefile_byhash(type=type, hash=hash)

    @staticmethod
    def by_id(APIClient, id: int) -> Optional[SourceFile]:
        """
        Fetches a SourceFile-object with a given ID
        :param APIClient: client for API-requests
        :param id: id of the object to fetch
        """
        return APIClient.sourcefile_detail(pk=id)
