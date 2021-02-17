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
from moneyonchain.governance import Governor, RDOCGovernor


class PriceFeederWhitelistChanger(BaseChanger):
    contract_name = 'PriceFeederWhitelistChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederWhitelist.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederWhitelist.bin'))

    mode = 'MoC'

    def constructor(self,
                    contract_address_price_feed,
                    contract_address_medianizer=None,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        if not contract_address_medianizer:
            contract_address_medianizer = self.network_manager.options['networks'][config_network]['addresses']['oracle']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(Web3.toChecksumAddress(contract_address_medianizer),
                                 Web3.toChecksumAddress(contract_address_price_feed),
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


class RDOCPriceFeederWhitelistChanger(BaseChanger):
    contract_name = 'RDOCPriceFeederWhitelistChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederWhitelist.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederWhitelist.bin'))

    mode = 'RDoC'

    def constructor(self,
                    contract_address_price_feed,
                    contract_address_medianizer=None,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        if not contract_address_medianizer:
            contract_address_medianizer = self.network_manager.options['networks'][config_network]['addresses']['oracle']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(Web3.toChecksumAddress(contract_address_medianizer),
                                 Web3.toChecksumAddress(contract_address_price_feed),
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


class PriceFeederAdderChanger(BaseChanger):
    contract_name = 'PriceFeederAdderChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederAdder.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederAdder.bin'))

    mode = 'MoC'

    def constructor(self,
                    account_owner,
                    contract_address_medianizer=None,
                    contract_address_feedfactory=None,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        if not contract_address_medianizer:
            contract_address_medianizer = self.network_manager.options['networks'][config_network]['addresses']['oracle']
        if not contract_address_feedfactory:
            contract_address_feedfactory = self.network_manager.options['networks'][config_network]['addresses']['FeedFactory']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(Web3.toChecksumAddress(contract_address_feedfactory),
                                 Web3.toChecksumAddress(contract_address_medianizer),
                                 Web3.toChecksumAddress(account_owner),
                                 **tx_arguments)

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


class RDOCPriceFeederAdderChanger(BaseChanger):
    contract_name = 'RDOCPriceFeederAdderChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederAdder.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederAdder.bin'))

    mode = 'RDoC'

    def constructor(self,
                    account_owner,
                    contract_address_medianizer=None,
                    contract_address_feedfactory=None,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        if not contract_address_medianizer:
            contract_address_medianizer = self.network_manager.options['networks'][config_network]['addresses']['oracle']
        if not contract_address_feedfactory:
            contract_address_feedfactory = self.network_manager.options['networks'][config_network]['addresses']['FeedFactory']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(Web3.toChecksumAddress(contract_address_feedfactory),
                                 Web3.toChecksumAddress(contract_address_medianizer),
                                 Web3.toChecksumAddress(account_owner),
                                 **tx_arguments)

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


class PriceFeederRemoverChanger(BaseChanger):
    contract_name = 'PriceFeederRemoverChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederRemover.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederRemover.bin'))

    mode = 'MoC'

    def constructor(self,
                    contract_address_price_feed,
                    contract_address_medianizer=None,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        if not contract_address_medianizer:
            contract_address_medianizer = self.network_manager.options['networks'][config_network]['addresses']['oracle']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(Web3.toChecksumAddress(contract_address_medianizer),
                                 Web3.toChecksumAddress(contract_address_price_feed),
                                 **tx_arguments)

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


class RDOCPriceFeederRemoverChanger(BaseChanger):
    contract_name = 'RDOCPriceFeederRemoverChanger'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederRemover.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederRemover.bin'))

    mode = 'RDoC'

    def constructor(self,
                    contract_address_price_feed,
                    contract_address_medianizer=None,
                    execute_change=False,
                    **tx_arguments):

        config_network = self.network_manager.config_network
        if not contract_address_medianizer:
            contract_address_medianizer = self.network_manager.options['networks'][config_network]['addresses']['oracle']

        self.log.info("Deploying new contract...")

        tx_receipt = self.deploy(Web3.toChecksumAddress(contract_address_medianizer),
                                 Web3.toChecksumAddress(contract_address_price_feed),
                                 **tx_arguments)

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
