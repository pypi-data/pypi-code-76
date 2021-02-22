from NewRelic.Base import BaseNewRelic
from NewRelic.CustomExceptions import ArgumentException

class Users(BaseNewRelic):

    def __init__(self, API_KEY):
        super().__init__(API_KEY)

    def get_list(self, options = {}):
        """
        returns a list of User objects
        """
        url = self.BASE_URI + '/users.json'
        return super().get_data(url, options=options)

    def show(self, id, options = {}):
        """
        returns a User object corresponding to the ID provided
        """
        try:
            if id is None:
                raise ArgumentException
            url = self.BASE_URI + '/users/{0}.json'.format(id)
            return super().get_data(url, options=options)
        except ArgumentException as ae:
            print(ae)