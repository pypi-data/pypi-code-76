import importlib
import os
import subprocess
import sys
from typing import Any, Dict, Optional, cast

import typer
from loguru import logger
import yaml

from commandfrog.drivers.driver import Driver
from commandfrog.drivers.ssh import SSHHost
from commandfrog.drivers.local import LocalHost
from commandfrog.drivers.docker import DockerHost
from commandfrog.config import Config



def main(host: str, deploy: str, config: str = None):
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    )

    host_ob: Driver
    config_ob = get_config_ob_from_path(config)

    if host == "@local":
        host_ob = LocalHost(config=config_ob)
    elif host.startswith("@docker/"):
        docker_item_id = host[len("@docker/"):]
        if subprocess.run(f"docker image inspect {docker_item_id} > /dev/null", shell=True).returncode == 0:
            host_ob = DockerHost(image_id=docker_item_id, config=config_ob)
        elif subprocess.run(f"docker container inspect {docker_item_id} > /dev/null", shell=True).returncode == 0:
            host_ob = DockerHost(container_id=docker_item_id, config=config_ob)
        else:
            raise ValueError("not image or container")
    else:
        username, hostname = host.split("@", maxsplit=1)
        host_ob = SSHHost(hostname=hostname, username=username, config=config_ob)

    # Don't assume the caller has a real Python environment setup (they may be calling
    # from the PyInstaller package), so support an arbitrary path to a Python file rather
    # than a regular Python import path.
    path, func_name = deploy.split(":")
    sys.path.insert(0, os.path.dirname(path))
    # For PyInstaller
    sys.path.append(os.path.dirname(sys.executable))

    if path.endswith(".py"):
        path = path[0:-len(".py")]
    module = importlib.import_module(os.path.basename(path))
    deploy_func  = getattr(module, func_name)

    try:
        deploy_func(host_ob)
    finally:
        # Note: for some reason, if we just do `return host_ob.disconnect()`
        # here, exception output / stack traces can get swallowed, which
        # doesn't happen if we assign to `result` and then return outside of
        # the finally clause.
        result = host_ob.disconnect()

    return result


def get_config_ob_from_path(path: Optional[str] = None) -> Config:
    if path is not None:
        if path.lower().endswith((".yaml", ".yml")):
            with open(path) as f:
                content = f.read()
            return get_config_ob_from_dict(yaml.safe_load(content))
        else:
            raise ValueError("We only support yaml config")
    else:
        return get_config_ob_from_dict({})


def get_config_ob_from_dict(dct: Dict) -> Config:
    dataclass_fields = cast(Any, Config).__dataclass_fields__

    config = Config(**{k: v for k, v in dct.items() if k in dataclass_fields})
    for k, v in dct.items():
        if k not in dataclass_fields:
            setattr(config, k, v)

    return config


if __name__ == "__main__":
    typer.run(main)
