# SPDX-License-Identifier: GPL-3.0-only
# © Copyright 2021 Julien Harbulot
# see: https://github.com/julien-h/python-eth-balancer
from collections import namedtuple
from dataclasses import dataclass
from web3 import Web3
from web3.types import TxReceipt
from typing import Tuple, NamedTuple, List, Dict, Any, TypeVar, Callable, Generic

from web3.datastructures import AttributeDict
from eth_common.types import *
from pathlib import Path
import json
from typing import Union, Any, List
from hexbytes import HexBytes

BUILD_DIR = Path(__file__).parent.joinpath("resources").resolve()


# ---------------------------------------------------------------
# ERC20

# ---
@dataclass
class ERC20ReceiptEvents:
    contract: "ERC20"
    web3_receipt: TxReceipt

    def Approval(self) -> Any:
        return (
            self.contract.to_web3().events.Approval().processReceipt(self.web3_receipt)
        )

    def Transfer(self) -> Any:
        return (
            self.contract.to_web3().events.Transfer().processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class ERC20Receipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: ERC20ReceiptEvents


# ---


class ERC20Functions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "ERC20"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.DOMAIN_SEPARATOR()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.PERMIT_TYPEHASH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> Function[int, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.allowance(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> Function[bool, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> Function[int, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.balanceOf(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> Function[int, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.nonces(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # permit (address, address, uint256, uint256, uint8, bytes32, bytes32) -> ()
    def permit(
        self,
        owner: Address,
        spender: Address,
        value: int,
        deadline: int,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ):
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        owner, spender, value, deadline, v, r, s = (
            unsugar(owner),
            unsugar(spender),
            unsugar(value),
            unsugar(deadline),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.permit(
            owner, spender, value, deadline, v, r, s
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> Function[bool, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> ERC20Receipt:
            return ERC20Receipt(receipt, ERC20ReceiptEvents(self.contract, receipt))

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class ERC20Caller:
    def __init__(self, functions: ERC20Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "ERC20Caller":
        return ERC20Caller(functions=self.functions, transaction=transaction)

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.DOMAIN_SEPARATOR().call(self.transaction)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.PERMIT_TYPEHASH().call(self.transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> int:
        return self.functions.allowance(item0, item1).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> bool:
        return self.functions.approve(spender, value).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> int:
        return self.functions.balanceOf(item0).call(self.transaction)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # name () -> (string)
    def name(
        self,
    ) -> Any:
        return self.functions.name().call(self.transaction)

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> int:
        return self.functions.nonces(item0).call(self.transaction)

    # permit (address, address, uint256, uint256, uint8, bytes32, bytes32) -> ()
    def permit(
        self,
        owner: Address,
        spender: Address,
        value: int,
        deadline: int,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ):
        return self.functions.permit(owner, spender, value, deadline, v, r, s).call(
            self.transaction
        )

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Any:
        return self.functions.symbol().call(self.transaction)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> int:
        return self.functions.totalSupply().call(self.transaction)

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> bool:
        return self.functions.transfer(to, value).call(self.transaction)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, from_: Address, to: Address, value: int) -> bool:
        return self.functions.transferFrom(from_, to, value).call(self.transaction)


# ---


class ERC20(HasAddress):
    #
    @staticmethod
    def deploy(w3: Web3, totalSupply: int) -> PendingDeployment["ERC20"]:
        if w3 is None:
            raise ValueError("In method ERC20.deploy(w3, ...) w3 must not be None")

        totalSupply = unsugar(totalSupply)
        json_path = BUILD_DIR.joinpath("utils/ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(totalSupply).transact()

        def on_receipt(receipt) -> "ERC20":
            return ERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("utils/ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = ERC20Functions(w3, address, self.contract, self)
        self.call = ERC20Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> ERC20Receipt:
        return self.functions.DOMAIN_SEPARATOR().waitForReceipt()

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> ERC20Receipt:
        return self.functions.PERMIT_TYPEHASH().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> ERC20Receipt:
        return self.functions.allowance(item0, item1).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> ERC20Receipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> ERC20Receipt:
        return self.functions.balanceOf(item0).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> ERC20Receipt:
        return self.functions.decimals().waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> ERC20Receipt:
        return self.functions.name().waitForReceipt()

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> ERC20Receipt:
        return self.functions.nonces(item0).waitForReceipt()

    # permit (address, address, uint256, uint256, uint8, bytes32, bytes32) -> ()
    def permit(
        self,
        owner: Address,
        spender: Address,
        value: int,
        deadline: int,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> ERC20Receipt:
        return self.functions.permit(
            owner, spender, value, deadline, v, r, s
        ).waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> ERC20Receipt:
        return self.functions.symbol().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> ERC20Receipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> ERC20Receipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, from_: Address, to: Address, value: int) -> ERC20Receipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end ERC20 ----------
