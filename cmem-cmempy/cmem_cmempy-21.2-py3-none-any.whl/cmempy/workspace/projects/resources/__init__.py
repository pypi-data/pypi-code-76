"""API for working with several resources."""
import json

from cmem.cmempy import config
from cmem.cmempy.api import send_request


def get_resources_uri():
    """Get endpoint URI pattern for resource list."""
    path = "/workspace/projects/{}/resources"
    return config.get_di_api_endpoint() + path


def get_resources(project_name):
    """GET retrieve list of resources."""
    response = send_request(get_resources_uri().format(project_name),
                            method="GET")
    return json.loads(response.decode("utf-8"))
