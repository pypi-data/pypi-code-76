from __future__ import annotations

from datetime import datetime, date
from typing import Iterator

from weasel_client.resources.Resource import Resource


class DateStatistics(Resource):
    """
    Resource class for DateStatistics
    """
    _date: str

    def __init__(
            self,
            APIClient,
            date: str
    ):
        super().__init__(APIClient=APIClient)
        self._date = date

    def date(self) -> datetime:
        """
        Returns the date-attribute
        """
        return datetime.fromisoformat(self._date)

    def results(self) -> Iterator[Resource]:
        """
        Returns /installations/<date>/ for the object's date
        """
        yield from self._client.installations_list(date=self._date)

    @staticmethod
    def from_date(APIClient, date: date) -> DateStatistics:
        """
        Creates a DateStatistics-object with a given date
        :param APIClient: client to for API-Requests
        :param date: date for the DateStatistics-object
        """
        return DateStatistics(APIClient=APIClient, date=date.isoformat())
