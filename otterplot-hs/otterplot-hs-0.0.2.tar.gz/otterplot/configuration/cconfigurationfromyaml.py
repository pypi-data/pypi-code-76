# -*- coding: utf-8 -*-
from otterplot.configuration.iconfiguration import IConfiguration
from typing import Dict, Any


class CConfigFromYaml(IConfiguration):
    def __init__(self, yamlcontent: Dict[Any, Any], **kwargs) -> None:
        super().__init__()
        self.content = yamlcontent

