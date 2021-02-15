# SPDX-License-Identifier: GPL-3.0-only
# © Copyright 2021 Julien Harbulot
# see: https://github.com/julien-h/python-eth-balancer
import pathlib

with pathlib.Path(__file__).parent.joinpath("resources/version").open("r") as f:
    __version__ = f.read()
