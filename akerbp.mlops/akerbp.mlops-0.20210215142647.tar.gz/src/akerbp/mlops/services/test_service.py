"""
test_service.py

Generic test for services (training or prediction)
"""
import os
import sys
from importlib import import_module

from akerbp.mlops.core import config, logger
locals().update(config.getenv.__dict__)
logging=logger.get_logger(name='MLOps')


api_keys = config.api_keys

def mock_saver(*args, **kargs):
    pass


def test_service(model_name):
   logging.info(f"Test {service_name} service")
   # Add deployment folder to path so that service can load the settings file
   sys.path.append(os.getcwd())
   service = import_module(f"akerbp.mlops.services.{service_name}").service
   c = config.get_model_config(model_name)
   
   if service_name == 'training':
      response = service(data=c.input, secrets=api_keys, saver=mock_saver)
   elif service_name == 'prediction':
      response = service(data=c.input, secrets=api_keys)
   else:
      raise Exception("Unknown service name")
   
   assert response['status'] == 'ok'
   assert c.check(response[service_name])
   