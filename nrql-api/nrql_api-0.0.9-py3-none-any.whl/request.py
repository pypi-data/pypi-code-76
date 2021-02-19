import uuid
import logging
from nrql_api.response import NrqlApiResponse
import time


class NrqlApiRequest:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    account = None
    api_key = None
    api_url = "https://api.newrelic.com/graphql"
    session = None

    @staticmethod
    def configure(account, api_key, session, is_debug=False, api_url="https://api.newrelic.com/graphql"):
        """
        Configure global Request class
        Args:
            account: your newrelic account
            api_key: new relic api key. Account settings -> Users and roles -> find youself
            api_url: url to new relic api. default https://api.newrelic.com/graphql
            session: aiohttp session object
            is_debug: if True then set log level to debug
        Returns: Bool

        """
        if is_debug:
            NrqlApiRequest.logger.setLevel(logging.DEBUG)
        NrqlApiRequest.account = account
        NrqlApiRequest.api_key = api_key
        NrqlApiRequest.api_url = api_url
        NrqlApiRequest.session = session
        return True

    def __init__(self, nrql_query, query_type='raw'):
        """
        Request object implements async request to nrql api.
        Args:
            nrql_query: nrql query which we want to search
        Returns:
            Responce object

        """
        self.nrql_query = nrql_query
        self.uuid = uuid.uuid4()
        self.query_type=query_type

    @property
    def to_graphql_format(self):
        """
        Create graphql format dict for sending to

        """
        query = '''
        query($account: Int!, $query_string: String!)
        {
            actor {
                account(id: $account) {
                    nrql(query: $query_string) {
                        nrql
                        totalResult
                        metadata {
                          timeWindow {
                            since
                            until
                          }
                          facets
                          messages
                        }
                        results
                    }
                }
            }
        }
        '''
        variables = {
            "account": NrqlApiRequest.account,
            "query_string": self.nrql_query
        }
        return {"query": query, "variables": variables}

    async def run_async(self):
        headers = {
            "Content-Type": "application/json",
            "API-Key": NrqlApiRequest.api_key
        }
        NrqlApiRequest.logger.info(f"{self.uuid} - Making request. with query string {self.nrql_query}..")
        start_time = time.time()
        async with NrqlApiRequest.session.post(NrqlApiRequest.api_url, headers=headers, json=self.to_graphql_format) as response:
            exec_time = time.time() - start_time
            NrqlApiRequest.logger.info(f"{self.uuid} - Get response with status={response.status} exec_time={exec_time}")
            json_body = await response.json()
            return NrqlApiResponse(
                status=response,
                json_body=json_body,
                method=response.method,
                headers=response.headers,
                content_type=response.headers,
                is_ok=response.ok,
                exec_time=exec_time,
                query_type=self.query_type
            )

