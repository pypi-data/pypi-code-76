from NewRelic.Base import BaseNewRelic
from NewRelic.CustomExceptions import ArgumentException

class KeyTransactions(BaseNewRelic):

    def __init__(self, API_KEY):
        super().__init__(API_KEY)

    def get_list(self, options: dict = {}) -> dict:
        """
        fetch the key transactions for new relic
        """
        url = self.BASE_URI + '/key_transactions.json'
        return super().get_data(url, options=options)

    def show(self, app_id: int) -> dict:
        """
        fetch single key transction data
        """
        url = self.BASE_URI + '/key_transactions/{0}.json'.format(app_id)
        return super().get_data(url)