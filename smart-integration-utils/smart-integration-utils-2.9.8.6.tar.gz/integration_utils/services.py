from hashlib import md5
from datetime import datetime, timedelta
from rest_framework.response import Response

from .exceptions import InvalidDateParams


class BaseStatisticSelector(object):
    selector_type: str = 'base'

    def __init__(
        self,
        data: dict,
        integration_id: int,
        admin: int,
        platform_id: str = 'prod',
        values: list = [],
    ):
        self.data = data
        self.integration_id = integration_id
        self.admin = admin
        self.platform_id = platform_id
        self.values = values

    def get_date_params(self) -> any:
        date_from = None
        date_to = None
        if self.data.get("last_week", "").lower() == 'true':
            date_to = datetime.today().strftime('%Y-%m-%d')
            last_date = datetime.today() - timedelta(days=7)
            date_from = last_date.strftime('%Y-%m-%d')
        elif self.data.get("last_3_days", "").lower() == 'true':
            date_to = datetime.today().strftime('%Y-%m-%d')
            last_date = datetime.today() - timedelta(days=3)
            date_from = last_date.strftime('%Y-%m-%d')

        elif self.data.get('date_from') and self.data.get('date_to'):
            date_to = self.data['date_to']
            date_from = self.data['date_from']

        if not date_to or not date_from:
            raise InvalidDateParams(
                {
                    "status": "error",
                    "message": "Miss date param (like last_week,last_3_days, date_from and date_to)",
                }
            )
        return date_from, date_to

    def generate_statistic_response(
        self, date_from: str, date_to: str, filename: str
    ) -> Response:
        raise NotImplementedError()

    def generate_file_name(self, date_from: str, date_to: str) -> str:
        if self.values:
            hash_ = md5(str(self.values).encode('utf-8')).hexdigest()
            filename = f'/tmp/{self.selector_type}_{self.admin}_{self.integration_id}_{hash_}{date_from}:{date_to}'
        else:
            filename = f'/tmp/{self.selector_type}_{self.admin}_{self.integration_id}_{date_from}:{date_to}'
        return filename

    def response(self) -> Response:
        date_from, date_to = self.get_date_params()
        filename = self.generate_file_name(date_from=date_from, date_to=date_to)
        return self.generate_statistic_response(
            date_from=date_from, date_to=date_to, filename=filename,
        )

