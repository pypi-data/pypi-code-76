# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-08 13:37

@author: johannes

"""
import yaml

from sharkvalidator.writers.writer import WriterBase
from sharkvalidator.validators.validator import ValidatorLog


class ValidationWriter(WriterBase):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    @staticmethod
    def write(file_path, **kwargs):
        with open(file_path, 'w') as file:
            yaml.safe_dump(
                ValidatorLog.log,
                file,
                indent=4,
                width=120,
                default_flow_style=False,
            )
