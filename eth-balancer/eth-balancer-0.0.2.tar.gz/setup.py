# SPDX-License-Identifier: GPL-3.0-only
# © Copyright 2021 Julien Harbulot
# see: https://github.com/julien-h/python-eth-balancer
import setuptools

setuptools.setup(
    include_package_data=True, version=open("eth_balancer/resources/version").read()
)
