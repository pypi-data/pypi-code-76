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
from moneyonchain.moc import MoCState


class VENDORSMoCState(MoCState):
    contract_name = 'MoCState'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCState.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCState.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def moc_price(self,
                  formatted: bool = True,
                  block_identifier: BlockIdentifier = 'latest'):
        """MoC price in USD.
        NOTE: This call have a required if the price is valid, so it can fail.
        """

        if self.mode == 'MoC':
            result = self.sc.getMoCPrice(block_identifier=block_identifier)
        else:
            raise NotImplementedError('Only supported in MoC mode')

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def moc_price_provider(self,
                           block_identifier: BlockIdentifier = 'latest'):
        """MoC Price provider address"""

        if self.mode == 'MoC':
            result = self.sc.getMoCPriceProvider(block_identifier=block_identifier)
        else:
            raise NotImplementedError('Only supported in MoC mode')

        return result

    def moc_token(self,
                  block_identifier: BlockIdentifier = 'latest'):
        """MoC token address"""

        if self.mode == 'MoC':
            result = self.sc.getMoCToken(block_identifier=block_identifier)
        else:
            raise NotImplementedError('Only supported in MoC mode')

        return result

    def moc_vendors(self,
                    block_identifier: BlockIdentifier = 'latest'):
        """MoC Vendor address"""

        if self.mode == 'MoC':
            result = self.sc.getMoCVendors(block_identifier=block_identifier)
        else:
            raise NotImplementedError('Only supported in MoC mode')

        return result

    def max_mint_bpro_available(self,
                                formatted: bool = True,
                                block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == 'MoC':
            raise Exception('DEPRECATED')
        else:
            result = self.sc.maxMintRiskProAvalaible(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def protected(self,
                  formatted: bool = True,
                  block_identifier: BlockIdentifier = 'latest'):
        """protected"""

        result = self.sc.getProtected(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def liquidation_enabled(self,
                            block_identifier: BlockIdentifier = 'latest'):
        """liquidation enabled"""

        result = self.sc.getLiquidationEnabled(block_identifier=block_identifier)

        return result
