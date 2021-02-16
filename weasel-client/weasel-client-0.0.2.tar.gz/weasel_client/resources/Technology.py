from weasel_client.resources.Resource import Resource


class Technology(Resource):
    _name = None
    _releases_url = None

    def __init__(self, APIClient, id, name, releases_url):
        super().__init__(APIClient=APIClient, id=id)
        self._name = name
        self._releases_url = releases_url

    def tech_name(self):
        """
        Returns the name of the technology
        """
        return self._name

    def releases(self):
        """
        Returns the associated releases
        """
        return self._client.release_tech_list(tech_name=self._name)

    def updates(self):
        """
        #Todo
        Should return the updates of the technology
        """
        pass

    @staticmethod
    def from_name(APIClient, name):
        """
        Fetches a Technology-object with a given name
        :param APIClient: client for API-requests
        :param name: name of the technology to fetch
        """
        return APIClient.technology(name=name)
