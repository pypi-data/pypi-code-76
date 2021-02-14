from contextlib import contextmanager
from unittest.mock import patch

from w.services.abstract_service import AbstractService


def get_target(config):
    return config["service"].get_patch_target(config["method_name"])


@contextmanager
def mock_services(mock_configs):
    """
    Patch services methods calls

    Args:
        mock_configs(list): list of mock config
            config = [{
              "service": <service>
              "method_name": <method to patch>,
              "return_value": <return value>
              "side_effect": [<return value>]
            }]

    Returns:
        dict: {<method_name>: mocks, ...}
    """
    patchers = []
    mocks = {}
    for config in mock_configs:
        patcher = patch(get_target(config))
        mock = patcher.start()
        if "return_value" in config:
            mock.return_value = config["return_value"]
        if "side_effect" in config:
            mock.side_effect = config["side_effect"]
        mocks[config["method_name"]] = mock
        patchers.append(patcher)

    yield mocks

    for patcher in patchers:
        patcher.stop()


@contextmanager
def mock_service(
    service: AbstractService, method_name: str, return_value=None, side_effect=None
):
    """
    Patch a service method calls
    """
    params = {"target": get_target({"service": service, "method_name": method_name})}
    # not None for Boolean return
    if return_value is not None:
        params["return_value"] = return_value
    elif side_effect:
        params["side_effect"] = side_effect
    else:
        raise RuntimeError("Missing 'return_value' or 'side_effect'")
    with patch(**params) as m:
        yield m
