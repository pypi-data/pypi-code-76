import requests
import yaml


class ArcheApiClient():
    """Main Class to interact with ARCHE-API """

    def __init__(
        self,
        arche_endpoint
    ):
        """ initializes the class
        :param arche_endpoint: The ARCHE endpoint e.g. `https://arche-dev.acdh-dev.oeaw.ac.at/api/`
        :type endpoint: str

        :return: A ArcheApiClient instance
        :rtype: class:`achd_arch_pyutils.client.ArcheApiClient`
        """
        super().__init__()
        self.endpoint = arche_endpoint
        self.describe_url = f"{arche_endpoint}describe"
        self.info = requests.get(self.describe_url)
        self.description = yaml.load(self.info.text, Loader=yaml.FullLoader)
