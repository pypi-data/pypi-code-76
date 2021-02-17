#    COPYRIGHT © 2017. TCPIP.
#    PATENT PENDING. ALL RIGHTS RESERVED.
#    SPEI GATEWAY IS REGISTERED TRADEMARKS OF TCPIP.
#
#    This software is confidential and proprietary information of TCPIP.
#    You shall not disclose such Confidential Information and shall use it only
#    in accordance with the company policy.

# coding: utf-8

"""
     <i>Fecha de creación: 9 de diciembre, 2019</i>

     author: Saintiago García
     version: 1.0
"""
import hashlib
import hmac


class UtilsCompute:
    DEFAULT_ENCODING: str = 'utf8'

    @staticmethod
    def compare_webhook_msg_signatures(message: str, key: str, header_signature: str) -> bool:
        byte_array = bytearray(key, UtilsCompute.DEFAULT_ENCODING)
        sign = hmac.new(byte_array, message.encode(), hashlib.sha512).hexdigest()

        return sign == header_signature
