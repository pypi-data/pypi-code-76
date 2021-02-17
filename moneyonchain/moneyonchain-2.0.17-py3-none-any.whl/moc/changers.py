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
from moneyonchain.governance import Governor


class MoCSettlementChanger(BaseChanger):

    contract_name = 'MoCSettlementChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlementChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlementChanger.bin'))

    mode = 'RDoC'

    def constructor(self, input_block_span, execute_change=False, **tx_arguments):

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
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MoCPriceProviderChanger(BaseChanger):
    contract_name = 'MoCPriceProviderChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.bin'))

    mode = 'MoC'

    def constructor(self, price_provider, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCState']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, Web3.toChecksumAddress(price_provider), **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MoCSetCommissionMocProportionChanger(BaseChanger):

    contract_name = 'DexAddTokenPairChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionMocProportionChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionMocProportionChanger.bin'))

    mode = 'MoC'

    def constructor(self, moc_proportion, commission_splitter=None, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        if not commission_splitter:
            commission_splitter = self.network_manager.options['networks'][config_network]['addresses']['CommissionSplitter']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(Web3.toChecksumAddress(commission_splitter), moc_proportion, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MoCSetCommissionFinalAddressChanger(BaseChanger):
    contract_name = 'MoCSetCommissionFinalAddressChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionFinalAddressChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionFinalAddressChanger.bin'))

    mode = 'MoC'

    def constructor(self, commission_address, commission_splitter=None, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        if not commission_splitter:
            commission_splitter = self.network_manager.options['networks'][config_network]['addresses']['CommissionSplitter']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(commission_splitter),
            Web3.toChecksumAddress(commission_address),
            **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MoCInrateCommissionsAddressChanger(BaseChanger):
    contract_name = 'MoCInrateCommissionsAddressChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionsAddressChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionsAddressChanger.bin'))

    mode = 'MoC'

    def constructor(self, commission_address, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(contract_address),
            Web3.toChecksumAddress(commission_address),
            **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MoCInrateRiskProRateChangerChanger(BaseChanger):
    contract_name = 'MoCInrateRiskProRateChangerChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrateRiskProRateChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrateRiskProRateChanger.bin'))

    mode = 'MoC'

    def constructor(self, bitpro_rate, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(contract_address),
            bitpro_rate,
            **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MocInrateBitProInterestChanger(BaseChanger):
    contract_name = 'MocInrateBitProInterestChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateBitProInterestChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateBitProInterestChanger.bin'))

    mode = 'MoC'

    def constructor(self, bitpro_blockspan, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(contract_address),
            bitpro_blockspan,
            **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MocInrateBtcxInterestChanger(BaseChanger):
    contract_name = 'MocInrateBtcxInterestChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateBtcxInterestChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateBtcxInterestChanger.bin'))

    mode = 'MoC'

    def constructor(self, btxc_tmin, btxc_tmax, btxc_power, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(contract_address),
            btxc_tmin,
            btxc_tmax,
            btxc_power,
            **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MocInrateDocInterestChanger(BaseChanger):
    contract_name = 'MocInrateDocInterestChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateDocInterestChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateDocInterestChanger.bin'))

    mode = 'MoC'

    def constructor(self, doc_tmin, doc_tmax, doc_power, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(
            Web3.toChecksumAddress(contract_address),
            doc_tmin,
            doc_tmax,
            doc_power,
            **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MocStateMaxMintBProChanger(BaseChanger):

    contract_name = 'DexTokenPairDisabler'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocStateMaxMintBProChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocStateMaxMintBProChanger.bin'))

    mode = 'MoC'

    def constructor(self, max_mint_bpro, execute_change=False, **tx_arguments):

        config_network = self.network_manager.config_network
        contract_address = self.network_manager.options['networks'][config_network]['addresses']['MoCState']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(contract_address, max_mint_bpro, **tx_arguments)

        tx_receipt.info()
        tx_receipt.info_to_log()

        self.log.info("Deployed contract done!")
        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))

        if execute_change:
            self.log.info("Executing change....")
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt


class MocMakeStoppableChanger(BaseChanger):

    contract_name = 'MocMakeStoppableChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocMakeStoppableChanger.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocMakeStoppableChanger.bin'))

    mode = 'MoC'

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
            governor = Governor(self.network_manager).from_abi()
            tx_receipt = governor.execute_change(tx_receipt.contract_address, **tx_arguments)
            self.log.info("Change successfull!")

        return tx_receipt

