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
from web3.exceptions import BlockNotFound
import datetime

from moneyonchain.events import BaseEvent


# MoCDecentralizedExchange.sol


class DEXNewOrderAddedToPendingQueue(BaseEvent):

    name = "NewOrderAddedToPendingQueue"

    def __init__(self, event):

        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'id', 'notIndexedArgumentSoTheThingDoesntBreak']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['id'] = self.event['id']
        d_event['notIndexedArgumentSoTheThingDoesntBreak'] = self.event['notIndexedArgumentSoTheThingDoesntBreak']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['id'],
                d_event['notIndexedArgumentSoTheThingDoesntBreak']]


class DEXBuyerMatch(BaseEvent):
    name = "BuyerMatch"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'orderId', 'amountSent', 'commission', 'change', 'received',
                   'remainingAmount', 'matchPrice', 'tickNumber']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['orderId'] = self.event['orderId']
        d_event['amountSent'] = Web3.fromWei(self.event['amountSent'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['change'] = Web3.fromWei(self.event['change'], 'ether')
        d_event['received'] = Web3.fromWei(self.event['received'], 'ether')
        d_event['remainingAmount'] = Web3.fromWei(self.event['remainingAmount'], 'ether')
        d_event['matchPrice'] = Web3.fromWei(self.event['matchPrice'], 'ether')
        d_event['tickNumber'] = self.event['tickNumber']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['orderId'],
                format(float(d_event['amountSent']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['change']), '.18f'),
                format(float(d_event['received']), '.18f'),
                format(float(d_event['remainingAmount']), '.18f'),
                format(float(d_event['matchPrice']), '.18f'),
                d_event['tickNumber']
                ]


class DEXSellerMatch(BaseEvent):
    name = "SellerMatch"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'orderId', 'amountSent', 'commission', 'received', 'surplus',
                   'remainingAmount', 'matchPrice', 'tickNumber']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['orderId'] = self.event['orderId']
        d_event['amountSent'] = Web3.fromWei(self.event['amountSent'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['received'] = Web3.fromWei(self.event['received'], 'ether')
        d_event['surplus'] = Web3.fromWei(self.event['surplus'], 'ether')
        d_event['remainingAmount'] = Web3.fromWei(self.event['remainingAmount'], 'ether')
        d_event['matchPrice'] = Web3.fromWei(self.event['matchPrice'], 'ether')
        d_event['tickNumber'] = self.event['tickNumber']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['orderId'],
                format(float(d_event['amountSent']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['received']), '.18f'),
                format(float(d_event['surplus']), '.18f'),
                format(float(d_event['remainingAmount']), '.18f'),
                format(float(d_event['matchPrice']), '.18f'),
                d_event['tickNumber']
                ]


class DEXExpiredOrderProcessed(BaseEvent):
    name = "ExpiredOrderProcessed"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'orderId', 'owner', 'returnedAmount', 'commission', 'returnedCommission']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['orderId'] = self.event['orderId']
        d_event['owner'] = self.event['owner']
        d_event['returnedAmount'] = Web3.fromWei(self.event['returnedAmount'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['returnedCommission'] = Web3.fromWei(self.event['returnedCommission'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['orderId'],
                d_event['owner'],
                format(float(d_event['returnedAmount']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['returnedCommission']), '.18f')
                ]


class DEXTickStart(BaseEvent):
    name = "TickStart"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'baseTokenAddress', 'secondaryTokenAddress', 'number']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['baseTokenAddress'] = self.event['baseTokenAddress']
        d_event['secondaryTokenAddress'] = self.event['secondaryTokenAddress']
        d_event['number'] = self.event['number']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['baseTokenAddress'],
                d_event['secondaryTokenAddress'],
                d_event['number']
                ]


class DEXTickEnd(BaseEvent):
    name = "TickEnd"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'baseTokenAddress', 'secondaryTokenAddress', 'number',
                   'nextTickBlock', 'closingPrice']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['baseTokenAddress'] = self.event['baseTokenAddress']
        d_event['secondaryTokenAddress'] = self.event['secondaryTokenAddress']
        d_event['number'] = self.event['number']
        d_event['nextTickBlock'] = self.event['nextTickBlock']
        d_event['closingPrice'] = Web3.fromWei(self.event['closingPrice'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['baseTokenAddress'],
                d_event['secondaryTokenAddress'],
                d_event['number'],
                d_event['nextTickBlock'],
                format(float(d_event['closingPrice']), '.18f')
                ]


class DEXNewOrderInserted(BaseEvent):
    name = "NewOrderInserted"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'id', 'sender', 'baseTokenAddress',
                   'secondaryTokenAddress', 'exchangeableAmount', 'reservedCommission',
                   'price', 'multiplyFactor', 'expiresInTick', 'isBuy', 'orderType']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['id'] = self.event['id']
        d_event['sender'] = self.event['sender']
        d_event['baseTokenAddress'] = self.event['baseTokenAddress']
        d_event['secondaryTokenAddress'] = self.event['secondaryTokenAddress']
        d_event['exchangeableAmount'] = Web3.fromWei(self.event['exchangeableAmount'], 'ether')
        d_event['reservedCommission'] = Web3.fromWei(self.event['reservedCommission'], 'ether')
        d_event['price'] = Web3.fromWei(self.event['price'], 'ether')
        d_event['multiplyFactor'] = self.event['multiplyFactor']
        d_event['expiresInTick'] = self.event['expiresInTick']
        d_event['isBuy'] = self.event['isBuy']
        d_event['orderType'] = self.event['orderType']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['id'],
                d_event['sender'],
                d_event['baseTokenAddress'],
                d_event['secondaryTokenAddress'],
                format(float(d_event['exchangeableAmount']), '.18f'),
                format(float(d_event['reservedCommission']), '.18f'),
                format(float(d_event['price']), '.18f'),
                d_event['multiplyFactor'],
                d_event['expiresInTick'],
                d_event['isBuy'],
                d_event['orderType']
                ]


