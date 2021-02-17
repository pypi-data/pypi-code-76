#    COPYRIGHT © 2017. TCPIP.
#    PATENT PENDING. ALL RIGHTS RESERVED.
#    SPEI GATEWAY IS REGISTERED TRADEMARKS OF TCPIP.
#
#    This software is confidential and proprietary information of TCPIP.
#    You shall not disclose such Confidential Information and shall use it only
#    in accordance with the company policy.

# coding: utf-8

"""
     <i>Fecha de creación: 5 de diciembre, 2019</i>

     author: Saintiago García
     version: 1.0
"""

from enum import Enum


class EnvironmentEnum(Enum):
    __order__ = 'SANDBOX DEVELOPMENT PRODUCTION'

    SANDBOX = 'https://sandbox-api.wire4.mx/token', 'https://sandbox-api.wire4.mx/wire4/1.0.0'

    DEVELOPMENT = 'https://development-api.wire4.mx/token', 'https://development-api.wire4.mx/wire4/1.0.0'

    PRODUCTION = 'https://api.wire4.mx/token', 'https://api.wire4.mx/wire4/1.0.0'

    def __new__(cls, token_url, service_url):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj.token_url = token_url
        obj.service_url = service_url
        obj._value_ = value
        return obj
