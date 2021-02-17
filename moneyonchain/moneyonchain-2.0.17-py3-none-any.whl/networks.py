"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""


from brownie import web3
from moneyonchain.main import accounts, rpc, history, chain
from moneyonchain.network_manager import NetworkManager

network_manager = NetworkManager()

__all__ = ["accounts", "chain", "history", "rpc", "web3", "network_manager", "NetworkManager"]

