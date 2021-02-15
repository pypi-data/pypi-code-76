# SPDX-License-Identifier: GPL-3.0-only
# © Copyright 2021 Julien Harbulot
# see: https://github.com/julien-h/python-eth-common
from collections import namedtuple
from dataclasses import dataclass
import web3.contract
from web3 import Web3
from web3.contract import Contract
from typing import Tuple, NamedTuple, List, Dict, Any, TypeVar, Callable, Generic
from web3.types import TxReceipt
from pathlib import Path
import json
from typing import Union, Any, List
import abc
from hexbytes import HexBytes
import atexit
import sys

Contract_T = TypeVar("Contract_T")
TransactionReceipt_T = TypeVar("TransactionReceipt_T")
DeploymentReceipt_T = TypeVar("DeploymentReceipt_T")
T = TypeVar("T")

# --------------------------------------------------------------
# wrappers


@dataclass
class DeploymentReceipt(Generic[Contract_T]):
    contract: Contract_T
    web3_receipt: TxReceipt
    web3_contract: web3.contract.Contract


@dataclass
class TransactionReceipt:
    web3_receipt: TxReceipt


@dataclass
class PendingTransaction(Generic[TransactionReceipt_T]):
    w3: Web3
    hash: str
    make_receipt: Callable[[TxReceipt], TransactionReceipt_T]

    def waitForReceipt(self) -> TransactionReceipt_T:
        return self.make_receipt(self.w3.eth.waitForTransactionReceipt(self.hash))


@dataclass
class PendingDeployment(Generic[Contract_T]):
    w3: Web3
    hash: str
    on_receipt: Callable[[TxReceipt], Contract_T] = None

    def waitForReceipt(self) -> DeploymentReceipt[Contract_T]:
        receipt = self.w3.eth.waitForTransactionReceipt(self.hash)
        if self.on_receipt:
            c = self.on_receipt(receipt)
            return DeploymentReceipt(
                web3_receipt=receipt, contract=c, web3_contract=c.contract
            )
        else:
            return DeploymentReceipt(
                web3_receipt=receipt, contract=None, web3_contract=None
            )


# To make sure the Function object created are used at least once
objects_to_check = []


def check():
    for o in objects_to_check:
        o.unused_warning()


atexit.register(check)


class Function(Generic[T, TransactionReceipt_T]):
    def __init__(
        self,
        w3,
        web3_fn,
        convert: Callable[[Any], T] = lambda x: x,
        make_receipt: Callable[
            [TxReceipt], TransactionReceipt_T
        ] = lambda x: TransactionReceipt(x),
    ):
        self.w3 = w3
        self.fn = web3_fn
        self.convert = convert
        self.make_receipt = make_receipt
        objects_to_check.append(self)

    def call(self, transaction=None, block_identifier="latest") -> T:
        self.unregister()
        return self.convert(self.fn.call(transaction, block_identifier))

    def transact(self, transaction=None) -> PendingTransaction[TransactionReceipt_T]:
        self.unregister()
        hash = self.fn.transact(transaction)
        return PendingTransaction(self.w3, hash, self.make_receipt)

    def waitForReceipt(self, transaction=None) -> TransactionReceipt_T:
        self.unregister()
        return self.transact(transaction).waitForReceipt()

    def estimateGas(self, transaction=None, block_identifier=None):
        self.unregister()
        return self.fn.estimateGas(transaction, block_identifier)

    def buildTransaction(self, transaction=None):
        self.unregister()
        return self.fn.buildTransaction(transaction)

    def unregister(self):
        try:
            objects_to_check.remove(self)
        except ValueError as e:
            if "not in list" in str(e):
                # this object was already used once, which is fine since we can reuse it
                pass
            else:
                raise e

    def unused_warning(self):
        print(
            "\u001b[31m!! Warning: Function created but not used. Did you forget to call waitForReceipt() ?\u001b[0m",
            file=sys.stderr,
            flush=True,
        )


@dataclass
class Event:
    pass


# -----------------------------------------------------------------------------
# Additional syntactic sugar


class HasAddress(abc.ABC):
    @property
    @abc.abstractmethod
    def address(self):
        ...


Address = Union[str, HasAddress]


def address_of(contract: Address) -> str:
    try:
        return contract.address
    except AttributeError:
        return str(contract)


def unsugar(item: Union[HasAddress, T]) -> Union[HasAddress, T]:
    """ Converts a legal eth_context input argument to a web3 argument """
    if isinstance(item, list):
        return [unsugar(subitem) for subitem in item]
    if isinstance(item, HasAddress):
        return address_of(item)
    else:
        return item
