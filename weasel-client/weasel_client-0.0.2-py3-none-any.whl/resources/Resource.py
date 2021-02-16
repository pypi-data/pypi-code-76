from typing import Optional


class Resource:
    """
    Base class for resources fetched from the WEASEL-API
    """
    _client = None
    _id: Optional[int]
    _url: Optional[str]

    def __init__(self, APIClient, id: Optional[int] = None, url: Optional[str] = None):
        self._client = APIClient
        self._id = id
        self._url = url

    def id(self) -> Optional[int]:
        """
        Returns the ID
        """
        return self._id

    def pk(self) -> Optional[int]:
        """
        Alias for id
        """
        return self.id()

    def url(self) -> Optional[str]:
        """
        Returns the detail-endpoint URL of the resource
        """
        return self._url
