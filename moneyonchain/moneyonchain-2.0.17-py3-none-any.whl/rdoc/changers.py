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
from moneyonchain.contract import ContractBase
from moneyonchain.changers import BaseChanger
from moneyonchain.governance import RDOCGovernor
from moneyonchain.moc import MoCPriceProviderChanger


class RDOCMoCSettlementChanger(BaseChanger):
    contract_name = 'RDOCMoCSettlementChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlementChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlementChanger.bin'))

    mode = 'RDoC'

    def constructor(self,
                    input_block_span,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCSettlement']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, input_block_span, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = RDOCGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class RDOCMoCInrateStableChanger(BaseChanger):
    contract_name = 'RDOCMoCInrateStableChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateStableChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateStableChanger.bin'))

    mode = 'RDoC'

    def constructor(self, t_min, t_max, t_power, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, t_min, t_max, t_power, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = RDOCGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class RDOCMoCInrateRiskproxChanger(BaseChanger):
    contract_name = 'RDOCMoCInrateRiskproxChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrateRiskproxChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrateRiskproxChanger.bin'))

    mode = 'RDoC'

    def constructor(self, t_min, t_max, t_power, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, t_min, t_max, t_power, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = RDOCGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class RDOCMoCBucketContainerChanger(BaseChanger):
    contract_name = 'RDOCMoCBucketContainerChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCBucketContainerChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCBucketContainerChanger.bin'))

    mode = 'RDoC'

    def constructor(self, cobj_c0, cobj_x2, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCBProxManager']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, cobj_c0, cobj_x2, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = RDOCGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class RDOCCommissionSplitterAddressChanger(BaseChanger):
    contract_name = 'DexAddTokenPairChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionFinalAddressChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionFinalAddressChanger.bin'))

    mode = 'RDoC'

    def constructor(self, commission_address, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['CommissionSplitter']
        commission_address = Web3.toChecksumAddress(commission_address)

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, commission_address, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = RDOCGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class RDOCMoCStateMaxMintRiskProChanger(BaseChanger):
    contract_name = 'RDOCMoCStateMaxMintRiskProChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCStateMaxMintRiskProChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCStateMaxMintRiskProChanger.bin'))

    mode = 'MoC'

    def constructor(self, max_mint_riskpro, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCState']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, max_mint_riskpro, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = RDOCGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class RDOCPriceProviderChanger(MoCPriceProviderChanger):
    contract_name = 'RDOCPriceProviderChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.bin'))

    mode = 'RDoC'


class RDOCMocMakeStoppableChanger(BaseChanger):

    contract_name = 'RDOCMocMakeStoppableChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocMakeStoppableChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocMakeStoppableChanger.bin'))

    mode = 'RDOC'

    def constructor(self, stoppable=True, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoC']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, stoppable, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = RDOCGovernor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt
