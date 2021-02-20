import rdflib
import requests
import yaml

from acdh_arche_pyutils.utils import (
    camel_to_snake,
    create_query_sting
)


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
        self.rest = self.description['rest']
        self.schema = self.description['schema']
        self.base_url = self.rest['urlBase']
        self.path_base = self.rest['pathBase']
        self.fetched_endpoint = f"{self.base_url}{self.path_base}"
        for key, value in self.schema.items():
            if isinstance(value, str):
                setattr(self, camel_to_snake(key), value)
        for key, value in self.schema['classes'].items():
            if isinstance(value, str):
                setattr(self, camel_to_snake(key), value)

    def top_col_ids(self):
        """returns of list of tuples (hasIdentifier, hasTitle) of all TopCollection"""
        query_params = {
            "property[0]": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "value[0]": self.top_collection,
            "readMode": 'ids'
        }
        query_string = create_query_sting(query_params)
        r = requests.get(f"{self.fetched_endpoint}search?{query_string}")
        g = rdflib.Graph().parse(data=r.text, format='ttl')
        items = [
            (
                str(x[0]),
                str(x[1])
            ) for x in g.subject_objects(predicate=rdflib.URIRef(self.label))
        ]
        return items
