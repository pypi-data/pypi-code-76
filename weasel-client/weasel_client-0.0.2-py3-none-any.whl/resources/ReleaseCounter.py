from datetime import datetime
from typing import Optional

from weasel_client.resources.Resource import Resource


class ReleaseCounter(Resource):
    """
    Resource class for ReleaseCounter
    """
    _release: int
    _observed_day: str
    _count: int

    def __init__(
            self,
            APIClient,
            release: int,
            observed_day: str,
            count: int
    ):
        super().__init__(APIClient=APIClient)
        self._release = release
        self._observed_day = observed_day
        self._count = count

    def release(self) -> Optional[Resource]:
        """
        Returns the associated release
        """
        return self._client.release_detail(pk=self._release)

    def observed_day(self) -> datetime:
        """
        Returns the associated date
        """
        return datetime.fromisoformat(self._observed_day)

    def count(self) -> int:
        """
        Returns the count
        :return:
        """
        return self._count
