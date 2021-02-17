"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os

from moneyonchain.contract import ContractBase
from moneyonchain.moc import MoCConnector


class VENDORSMoCConnector(MoCConnector):
    contract_name = 'MoCConnector'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConnector.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConnector.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def contracts_addresses(self):

        d_addresses = dict()
        d_addresses['MoC'] = self.sc.moc()
        d_addresses['MoCState'] = self.sc.mocState()
        d_addresses['MoCConverter'] = self.sc.mocConverter()
        d_addresses['MoCSettlement'] = self.sc.mocSettlement()
        d_addresses['MoCExchange'] = self.sc.mocExchange()
        d_addresses['MoCInrate'] = self.sc.mocInrate()
        if self.mode == 'MoC':
            d_addresses['DoCToken'] = self.sc.docToken()
            d_addresses['BProToken'] = self.sc.bproToken()
            d_addresses['MoCBProxManager'] = self.sc.bproxManager()
        else:
            d_addresses['MoCBurnout'] = self.sc.mocBurnout()
            d_addresses['DoCToken'] = self.sc.stableToken()
            d_addresses['BProToken'] = self.sc.riskProToken()
            d_addresses['MoCBProxManager'] = self.sc.riskProxManager()
            d_addresses['ReserveToken'] = self.sc.reserveToken()

        return d_addresses
