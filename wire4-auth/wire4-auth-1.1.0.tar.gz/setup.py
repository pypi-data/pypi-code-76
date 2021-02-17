# coding: utf-8
#    COPYRIGHT © 2017. TCPIP.
#    PATENT PENDING. ALL RIGHTS RESERVED.
#    SPEI GATEWAY IS REGISTERED TRADEMARKS OF TCPIP.
#
#    This software is confidential and proprietary information of TCPIP.
#    You shall not disclose such Confidential Information and shall use it only
#    in accordance with the company policy.



"""
     <i>Fecha de creación: 9 de diciembre, 2019</i>

     author: Saintiago García
     version: 1.0
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "wire4-auth"
VERSION = "1.1.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["requests_oauthlib >= 1.3"]

setup(
    name=NAME,
    version=VERSION,
    description="Wire4Authenticator",
    author="Wire4",
    author_email="speiok-team@tcpip.tech",
    url="http://wire4.mx",
    keywords=["Swagger", "Wire4Authenticator"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Herramienta para autenticación de la API de Wire4  # noqa: E501
    """
)
