# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-16 14:03

@author: johannes

"""
from abc import ABC


class Validator(ABC):
    """
    Base class for validators.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = None
        self.delivery_name = None
        self.data_types = None
        self.format_validators = None
        self.parameters = None

    def validate(self, *args, **kwargs):
        raise NotImplementedError

    def update_attributes(self, **kwargs):
        for key, item in kwargs.items():
            setattr(self, key, item)

    @staticmethod
    def message(*args):
        print(' - '.join(args))


class ValidatorLog:
    """
    Logger for validators.

    Each validator categorizes validation in "approved" and "disapproved" validation.

    log: {
        'delivery_name':
            'validator_name': {
                approved: [],
                disapproved: [],
            },...
    ... }
    """
    log = {}

    def __init__(self, *args, **kwargs):
        if any(args):
            if 'etc' not in self.log:
                self.log['etc'] = []
            for a in args:
                self.log['etc'].append(a)

        if kwargs.get('reset_log'):
            self.log = {}

        if kwargs.get('delivery_name'):
            delivery_name = kwargs.get('delivery_name')

            if delivery_name not in self.log:
                self.log[delivery_name] = {}

            if kwargs.get('validator_name'):
                self.log[delivery_name].setdefault(
                    kwargs.get('validator_name'),
                    kwargs.get('info')
                )

    @classmethod
    def update_info(cls, *args, **kwargs):
        return cls(*args, **kwargs)
