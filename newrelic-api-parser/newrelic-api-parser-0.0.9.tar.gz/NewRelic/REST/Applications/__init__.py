from NewRelic.Base import BaseNewRelic
from NewRelic.CustomExceptions import ArgumentException

class Applications(BaseNewRelic):

    def __init__(self, API_KEY):
        super().__init__(API_KEY)

    def get_list(self, options: dict = {}) -> dict:
        """
        fetch the apm applications for new relic
        """
        url = self.BASE_URI + '/applications.json'
        return super().get_data(url, options=options)

    def show(self, app_id: int) -> dict:
        """
        fetch single application data
        """
        url = self.BASE_URI + '/applcations/{0}.json'.format(app_id)
        return super().get_data(url)

    def delete(self, app_id: int):
        """
        fetch single application data
        """
        url = self.BASE_URI + '/applcations/{0}.json'.format(app_id)
        return super().delete(url, app_id)