class DEXOrderCancelled(BaseEvent):
    name = "OrderCancelled"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'id', 'sender', 'returnedAmount',
                   'commission', 'returnedCommission', 'isBuy']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['id'] = self.event['id']
        d_event['sender'] = self.event['sender']
        d_event['returnedAmount'] = Web3.fromWei(self.event['returnedAmount'], 'ether')
        d_event['commission'] = Web3.fromWei(self.event['commission'], 'ether')
        d_event['returnedCommission'] = Web3.fromWei(self.event['returnedCommission'], 'ether')
        d_event['isBuy'] = self.event['isBuy']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['id'],
                d_event['sender'],
                format(float(d_event['returnedAmount']), '.18f'),
                format(float(d_event['commission']), '.18f'),
                format(float(d_event['returnedCommission']), '.18f'),
                d_event['isBuy']
                ]


class DEXTransferFailed(BaseEvent):
    name = "TransferFailed"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', '_tokenAddress', '_to', '_amount',
                   '_isRevert']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['_tokenAddress'] = self.event['_tokenAddress']
        d_event['_to'] = self.event['_to']
        d_event['_amount'] = Web3.fromWei(self.event['_amount'], 'ether')
        d_event['_isRevert'] = self.event['_isRevert']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['_tokenAddress'],
                d_event['_to'],
                format(float(d_event['_amount']), '.18f'),
                d_event['_isRevert']
                ]


class DEXCommissionWithdrawn(BaseEvent):
    name = "CommissionWithdrawn"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'token', 'commissionBeneficiary', 'withdrawnAmount']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['token'] = self.event['token']
        d_event['commissionBeneficiary'] = self.event['commissionBeneficiary']
        d_event['withdrawnAmount'] = Web3.fromWei(self.event['withdrawnAmount'], 'ether')

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['token'],
                d_event['commissionBeneficiary'],
                format(float(d_event['withdrawnAmount']), '.18f')
                ]


class DEXTokenPairDisabled(BaseEvent):
    name = "TokenPairDisabled"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'baseToken', 'secondaryToken']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['baseToken'] = self.event['baseToken']
        d_event['secondaryToken'] = self.event['secondaryToken']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['baseToken'],
                d_event['secondaryToken']
                ]


class DEXTokenPairEnabled(BaseEvent):
    name = "TokenPairEnabled"

    def __init__(self, event):
        self.blockNumber = event['blockNumber']
        self.transactionHash = event['transactionHash']
        self.timestamp = event['timestamp']
        self.event = event['event'][self.name]

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'baseToken', 'secondaryToken']
        return columns

    def formatted(self):
        d_event = dict()
        d_event['blockNumber'] = self.blockNumber
        d_event['timestamp'] = self.timestamp
        d_event['baseToken'] = self.event['baseToken']
        d_event['secondaryToken'] = self.event['secondaryToken']

        return d_event

    def row(self):
        d_event = self.formatted()
        return [d_event['blockNumber'],
                d_event['timestamp'],
                d_event['baseToken'],
                d_event['secondaryToken']
                ]
