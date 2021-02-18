# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-11 13:15

@author: johannes

"""
from sharkvalidator.validators.validator import Validator, ValidatorLog
from sharkvalidator.utils import deep_get


class EssentialValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, delivery, **kwargs):
        report = {'disapproved': {}} if kwargs.get('disapproved_only') else {'approved': {}, 'disapproved': {}}

        for element, item in delivery.items():

            parameter_list = deep_get(self.data_types, [delivery.data_type, element]) or []

            for parameter in parameter_list:
                report_key = ' - '.join((element, parameter))
                if parameter in item:
                    if item[parameter].ne('').all():
                        # not equal to ''
                        if not kwargs.get('disapproved_only'):
                            report['approved'].setdefault(report_key, 'No missing values')
                    else:
                        report['disapproved'].setdefault(report_key, 'Missing values')
                else:
                    report['disapproved'].setdefault(report_key, 'Missing parameter')

        ValidatorLog.update_info(
            delivery_name=delivery.name,
            validator_name=self.name,
            info=report,
        )
