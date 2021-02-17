"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

from web3 import Web3

from moneyonchain.events import BaseEvent


class MoCExchangeRiskProMint(BaseEvent):

    name = "RiskProMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'Amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCExchangeRiskProWithDiscountMint(BaseEvent):
    name = "RiskProWithDiscountMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'riskProTecPrice', 'riskProDiscountPrice', 'amount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['riskProTecPrice'] = Web3.fromWei(self.event['riskProTecPrice'], 'ether')
        d_event['riskProDiscountPrice'] = Web3.fromWei(self.event['riskProDiscountPrice'], 'ether')
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                format(float(d_event['riskProTecPrice']), '.18f'),
                format(float(d_event['riskProDiscountPrice']), '.18f'),
                format(float(d_event['amount']), '.18f')]


class MoCExchangeRiskProRedeem(BaseEvent):
    name = "RiskProRedeem"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCExchangeStableTokenMint(BaseEvent):
    name = "StableTokenMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCExchangeStableTokenRedeem(BaseEvent):
    name = "StableTokenRedeem"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCExchangeFreeStableTokenRedeem(BaseEvent):
    name = "FreeStableTokenRedeem"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'Amount', 'ReserveTotal', 'Commission', 'Interests', 'ReservePrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['interests'] = Web3.fromWei(self.event['interests'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['interests']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCExchangeRiskProxMint(BaseEvent):
    name = "RiskProxMint"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Bucket', 'Account', 'Amount', 'Reserve Total', 'Interests',  'Leverage',  'Commission',  'Reserve Price']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['bucket'] = self.event['bucket']
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['interests'] = Web3.fromWei(self.event['interests'], 'ether')
        d_event['leverage'] = Web3.fromWei(self.event['leverage'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['bucket'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['interests']), '.18f'),
                format(float(d_event['leverage']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCExchangeRiskProxRedeem(BaseEvent):
    name = "RiskProxRedeem"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Bucket', 'Account', 'Amount', 'Reserve Total', 'Interests',  'Leverage',  'Commission',  'Reserve Price']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['bucket'] = self.event['bucket']
        d_event['account'] = self.event['account']
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['reserveTotal'] = Web3.fromWei(self.event['reserveTotal'], 'ether')
        d_event['interests'] = Web3.fromWei(self.event['interests'], 'ether')
        d_event['leverage'] = Web3.fromWei(self.event['leverage'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['bucket'],
                d_event['account'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['reserveTotal']), '.18f'),
                format(float(d_event['interests']), '.18f'),
                format(float(d_event['leverage']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


# SETTLEMENT

class MoCSettlementRedeemRequestProcessed(BaseEvent):
    name = "RedeemRequestProcessed"

    @staticmethod
    def columns():
        columns = ['Block Nº',  'Timestamp', 'Account', 'Commission', 'Amount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['redeemer'] = self.event['redeemer']
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['redeemer'],
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['amount']), '.18f')]


class MoCSettlementSettlementRedeemStableToken(BaseEvent):
    name = "SettlementRedeemStableToken"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'queueSize', 'accumCommissions', 'reservePrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['queueSize'] = self.event['queueSize']
        d_event['accumCommissions'] = Web3.fromWei(self.event['accumCommissions'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['queueSize'],
                format(float(d_event['accumCommissions']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCSettlementSettlementCompleted(BaseEvent):
    name = "SettlementCompleted"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'commissionsPayed']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['commissionsPayed'] = Web3.fromWei(self.event['commissionsPayed'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                format(float(d_event['commissionsPayed']), '.18f')]


class MoCSettlementSettlementDeleveraging(BaseEvent):
    name = "SettlementDeleveraging"

    @staticmethod
    def columns():
        columns = ['Block Nº',  'Timestamp', 'leverage', 'riskProxPrice', 'reservePrice', 'startBlockNumber']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['leverage'] = Web3.fromWei(self.event['leverage'], 'ether')
        d_event['riskProxPrice'] = Web3.fromWei(self.event['riskProxPrice'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')
        d_event['startBlockNumber'] = self.event['startBlockNumber']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                format(float(d_event['leverage']), '.18f'),
                format(float(d_event['riskProxPrice']), '.18f'),
                format(float(d_event['reservePrice']), '.18f'),
                d_event['startBlockNumber']]


class MoCSettlementSettlementStarted(BaseEvent):
    name = "SettlementStarted"

    @staticmethod
    def columns():
        columns = ['Block Nº',  'Timestamp', 'stableTokenRedeemCount', 'deleveragingCount', 'riskProxPrice', 'reservePrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['stableTokenRedeemCount'] = self.event['stableTokenRedeemCount']
        d_event['deleveragingCount'] = self.event['deleveragingCount']
        d_event['riskProxPrice'] = Web3.fromWei(self.event['riskProxPrice'], 'ether')
        d_event['reservePrice'] = Web3.fromWei(self.event['reservePrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['stableTokenRedeemCount'],
                d_event['deleveragingCount'],
                format(float(d_event['riskProxPrice']), '.18f'),
                format(float(d_event['reservePrice']), '.18f')]


class MoCSettlementRedeemRequestAlter(BaseEvent):
    name = "RedeemRequestAlter"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'address', 'isAddition', 'delta']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['redeemer'] = self.event['redeemer']
        d_event['isAddition'] = self.event['isAddition']
        d_event['delta'] = Web3.fromWei(self.event['delta'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['redeemer'],
                d_event['isAddition'],
                format(float(d_event['delta']), '.18f')]


class MoCInrateDailyPay(BaseEvent):
    name = "InrateDailyPay"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'Amount', 'daysToSettlement', 'nReserveBucketC0']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['daysToSettlement'] = self.event['daysToSettlement']
        d_event['nReserveBucketC0'] = Web3.fromWei(self.event['nReserveBucketC0'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                format(float(d_event['amount']), '.18f'),
                d_event['daysToSettlement'],
                format(float(d_event['nReserveBucketC0']), '.18f')]


class MoCInrateRiskProHoldersInterestPay(BaseEvent):
    name = "RiskProHoldersInterestPay"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'Amount', 'nReserveBucketC0BeforePay']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['amount'] = Web3.fromWei(self.event['amount'], 'ether')
        d_event['nReserveBucketC0BeforePay'] = Web3.fromWei(self.event['nReserveBucketC0BeforePay'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                format(float(d_event['amount']), '.18f'),
                format(float(d_event['nReserveBucketC0BeforePay']), '.18f')]


class ERC20Transfer(BaseEvent):
    name = "Transfer"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'Value', 'From', 'To']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['value'] = Web3.fromWei(self.event['value'], 'ether')
        d_event['e_from'] = Web3.fromWei(self.event['e_from'], 'ether')
        d_event['e_to'] = Web3.fromWei(self.event['e_to'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                format(float(d_event['value']), '.18f'),
                d_event['e_from'],
                d_event['e_to']]


class ERC20Approval(BaseEvent):
    name = "Approval"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'owner', 'spender', 'value']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['owner'] = self.event['owner']
        d_event['spender'] = self.event['spender']
        d_event['value'] = Web3.fromWei(self.event['value'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['owner'],
                d_event['spender'],
                format(float(d_event['value']), '.18f')]


class MoCBucketLiquidation(BaseEvent):
    name = "BucketLiquidation"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'bucket']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['bucket'] = self.event['bucket']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['bucket']
                ]


class MoCStateStateTransition(BaseEvent):
    name = "StateTransition"

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'newState']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['newState'] = self.event['newState']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['newState']
                ]
