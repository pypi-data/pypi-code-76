import os
from typing import Dict, Any

from tzlocal import get_localzone

from simio.app.config_names import AppConfig


def get_default_config() -> Dict[Any, Any]:
    return {
        AppConfig: {
            AppConfig.version: "0.1.0",
            AppConfig.autogen_swagger: True,
            AppConfig.enable_swagger: True,
            AppConfig.timezone: get_localzone(),
            AppConfig.swagger_config: {
                "config_path": os.path.join(os.getcwd(), "swagger.json"),
            },
        },
    }
