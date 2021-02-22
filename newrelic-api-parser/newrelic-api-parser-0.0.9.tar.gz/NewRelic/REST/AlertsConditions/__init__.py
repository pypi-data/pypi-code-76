from NewRelic.Base import BaseNewRelic

class AlertsConditions(BaseNewRelic):

    def __init__(self, API_KEY):
        super().__init__(API_KEY)

    def get_list(self, policy_id: int, options: dict = {}) -> dict:
        """
        fetch the alert conditions for new relic
        """
        options['policy_id'] = policy_id
        url = self.BASE_URI + '/alerts_conditions.json'
        return super().get_data(url, options=options)