import asyncio
import logging

import jmespath
from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.http_client.apim.api_async import ApiClientAsync
from jmespath import exceptions

logger = logging.getLogger("api-service")

def create_update_data(self, api_id, api_data: dict):
        api_data_local = api_data.copy()

        if 'metadata' in api_data_local:
            for meta in api_data_local['metadata']:
                if api_id:
                    meta['apiId'] = api_id
                if 'defaultValue' in meta:
                    del meta['defaultValue']
        return api_data_local

def list(query, config, custom_function=None):

    async def get_apis():
        client = ApiClientAsync(config)
        apis = await client.get_apis_with_state()
        return apis

    loop = asyncio.get_event_loop()
    apis = loop.run_until_complete(get_apis())

    logger.debug(f"apis response: {apis}")

    try:
        if custom_function:
            return jmespath.search(
                    query,
                    apis,
                    jmespath.Options(custom_functions=custom_function)
                )
        else:
            return jmespath.search(query, apis)
    except exceptions.JMESPathError as jmespatherr:
        logging.exception("LIST JMESPathError exception")
        raise GraviteeioError(str(jmespatherr))
