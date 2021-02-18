# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-07 15:54

@author: johannes

"""
from sharkvalidator.validators.validator import Validator, ValidatorLog
from sharkvalidator.utils import deep_get


class ElementValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, delivery, **kwargs):
        report = {'disapproved': {}} if kwargs.get('disapproved_only') else {'approved': {}, 'disapproved': {}}

        element_list = deep_get(self.data_types, [delivery.data_type, 'element_list']) or []

        for element in element_list:
            if delivery[element].empty:
                report['disapproved'].setdefault(element, 'Missing!')
            else:
                if not kwargs.get('disapproved_only'):
                    report['approved'].setdefault(element, 'All good!')

        ValidatorLog.update_info(
            delivery_name=delivery.name,
            validator_name=self.name,
            info=report,
        )
