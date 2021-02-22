#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from . import Util
from typing import Literal
filepath = os.path.dirname(__file__)


class ConfigError(Exception):
    pass


class Config(object):
    user = {}
    software = {}
    verifySSL = ''
    validateAPIScheme = True
    validateDataScheme = True
    requestTimeout = 60
    apiversion = '3.0'  # Only 3.0 supported
    live = False
    compression = True

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def URL(self):
        if self.live:
            return f'https://api.onlineszamla.nav.gov.hu/invoiceService/v{self.apiversion[0]}/'
        return f'https://api-test.onlineszamla.nav.gov.hu/invoiceService/v{self.apiversion[0]}/'

    def ns(self, val: Literal['api', 'base', 'common', 'data']):
        if val == 'common':
            return '{http://schemas.nav.gov.hu/NTCA/1.0/common}'
        return f'{{http://schemas.nav.gov.hu/OSA/{self.apiversion}/{val}}}'

    def revxsdns(self, val: str):
        if val == 'http://schemas.nav.gov.hu/NTCA/1.0/common':
            return 'common.xsd'
        if val == f'http://schemas.nav.gov.hu/OSA/{self.apiversion}/base':
            return 'invoiceBase.xsd'
        return NotImplemented

    @property
    def dataXsdFile(self) -> str:
        return os.path.join(filepath, 'xsd', self.apiversion, 'invoiceData.xsd')

    @property
    def apiXsdFile(self) -> str:
        return os.path.join(filepath, 'xsd', self.apiversion, 'invoiceApi.xsd')

    @property
    def annulmentXsdFile(self) -> str:
        return os.path.join(filepath, 'xsd', self.apiversion, 'invoiceAnnulment.xsd')

    @property
    def passwordHash(self) -> str:
        return Util.sha512(self.user['password'])

    @passwordHash.setter
    @passwordHash.deleter
    @URL.setter
    @URL.deleter
    @dataXsdFile.setter
    @dataXsdFile.deleter
    @apiXsdFile.setter
    @apiXsdFile.deleter
    @annulmentXsdFile.setter
    @annulmentXsdFile.deleter
    def passer(self, *args, **kwargs):
        raise NotImplementedError("Function not implemented")


__all__ = ['Config', 'ConfigError']
