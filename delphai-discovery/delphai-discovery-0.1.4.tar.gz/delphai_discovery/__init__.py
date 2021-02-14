from typing import Dict, List
import consul
import os
from grpc.aio import insecure_channel as async_insecure_channel
from grpc import Channel, insecure_channel
import httpx
import json

MAX_MESSAGE_LENGTH = 50 * 1024 * 1024


class DiscoveryException(Exception):
  pass


def __get_grpc_client(Stub, address: str, is_async: bool = True):
  options = [
    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
  ]
  if is_async:
    channel = async_insecure_channel(address, options)
  else:
    channel = insecure_channel(address, options)
  client = Stub(channel)
  return client


def get_service(api_name: str,
                stub=None,
                protocol: str = 'grpc',
                visibility: str = 'public',
                branch: str = 'master',
                delphai_environment: str = os.environ.get('DELPHAI_ENVIRONMENT') or 'staging',
                meta: dict = {},
                tags: List[str] = None,
                config: dict = {
                  'host': 'consul.delphai.xyz',
                  'port': 443,
                  'scheme': 'https'
                }):
  client = consul.Consul(**config)
  services: Dict[str, dict] = client.agent.services()
  filtered_services = []
  for service in services.values():
    include = True
    service_meta = service['Meta']
    if service_meta.get('namespace') != api_name:
      include = False
    if include:
      if not tags or len(tags) == 0:
        if service_meta.get('protocol') != protocol \
        or service_meta.get('type') != 'microservice' \
        or service_meta.get('visibility') != visibility \
        or service_meta.get('branch') != branch \
        or service_meta.get('delphaiEnvironment') != delphai_environment:
          include = False
        if include:
          for key, value in meta.items():
            if service_meta[key] != value:
              include = False
              break
      else:
        service_tags = service['Tags']
        for tag in tags:
          if tag not in service_tags:
            include = False
            break
    if include:
      filtered_services.append(service)
  if len(filtered_services) > 1:
    raise DiscoveryException('multiple services found')
  elif len(filtered_services) == 0:
    raise DiscoveryException(f'{api_name} service not found')
  found_service = filtered_services[0]
  found_address = found_service['Address']
  found_meta = found_service['Meta']
  if found_meta['protocol'] == 'grpc':
    if not stub:
      raise DiscoveryException('stub is required for grpc services')
    return __get_grpc_client(stub, found_address)
  elif found_meta['protocol'] == 'http':
    session = httpx.AsyncClient()
    session.base_url = found_address
    return session


def get_model(model_name: str,
              delphai_environment: str = 'common',
              config: dict = {
                'host': 'consul.delphai.xyz',
                'port': 443,
                'scheme': 'https'
              }):
  client = consul.Consul(**config)
  services: Dict[str, dict] = client.agent.services()
  filtered_services = []
  for service in services.values():
    service_meta = service['Meta']
    if service_meta['name'] == model_name \
    and service_meta['type'] == 'model' \
    and service_meta['delphaiEnvironment'] == delphai_environment:
      filtered_services.append(service)
  if len(filtered_services) > 1:
    raise DiscoveryException('multiple models found')
  elif len(filtered_services) == 0:
    raise DiscoveryException(f'{model_name} model not found')
  found_model = filtered_services[0]
  found_address = found_model['Address']
  found_meta = found_model['Meta']
  keys_str = client.kv.get(found_meta['name'])[1]['Value']
  keys = json.loads(keys_str)
  primary_key = keys['primaryKey']
  session = httpx.AsyncClient()
  session.base_url = found_address
  session.headers = {'Authorization': f'Bearer {primary_key}'}
  return session


async def call_model(model_name: str,
                     body: any,
                     delphai_environment: str = 'common',
                     config: dict = {
                       'host': 'consul.delphai.xyz',
                       'port': 443,
                       'scheme': 'https'
                     }):
  model = get_model(model_name, delphai_environment, config)
  async with model as client:
    response = await client.post('/', json=body)
    response.raise_for_status()
  return response.json()