#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

import os
import logging

import OpenSSL

logger = logging.getLogger(__name__)

# _SECURITY_OUTPUT_DIR = os.path.join(get_tool_dir(), 'security')
#
# _SECURITY_CERT_NAME = 'oem-client.pem'
# _SECURITY_PUB_NAME = 'public_key.pem'
# _SECURITY_KEY_NAME = 'private_key.pem'
#
# _SECURITY_CERT_PATH = os.path.join(_SECURITY_OUTPUT_DIR, _SECURITY_CERT_NAME)
# _SECURITY_PUB_PATH = os.path.join(_SECURITY_OUTPUT_DIR, _SECURITY_PUB_NAME)
# _SECURITY_KEY_PATH = os.path.join(_SECURITY_OUTPUT_DIR, _SECURITY_KEY_NAME)
#
# _SERVER_MERGED_CERT = os.path.join(_SECURITY_OUTPUT_DIR, '.server.cred.pem')


# def keys_exist(output=_SECURITY_OUTPUT_DIR):
#     """ Checks a key pair. """
#     pub_file = os.path.join(output, _SECURITY_PUB_NAME)
#     key_file = os.path.join(output, _SECURITY_KEY_NAME)
#
#     logger.debug("Checking the keys:\n%s\n%s", pub_file, key_file)
#     if os.path.isfile(pub_file) and os.path.isfile(key_file):
#         return True
#
#     return False
#
#
# def check_private_public_key_pair(pem_pub, pem_pri) -> bool:
#     try:
#         private_key_obj = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, pem_pri)
#     except OpenSSL.crypto.Error:
#         raise RuntimeError('private key is not correct')
#
#     try:
#         cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_pub)
#     except OpenSSL.crypto.Error:
#         raise Exception('Certificate is not correct: %s' % pem_pub)
#
#     context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
#     context.use_privatekey(private_key_obj)
#     context.use_certificate(cert_obj)
#     try:
#         context.check_privatekey()
#         return True
#     except OpenSSL.SSL.Error:
#         return False
#
#
# def merge_certs(cert, key):
#     """ Appends a private key to certs. """
#     with open(cert, "rb") as c, open(key, "rb") as k:
#         cert_cont = c.read()
#         key_cont = k.read()
#
#     if not check_private_public_key_pair(cert_cont, key_cont):
#         raise RuntimeError('Certificate public key is not derived from the private key')
#
#     return cert, key
