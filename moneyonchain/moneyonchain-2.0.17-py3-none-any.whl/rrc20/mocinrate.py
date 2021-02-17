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
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import ContractBase
from moneyonchain.moc import MoCInrate


class RRC20MoCInrate(MoCInrate):
    contract_name = 'MoCInrate'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrate.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrate.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'

    def stable_inrate(self,
                      formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """Parameters inrate Stable"""

        info = dict()

        result = self.sc.getStableTmax(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['StableTmax'] = result

        result = self.sc.getStablePower(block_identifier=block_identifier)
        info['StablePower'] = result

        result = self.sc.getStableTmin(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['StableTmin'] = result

        return info

    def riskprox_inrate(self,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """Parameters inrate riskprox"""

        info = dict()

        result = self.sc.getRiskProxTmax(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['RiskProxTmax'] = result

        result = self.sc.getRiskProxPower(block_identifier=block_identifier)
        info['RiskProxPower'] = result

        result = self.sc.getRiskProxTmin(block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['RiskProxTmin'] = result

        return info
