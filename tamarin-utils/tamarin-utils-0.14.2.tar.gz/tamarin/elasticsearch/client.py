from .config import HOST, PORT, USE_SSL, PROTOCOL, USER, SECRET
from elasticsearch import Elasticsearch


class ElasticSearchClient:
    client: Elasticsearch = None

    @classmethod
    def get_client(cls):
        if not ElasticSearchClient.client:
            hosts = [
                {
                    "host": HOST,
                    "port": PORT
                }
            ]
            ElasticSearchClient.client = Elasticsearch(
                hosts=hosts,
                use_ssl=USE_SSL,
                scheme=PROTOCOL,
                http_auth=(USER, SECRET) if USER else None
            )
        return ElasticSearchClient.client

    @classmethod
    def info(cls):
        if ElasticSearchClient.client:
            return ElasticSearchClient.client.info()
        return {}

    @classmethod
    def health(cls):
        if ElasticSearchClient.client:
            return ElasticSearchClient.client.cluster.health()
        return {}
