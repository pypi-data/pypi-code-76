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
# BConst

# ---
@dataclass
class BConstReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class BConstFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "BConst"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BConstReceipt]:
        def make_receipt(receipt: TxReceipt) -> BConstReceipt:
            return BConstReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BConstCaller:
    def __init__(self, functions: BConstFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BConstCaller":
        return BConstCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)


# ---


class BConst(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BConst"]:
        if w3 is None:
            raise ValueError("In method BConst.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BConst.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BConst":
            return BConst(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BConst.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BConstFunctions(w3, address, self.contract, self)
        self.call = BConstCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> BConstReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> BConstReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> BConstReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> BConstReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> BConstReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> BConstReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> BConstReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> BConstReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> BConstReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> BConstReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> BConstReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> BConstReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> BConstReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> BConstReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> BConstReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> BConstReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BConstReceipt:
        return self.functions.getColor().waitForReceipt()


# --------- end BConst ----------


# ---------------------------------------------------------------
# IERC20

# ---
@dataclass
class IERC20ReceiptEvents:
    contract: "IERC20"
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
class IERC20Receipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: IERC20ReceiptEvents


# ---


class IERC20Functions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "IERC20"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> Function[int, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        whom = unsugar(whom)
        web3_fn = self.web3_contract.functions.balanceOf(whom)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> Function[int, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        src, dst = unsugar(src), unsugar(dst)
        web3_fn = self.web3_contract.functions.allowance(src, dst)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> Function[bool, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.approve(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> Function[bool, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transfer(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, src: Address, dst: Address, amt: int
    ) -> Function[bool, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        src, dst, amt = unsugar(src), unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transferFrom(src, dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IERC20Caller:
    def __init__(self, functions: IERC20Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IERC20Caller":
        return IERC20Caller(functions=self.functions, transaction=transaction)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> int:
        return self.functions.totalSupply().call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> int:
        return self.functions.balanceOf(whom).call(self.transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> int:
        return self.functions.allowance(src, dst).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> bool:
        return self.functions.approve(dst, amt).call(self.transaction)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> bool:
        return self.functions.transfer(dst, amt).call(self.transaction)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> bool:
        return self.functions.transferFrom(src, dst, amt).call(self.transaction)


# ---


class IERC20(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IERC20"]:
        if w3 is None:
            raise ValueError("In method IERC20.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/IERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IERC20":
            return IERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/IERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IERC20Functions(w3, address, self.contract, self)
        self.call = IERC20Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> IERC20Receipt:
        return self.functions.totalSupply().waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> IERC20Receipt:
        return self.functions.balanceOf(whom).waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> IERC20Receipt:
        return self.functions.allowance(src, dst).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> IERC20Receipt:
        return self.functions.approve(dst, amt).waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> IERC20Receipt:
        return self.functions.transfer(dst, amt).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> IERC20Receipt:
        return self.functions.transferFrom(src, dst, amt).waitForReceipt()


# --------- end IERC20 ----------


# ---------------------------------------------------------------
# TBPoolJoinExit

# ---
@dataclass
class TBPoolJoinExitReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class TBPoolJoinExitFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "TBPoolJoinExit"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> Function[bool, TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.echidna_no_bug_found()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], TBPoolJoinExitReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # joinAndExitPool (uint256, uint256, uint256, uint256) -> ()
    def joinAndExitPool(
        self,
        poolAmountOut: int,
        poolAmountIn: int,
        poolTotal: int,
        records_t_balance: int,
    ):
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitReceipt:
            return TBPoolJoinExitReceipt(receipt)

        poolAmountOut, poolAmountIn, poolTotal, records_t_balance = (
            unsugar(poolAmountOut),
            unsugar(poolAmountIn),
            unsugar(poolTotal),
            unsugar(records_t_balance),
        )
        web3_fn = self.web3_contract.functions.joinAndExitPool(
            poolAmountOut, poolAmountIn, poolTotal, records_t_balance
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class TBPoolJoinExitCaller:
    def __init__(self, functions: TBPoolJoinExitFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "TBPoolJoinExitCaller":
        return TBPoolJoinExitCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> bool:
        return self.functions.echidna_no_bug_found().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # joinAndExitPool (uint256, uint256, uint256, uint256) -> ()
    def joinAndExitPool(
        self,
        poolAmountOut: int,
        poolAmountIn: int,
        poolTotal: int,
        records_t_balance: int,
    ):
        return self.functions.joinAndExitPool(
            poolAmountOut, poolAmountIn, poolTotal, records_t_balance
        ).call(self.transaction)


# ---


class TBPoolJoinExit(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["TBPoolJoinExit"]:
        if w3 is None:
            raise ValueError(
                "In method TBPoolJoinExit.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/TBPoolJoinExit.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "TBPoolJoinExit":
            return TBPoolJoinExit(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/TBPoolJoinExit.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = TBPoolJoinExitFunctions(w3, address, self.contract, self)
        self.call = TBPoolJoinExitCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.echidna_no_bug_found().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.getColor().waitForReceipt()

    # joinAndExitPool (uint256, uint256, uint256, uint256) -> ()
    def joinAndExitPool(
        self,
        poolAmountOut: int,
        poolAmountIn: int,
        poolTotal: int,
        records_t_balance: int,
    ) -> TBPoolJoinExitReceipt:
        return self.functions.joinAndExitPool(
            poolAmountOut, poolAmountIn, poolTotal, records_t_balance
        ).waitForReceipt()


# --------- end TBPoolJoinExit ----------


# ---------------------------------------------------------------
# Migrations

# ---
@dataclass
class MigrationsReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class MigrationsFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "Migrations"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # lastCompletedMigration () -> (uint256)
    def lastCompletedMigration(
        self,
    ) -> Function[int, MigrationsReceipt]:
        def make_receipt(receipt: TxReceipt) -> MigrationsReceipt:
            return MigrationsReceipt(receipt)

        web3_fn = self.web3_contract.functions.lastCompletedMigration()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # owner () -> (address)
    def owner(
        self,
    ) -> Function[Address, MigrationsReceipt]:
        def make_receipt(receipt: TxReceipt) -> MigrationsReceipt:
            return MigrationsReceipt(receipt)

        web3_fn = self.web3_contract.functions.owner()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setCompleted (uint256) -> ()
    def setCompleted(self, completed: int):
        def make_receipt(receipt: TxReceipt) -> MigrationsReceipt:
            return MigrationsReceipt(receipt)

        completed = unsugar(completed)
        web3_fn = self.web3_contract.functions.setCompleted(completed)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # upgrade (address) -> ()
    def upgrade(self, new_address: Address):
        def make_receipt(receipt: TxReceipt) -> MigrationsReceipt:
            return MigrationsReceipt(receipt)

        new_address = unsugar(new_address)
        web3_fn = self.web3_contract.functions.upgrade(new_address)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class MigrationsCaller:
    def __init__(self, functions: MigrationsFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "MigrationsCaller":
        return MigrationsCaller(functions=self.functions, transaction=transaction)

    # lastCompletedMigration () -> (uint256)
    def lastCompletedMigration(
        self,
    ) -> int:
        return self.functions.lastCompletedMigration().call(self.transaction)

    # owner () -> (address)
    def owner(
        self,
    ) -> Address:
        return self.functions.owner().call(self.transaction)

    # setCompleted (uint256) -> ()
    def setCompleted(self, completed: int):
        return self.functions.setCompleted(completed).call(self.transaction)

    # upgrade (address) -> ()
    def upgrade(self, new_address: Address):
        return self.functions.upgrade(new_address).call(self.transaction)


# ---


class Migrations(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["Migrations"]:
        if w3 is None:
            raise ValueError("In method Migrations.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/Migrations.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "Migrations":
            return Migrations(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/Migrations.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = MigrationsFunctions(w3, address, self.contract, self)
        self.call = MigrationsCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # lastCompletedMigration () -> (uint256)
    def lastCompletedMigration(
        self,
    ) -> MigrationsReceipt:
        return self.functions.lastCompletedMigration().waitForReceipt()

    # owner () -> (address)
    def owner(
        self,
    ) -> MigrationsReceipt:
        return self.functions.owner().waitForReceipt()

    # setCompleted (uint256) -> ()
    def setCompleted(self, completed: int) -> MigrationsReceipt:
        return self.functions.setCompleted(completed).waitForReceipt()

    # upgrade (address) -> ()
    def upgrade(self, new_address: Address) -> MigrationsReceipt:
        return self.functions.upgrade(new_address).waitForReceipt()


# --------- end Migrations ----------


# ---------------------------------------------------------------
# BBronze

# ---
@dataclass
class BBronzeReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class BBronzeFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "BBronze"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BBronzeReceipt]:
        def make_receipt(receipt: TxReceipt) -> BBronzeReceipt:
            return BBronzeReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BBronzeCaller:
    def __init__(self, functions: BBronzeFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BBronzeCaller":
        return BBronzeCaller(functions=self.functions, transaction=transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)


# ---


class BBronze(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BBronze"]:
        if w3 is None:
            raise ValueError("In method BBronze.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BBronze.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BBronze":
            return BBronze(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BBronze.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BBronzeFunctions(w3, address, self.contract, self)
        self.call = BBronzeCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BBronzeReceipt:
        return self.functions.getColor().waitForReceipt()


# --------- end BBronze ----------


# ---------------------------------------------------------------
# BColor

# ---
@dataclass
class BColorReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class BColorFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "BColor"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BColorReceipt]:
        def make_receipt(receipt: TxReceipt) -> BColorReceipt:
            return BColorReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BColorCaller:
    def __init__(self, functions: BColorFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BColorCaller":
        return BColorCaller(functions=self.functions, transaction=transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)


# ---


class BColor(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BColor"]:
        if w3 is None:
            raise ValueError("In method BColor.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BColor.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BColor":
            return BColor(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BColor.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BColorFunctions(w3, address, self.contract, self)
        self.call = BColorCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BColorReceipt:
        return self.functions.getColor().waitForReceipt()


# --------- end BColor ----------


# ---------------------------------------------------------------
# TBPoolJoinExitNoFee

# ---
@dataclass
class TBPoolJoinExitNoFeeReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class TBPoolJoinExitNoFeeFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "TBPoolJoinExitNoFee",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> Function[bool, TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.echidna_no_bug_found()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], TBPoolJoinExitNoFeeReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # joinAndExitNoFeePool (uint256, uint256, uint256, uint256) -> ()
    def joinAndExitNoFeePool(
        self,
        poolAmountOut: int,
        poolAmountIn: int,
        poolTotal: int,
        records_t_balance: int,
    ):
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinExitNoFeeReceipt:
            return TBPoolJoinExitNoFeeReceipt(receipt)

        poolAmountOut, poolAmountIn, poolTotal, records_t_balance = (
            unsugar(poolAmountOut),
            unsugar(poolAmountIn),
            unsugar(poolTotal),
            unsugar(records_t_balance),
        )
        web3_fn = self.web3_contract.functions.joinAndExitNoFeePool(
            poolAmountOut, poolAmountIn, poolTotal, records_t_balance
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class TBPoolJoinExitNoFeeCaller:
    def __init__(self, functions: TBPoolJoinExitNoFeeFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "TBPoolJoinExitNoFeeCaller":
        return TBPoolJoinExitNoFeeCaller(
            functions=self.functions, transaction=transaction
        )

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> bool:
        return self.functions.echidna_no_bug_found().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # joinAndExitNoFeePool (uint256, uint256, uint256, uint256) -> ()
    def joinAndExitNoFeePool(
        self,
        poolAmountOut: int,
        poolAmountIn: int,
        poolTotal: int,
        records_t_balance: int,
    ):
        return self.functions.joinAndExitNoFeePool(
            poolAmountOut, poolAmountIn, poolTotal, records_t_balance
        ).call(self.transaction)


# ---


class TBPoolJoinExitNoFee(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["TBPoolJoinExitNoFee"]:
        if w3 is None:
            raise ValueError(
                "In method TBPoolJoinExitNoFee.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/TBPoolJoinExitNoFee.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "TBPoolJoinExitNoFee":
            return TBPoolJoinExitNoFee(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/TBPoolJoinExitNoFee.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = TBPoolJoinExitNoFeeFunctions(w3, address, self.contract, self)
        self.call = TBPoolJoinExitNoFeeCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.echidna_no_bug_found().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.getColor().waitForReceipt()

    # joinAndExitNoFeePool (uint256, uint256, uint256, uint256) -> ()
    def joinAndExitNoFeePool(
        self,
        poolAmountOut: int,
        poolAmountIn: int,
        poolTotal: int,
        records_t_balance: int,
    ) -> TBPoolJoinExitNoFeeReceipt:
        return self.functions.joinAndExitNoFeePool(
            poolAmountOut, poolAmountIn, poolTotal, records_t_balance
        ).waitForReceipt()


# --------- end TBPoolJoinExitNoFee ----------


# ---------------------------------------------------------------
# TMath

Calc_bsubSignOutput = namedtuple(
    "Calc_bsubSignOutput", [x.strip() for x in " item0, item1".split(",")]
)
# ---
@dataclass
class TMathReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class TMathFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "TMath"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(tokenAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(tokenAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        (
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(tokenAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(tokenAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(poolAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        (
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(poolAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_btoi (uint256) -> (uint256)
    def calc_btoi(self, a: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a = unsugar(a)
        web3_fn = self.web3_contract.functions.calc_btoi(a)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_bfloor (uint256) -> (uint256)
    def calc_bfloor(self, a: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a = unsugar(a)
        web3_fn = self.web3_contract.functions.calc_bfloor(a)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_badd (uint256, uint256) -> (uint256)
    def calc_badd(self, a: int, b: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a, b = unsugar(a), unsugar(b)
        web3_fn = self.web3_contract.functions.calc_badd(a, b)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_bsub (uint256, uint256) -> (uint256)
    def calc_bsub(self, a: int, b: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a, b = unsugar(a), unsugar(b)
        web3_fn = self.web3_contract.functions.calc_bsub(a, b)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_bsubSign (uint256, uint256) -> (uint256, bool)
    def calc_bsubSign(
        self, a: int, b: int
    ) -> Function[Calc_bsubSignOutput, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a, b = unsugar(a), unsugar(b)
        web3_fn = self.web3_contract.functions.calc_bsubSign(a, b)

        def convert(args) -> Calc_bsubSignOutput:
            return Calc_bsubSignOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # calc_bmul (uint256, uint256) -> (uint256)
    def calc_bmul(self, a: int, b: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a, b = unsugar(a), unsugar(b)
        web3_fn = self.web3_contract.functions.calc_bmul(a, b)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_bdiv (uint256, uint256) -> (uint256)
    def calc_bdiv(self, a: int, b: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a, b = unsugar(a), unsugar(b)
        web3_fn = self.web3_contract.functions.calc_bdiv(a, b)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_bpowi (uint256, uint256) -> (uint256)
    def calc_bpowi(self, a: int, n: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        a, n = unsugar(a), unsugar(n)
        web3_fn = self.web3_contract.functions.calc_bpowi(a, n)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_bpow (uint256, uint256) -> (uint256)
    def calc_bpow(self, base: int, exp: int) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        base, exp = unsugar(base), unsugar(exp)
        web3_fn = self.web3_contract.functions.calc_bpow(base, exp)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calc_bpowApprox (uint256, uint256, uint256) -> (uint256)
    def calc_bpowApprox(
        self, base: int, exp: int, precision: int
    ) -> Function[int, TMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> TMathReceipt:
            return TMathReceipt(receipt)

        base, exp, precision = unsugar(base), unsugar(exp), unsugar(precision)
        web3_fn = self.web3_contract.functions.calc_bpowApprox(base, exp, precision)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class TMathCaller:
    def __init__(self, functions: TMathFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "TMathCaller":
        return TMathCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        ).call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # calc_btoi (uint256) -> (uint256)
    def calc_btoi(self, a: int) -> int:
        return self.functions.calc_btoi(a).call(self.transaction)

    # calc_bfloor (uint256) -> (uint256)
    def calc_bfloor(self, a: int) -> int:
        return self.functions.calc_bfloor(a).call(self.transaction)

    # calc_badd (uint256, uint256) -> (uint256)
    def calc_badd(self, a: int, b: int) -> int:
        return self.functions.calc_badd(a, b).call(self.transaction)

    # calc_bsub (uint256, uint256) -> (uint256)
    def calc_bsub(self, a: int, b: int) -> int:
        return self.functions.calc_bsub(a, b).call(self.transaction)

    # calc_bsubSign (uint256, uint256) -> (uint256, bool)
    def calc_bsubSign(self, a: int, b: int) -> Calc_bsubSignOutput:
        return self.functions.calc_bsubSign(a, b).call(self.transaction)

    # calc_bmul (uint256, uint256) -> (uint256)
    def calc_bmul(self, a: int, b: int) -> int:
        return self.functions.calc_bmul(a, b).call(self.transaction)

    # calc_bdiv (uint256, uint256) -> (uint256)
    def calc_bdiv(self, a: int, b: int) -> int:
        return self.functions.calc_bdiv(a, b).call(self.transaction)

    # calc_bpowi (uint256, uint256) -> (uint256)
    def calc_bpowi(self, a: int, n: int) -> int:
        return self.functions.calc_bpowi(a, n).call(self.transaction)

    # calc_bpow (uint256, uint256) -> (uint256)
    def calc_bpow(self, base: int, exp: int) -> int:
        return self.functions.calc_bpow(base, exp).call(self.transaction)

    # calc_bpowApprox (uint256, uint256, uint256) -> (uint256)
    def calc_bpowApprox(self, base: int, exp: int, precision: int) -> int:
        return self.functions.calc_bpowApprox(base, exp, precision).call(
            self.transaction
        )


# ---


class TMath(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["TMath"]:
        if w3 is None:
            raise ValueError("In method TMath.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/TMath.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "TMath":
            return TMath(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/TMath.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = TMathFunctions(w3, address, self.contract, self)
        self.call = TMathCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> TMathReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> TMathReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> TMathReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> TMathReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> TMathReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> TMathReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> TMathReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> TMathReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> TMathReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> TMathReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> TMathReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> TMathReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> TMathReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> TMathReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> TMathReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> TMathReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> TMathReceipt:
        return self.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> TMathReceipt:
        return self.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> TMathReceipt:
        return self.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> TMathReceipt:
        return self.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> TMathReceipt:
        return self.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> TMathReceipt:
        return self.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> TMathReceipt:
        return self.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        ).waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> TMathReceipt:
        return self.functions.getColor().waitForReceipt()

    # calc_btoi (uint256) -> (uint256)
    def calc_btoi(self, a: int) -> TMathReceipt:
        return self.functions.calc_btoi(a).waitForReceipt()

    # calc_bfloor (uint256) -> (uint256)
    def calc_bfloor(self, a: int) -> TMathReceipt:
        return self.functions.calc_bfloor(a).waitForReceipt()

    # calc_badd (uint256, uint256) -> (uint256)
    def calc_badd(self, a: int, b: int) -> TMathReceipt:
        return self.functions.calc_badd(a, b).waitForReceipt()

    # calc_bsub (uint256, uint256) -> (uint256)
    def calc_bsub(self, a: int, b: int) -> TMathReceipt:
        return self.functions.calc_bsub(a, b).waitForReceipt()

    # calc_bsubSign (uint256, uint256) -> (uint256, bool)
    def calc_bsubSign(self, a: int, b: int) -> TMathReceipt:
        return self.functions.calc_bsubSign(a, b).waitForReceipt()

    # calc_bmul (uint256, uint256) -> (uint256)
    def calc_bmul(self, a: int, b: int) -> TMathReceipt:
        return self.functions.calc_bmul(a, b).waitForReceipt()

    # calc_bdiv (uint256, uint256) -> (uint256)
    def calc_bdiv(self, a: int, b: int) -> TMathReceipt:
        return self.functions.calc_bdiv(a, b).waitForReceipt()

    # calc_bpowi (uint256, uint256) -> (uint256)
    def calc_bpowi(self, a: int, n: int) -> TMathReceipt:
        return self.functions.calc_bpowi(a, n).waitForReceipt()

    # calc_bpow (uint256, uint256) -> (uint256)
    def calc_bpow(self, base: int, exp: int) -> TMathReceipt:
        return self.functions.calc_bpow(base, exp).waitForReceipt()

    # calc_bpowApprox (uint256, uint256, uint256) -> (uint256)
    def calc_bpowApprox(self, base: int, exp: int, precision: int) -> TMathReceipt:
        return self.functions.calc_bpowApprox(base, exp, precision).waitForReceipt()


# --------- end TMath ----------


# ---------------------------------------------------------------
# BFactory

# ---
@dataclass
class BFactoryReceiptEvents:
    contract: "BFactory"
    web3_receipt: TxReceipt

    def LOG_BLABS(self) -> Any:
        return (
            self.contract.to_web3().events.LOG_BLABS().processReceipt(self.web3_receipt)
        )

    def LOG_NEW_POOL(self) -> Any:
        return (
            self.contract.to_web3()
            .events.LOG_NEW_POOL()
            .processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class BFactoryReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: BFactoryReceiptEvents


# ---


class BFactoryFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "BFactory"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BFactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> BFactoryReceipt:
            return BFactoryReceipt(
                receipt, BFactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # isBPool (address) -> (bool)
    def isBPool(self, b: Address) -> Function[bool, BFactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> BFactoryReceipt:
            return BFactoryReceipt(
                receipt, BFactoryReceiptEvents(self.contract, receipt)
            )

        b = unsugar(b)
        web3_fn = self.web3_contract.functions.isBPool(b)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # newBPool () -> (address)
    def newBPool(
        self,
    ) -> Function[Address, BFactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> BFactoryReceipt:
            return BFactoryReceipt(
                receipt, BFactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.newBPool()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getBLabs () -> (address)
    def getBLabs(
        self,
    ) -> Function[Address, BFactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> BFactoryReceipt:
            return BFactoryReceipt(
                receipt, BFactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.getBLabs()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setBLabs (address) -> ()
    def setBLabs(self, b: Address):
        def make_receipt(receipt: TxReceipt) -> BFactoryReceipt:
            return BFactoryReceipt(
                receipt, BFactoryReceiptEvents(self.contract, receipt)
            )

        b = unsugar(b)
        web3_fn = self.web3_contract.functions.setBLabs(b)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # collect (address) -> ()
    def collect(self, pool: Address):
        def make_receipt(receipt: TxReceipt) -> BFactoryReceipt:
            return BFactoryReceipt(
                receipt, BFactoryReceiptEvents(self.contract, receipt)
            )

        pool = unsugar(pool)
        web3_fn = self.web3_contract.functions.collect(pool)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BFactoryCaller:
    def __init__(self, functions: BFactoryFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BFactoryCaller":
        return BFactoryCaller(functions=self.functions, transaction=transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # isBPool (address) -> (bool)
    def isBPool(self, b: Address) -> bool:
        return self.functions.isBPool(b).call(self.transaction)

    # newBPool () -> (address)
    def newBPool(
        self,
    ) -> Address:
        return self.functions.newBPool().call(self.transaction)

    # getBLabs () -> (address)
    def getBLabs(
        self,
    ) -> Address:
        return self.functions.getBLabs().call(self.transaction)

    # setBLabs (address) -> ()
    def setBLabs(self, b: Address):
        return self.functions.setBLabs(b).call(self.transaction)

    # collect (address) -> ()
    def collect(self, pool: Address):
        return self.functions.collect(pool).call(self.transaction)


# ---


class BFactory(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BFactory"]:
        if w3 is None:
            raise ValueError("In method BFactory.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BFactory.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BFactory":
            return BFactory(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BFactory.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BFactoryFunctions(w3, address, self.contract, self)
        self.call = BFactoryCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BFactoryReceipt:
        return self.functions.getColor().waitForReceipt()

    # isBPool (address) -> (bool)
    def isBPool(self, b: Address) -> BFactoryReceipt:
        return self.functions.isBPool(b).waitForReceipt()

    # newBPool () -> (address)
    def newBPool(
        self,
    ) -> BFactoryReceipt:
        return self.functions.newBPool().waitForReceipt()

    # getBLabs () -> (address)
    def getBLabs(
        self,
    ) -> BFactoryReceipt:
        return self.functions.getBLabs().waitForReceipt()

    # setBLabs (address) -> ()
    def setBLabs(self, b: Address) -> BFactoryReceipt:
        return self.functions.setBLabs(b).waitForReceipt()

    # collect (address) -> ()
    def collect(self, pool: Address) -> BFactoryReceipt:
        return self.functions.collect(pool).waitForReceipt()


# --------- end BFactory ----------


# ---------------------------------------------------------------
# TToken

# ---
@dataclass
class TTokenReceiptEvents:
    contract: "TToken"
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
class TTokenReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: TTokenReceiptEvents


# ---


class TTokenFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "TToken"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> Function[int, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        src, dst = unsugar(src), unsugar(dst)
        web3_fn = self.web3_contract.functions.allowance(src, dst)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> Function[int, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        whom = unsugar(whom)
        web3_fn = self.web3_contract.functions.balanceOf(whom)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> Function[bool, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.approve(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # mint (address, uint256) -> (bool)
    def mint(self, dst: Address, amt: int) -> Function[bool, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.mint(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # burn (uint256) -> (bool)
    def burn(self, amt: int) -> Function[bool, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        amt = unsugar(amt)
        web3_fn = self.web3_contract.functions.burn(amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> Function[bool, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transfer(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, src: Address, dst: Address, amt: int
    ) -> Function[bool, TTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> TTokenReceipt:
            return TTokenReceipt(receipt, TTokenReceiptEvents(self.contract, receipt))

        src, dst, amt = unsugar(src), unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transferFrom(src, dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class TTokenCaller:
    def __init__(self, functions: TTokenFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "TTokenCaller":
        return TTokenCaller(functions=self.functions, transaction=transaction)

    # name () -> (string)
    def name(
        self,
    ) -> Any:
        return self.functions.name().call(self.transaction)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Any:
        return self.functions.symbol().call(self.transaction)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> int:
        return self.functions.allowance(src, dst).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> int:
        return self.functions.balanceOf(whom).call(self.transaction)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> int:
        return self.functions.totalSupply().call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> bool:
        return self.functions.approve(dst, amt).call(self.transaction)

    # mint (address, uint256) -> (bool)
    def mint(self, dst: Address, amt: int) -> bool:
        return self.functions.mint(dst, amt).call(self.transaction)

    # burn (uint256) -> (bool)
    def burn(self, amt: int) -> bool:
        return self.functions.burn(amt).call(self.transaction)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> bool:
        return self.functions.transfer(dst, amt).call(self.transaction)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> bool:
        return self.functions.transferFrom(src, dst, amt).call(self.transaction)


# ---


class TToken(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, name: Any, symbol: Any, decimals: int
    ) -> PendingDeployment["TToken"]:
        if w3 is None:
            raise ValueError("In method TToken.deploy(w3, ...) w3 must not be None")

        name, symbol, decimals = unsugar(name), unsugar(symbol), unsugar(decimals)
        json_path = BUILD_DIR.joinpath("core/TToken.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(name, symbol, decimals).transact()

        def on_receipt(receipt) -> "TToken":
            return TToken(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/TToken.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = TTokenFunctions(w3, address, self.contract, self)
        self.call = TTokenCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # name () -> (string)
    def name(
        self,
    ) -> TTokenReceipt:
        return self.functions.name().waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> TTokenReceipt:
        return self.functions.symbol().waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> TTokenReceipt:
        return self.functions.decimals().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> TTokenReceipt:
        return self.functions.allowance(src, dst).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> TTokenReceipt:
        return self.functions.balanceOf(whom).waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> TTokenReceipt:
        return self.functions.totalSupply().waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> TTokenReceipt:
        return self.functions.approve(dst, amt).waitForReceipt()

    # mint (address, uint256) -> (bool)
    def mint(self, dst: Address, amt: int) -> TTokenReceipt:
        return self.functions.mint(dst, amt).waitForReceipt()

    # burn (uint256) -> (bool)
    def burn(self, amt: int) -> TTokenReceipt:
        return self.functions.burn(amt).waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> TTokenReceipt:
        return self.functions.transfer(dst, amt).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> TTokenReceipt:
        return self.functions.transferFrom(src, dst, amt).waitForReceipt()


# --------- end TToken ----------


# ---------------------------------------------------------------
# TBPoolJoinPool

# ---
@dataclass
class TBPoolJoinPoolReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class TBPoolJoinPoolFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "TBPoolJoinPool"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> Function[bool, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.echidna_no_bug_found()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # joinPool (uint256, uint256, uint256) -> (uint256)
    def joinPool(
        self, poolAmountOut: int, poolTotal: int, records_t_balance: int
    ) -> Function[int, TBPoolJoinPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> TBPoolJoinPoolReceipt:
            return TBPoolJoinPoolReceipt(receipt)

        poolAmountOut, poolTotal, records_t_balance = (
            unsugar(poolAmountOut),
            unsugar(poolTotal),
            unsugar(records_t_balance),
        )
        web3_fn = self.web3_contract.functions.joinPool(
            poolAmountOut, poolTotal, records_t_balance
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class TBPoolJoinPoolCaller:
    def __init__(self, functions: TBPoolJoinPoolFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "TBPoolJoinPoolCaller":
        return TBPoolJoinPoolCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> bool:
        return self.functions.echidna_no_bug_found().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # joinPool (uint256, uint256, uint256) -> (uint256)
    def joinPool(
        self, poolAmountOut: int, poolTotal: int, records_t_balance: int
    ) -> int:
        return self.functions.joinPool(
            poolAmountOut, poolTotal, records_t_balance
        ).call(self.transaction)


# ---


class TBPoolJoinPool(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["TBPoolJoinPool"]:
        if w3 is None:
            raise ValueError(
                "In method TBPoolJoinPool.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/TBPoolJoinPool.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "TBPoolJoinPool":
            return TBPoolJoinPool(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/TBPoolJoinPool.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = TBPoolJoinPoolFunctions(w3, address, self.contract, self)
        self.call = TBPoolJoinPoolCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # echidna_no_bug_found () -> (bool)
    def echidna_no_bug_found(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.echidna_no_bug_found().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.getColor().waitForReceipt()

    # joinPool (uint256, uint256, uint256) -> (uint256)
    def joinPool(
        self, poolAmountOut: int, poolTotal: int, records_t_balance: int
    ) -> TBPoolJoinPoolReceipt:
        return self.functions.joinPool(
            poolAmountOut, poolTotal, records_t_balance
        ).waitForReceipt()


# --------- end TBPoolJoinPool ----------


# ---------------------------------------------------------------
# BTokenBase

# ---
@dataclass
class BTokenBaseReceiptEvents:
    contract: "BTokenBase"
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
class BTokenBaseReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: BTokenBaseReceiptEvents


# ---


class BTokenBaseFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "BTokenBase"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BTokenBaseReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenBaseReceipt:
            return BTokenBaseReceipt(
                receipt, BTokenBaseReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BTokenBaseCaller:
    def __init__(self, functions: BTokenBaseFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BTokenBaseCaller":
        return BTokenBaseCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)


# ---


class BTokenBase(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BTokenBase"]:
        if w3 is None:
            raise ValueError("In method BTokenBase.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BTokenBase.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BTokenBase":
            return BTokenBase(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BTokenBase.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BTokenBaseFunctions(w3, address, self.contract, self)
        self.call = BTokenBaseCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BTokenBaseReceipt:
        return self.functions.getColor().waitForReceipt()


# --------- end BTokenBase ----------


# ---------------------------------------------------------------
# BNum

# ---
@dataclass
class BNumReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class BNumFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "BNum"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BNumReceipt]:
        def make_receipt(receipt: TxReceipt) -> BNumReceipt:
            return BNumReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BNumCaller:
    def __init__(self, functions: BNumFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BNumCaller":
        return BNumCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)


# ---


class BNum(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BNum"]:
        if w3 is None:
            raise ValueError("In method BNum.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BNum.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BNum":
            return BNum(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BNum.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BNumFunctions(w3, address, self.contract, self)
        self.call = BNumCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> BNumReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> BNumReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> BNumReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> BNumReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> BNumReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> BNumReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> BNumReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> BNumReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> BNumReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> BNumReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> BNumReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> BNumReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> BNumReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> BNumReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> BNumReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> BNumReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BNumReceipt:
        return self.functions.getColor().waitForReceipt()


# --------- end BNum ----------


# ---------------------------------------------------------------
# BPool

SwapExactAmountInOutput = namedtuple(
    "SwapExactAmountInOutput",
    [x.strip() for x in " tokenAmountOut, spotPriceAfter".split(",")],
)
SwapExactAmountOutOutput = namedtuple(
    "SwapExactAmountOutOutput",
    [x.strip() for x in " tokenAmountIn, spotPriceAfter".split(",")],
)
# ---
@dataclass
class BPoolReceiptEvents:
    contract: "BPool"
    web3_receipt: TxReceipt

    def Approval(self) -> Any:
        return (
            self.contract.to_web3().events.Approval().processReceipt(self.web3_receipt)
        )

    def LOG_CALL(self) -> Any:
        return (
            self.contract.to_web3().events.LOG_CALL().processReceipt(self.web3_receipt)
        )

    def LOG_EXIT(self) -> Any:
        return (
            self.contract.to_web3().events.LOG_EXIT().processReceipt(self.web3_receipt)
        )

    def LOG_JOIN(self) -> Any:
        return (
            self.contract.to_web3().events.LOG_JOIN().processReceipt(self.web3_receipt)
        )

    def LOG_SWAP(self) -> Any:
        return (
            self.contract.to_web3().events.LOG_SWAP().processReceipt(self.web3_receipt)
        )

    def Transfer(self) -> Any:
        return (
            self.contract.to_web3().events.Transfer().processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class BPoolReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: BPoolReceiptEvents


# ---


class BPoolFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "BPool"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        src, dst = unsugar(src), unsugar(dst)
        web3_fn = self.web3_contract.functions.allowance(src, dst)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.approve(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        whom = unsugar(whom)
        web3_fn = self.web3_contract.functions.balanceOf(whom)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        (
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(tokenAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        (
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(tokenAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        (
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(tokenAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        (
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(tokenAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        (
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(poolAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        (
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(poolAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decreaseApproval (address, uint256) -> (bool)
    def decreaseApproval(self, dst: Address, amt: int) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.decreaseApproval(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # increaseApproval (address, uint256) -> (bool)
    def increaseApproval(self, dst: Address, amt: int) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.increaseApproval(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transfer(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, src: Address, dst: Address, amt: int
    ) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        src, dst, amt = unsugar(src), unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transferFrom(src, dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # isPublicSwap () -> (bool)
    def isPublicSwap(
        self,
    ) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.isPublicSwap()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # isFinalized () -> (bool)
    def isFinalized(
        self,
    ) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.isFinalized()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # isBound (address) -> (bool)
    def isBound(self, t: Address) -> Function[bool, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        t = unsugar(t)
        web3_fn = self.web3_contract.functions.isBound(t)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getNumTokens () -> (uint256)
    def getNumTokens(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getNumTokens()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getCurrentTokens () -> (address[])
    def getCurrentTokens(
        self,
    ) -> Function[List[Address], BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getCurrentTokens()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getFinalTokens () -> (address[])
    def getFinalTokens(
        self,
    ) -> Function[List[Address], BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getFinalTokens()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getDenormalizedWeight (address) -> (uint256)
    def getDenormalizedWeight(self, token: Address) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        token = unsugar(token)
        web3_fn = self.web3_contract.functions.getDenormalizedWeight(token)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getTotalDenormalizedWeight () -> (uint256)
    def getTotalDenormalizedWeight(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getTotalDenormalizedWeight()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getNormalizedWeight (address) -> (uint256)
    def getNormalizedWeight(self, token: Address) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        token = unsugar(token)
        web3_fn = self.web3_contract.functions.getNormalizedWeight(token)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getBalance (address) -> (uint256)
    def getBalance(self, token: Address) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        token = unsugar(token)
        web3_fn = self.web3_contract.functions.getBalance(token)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getSwapFee () -> (uint256)
    def getSwapFee(
        self,
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getSwapFee()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getController () -> (address)
    def getController(
        self,
    ) -> Function[Address, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getController()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setSwapFee (uint256) -> ()
    def setSwapFee(self, swapFee: int):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        swapFee = unsugar(swapFee)
        web3_fn = self.web3_contract.functions.setSwapFee(swapFee)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setController (address) -> ()
    def setController(self, manager: Address):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        manager = unsugar(manager)
        web3_fn = self.web3_contract.functions.setController(manager)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setPublicSwap (bool) -> ()
    def setPublicSwap(self, public_: bool):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        public_ = unsugar(public_)
        web3_fn = self.web3_contract.functions.setPublicSwap(public_)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # finalize () -> ()
    def finalize(
        self,
    ):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.finalize()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # bind (address, uint256, uint256) -> ()
    def bind(self, token: Address, balance: int, denorm: int):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        token, balance, denorm = unsugar(token), unsugar(balance), unsugar(denorm)
        web3_fn = self.web3_contract.functions.bind(token, balance, denorm)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # rebind (address, uint256, uint256) -> ()
    def rebind(self, token: Address, balance: int, denorm: int):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        token, balance, denorm = unsugar(token), unsugar(balance), unsugar(denorm)
        web3_fn = self.web3_contract.functions.rebind(token, balance, denorm)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # unbind (address) -> ()
    def unbind(self, token: Address):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        token = unsugar(token)
        web3_fn = self.web3_contract.functions.unbind(token)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # gulp (address) -> ()
    def gulp(self, token: Address):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        token = unsugar(token)
        web3_fn = self.web3_contract.functions.gulp(token)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getSpotPrice (address, address) -> (uint256)
    def getSpotPrice(
        self, tokenIn: Address, tokenOut: Address
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenIn, tokenOut = unsugar(tokenIn), unsugar(tokenOut)
        web3_fn = self.web3_contract.functions.getSpotPrice(tokenIn, tokenOut)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getSpotPriceSansFee (address, address) -> (uint256)
    def getSpotPriceSansFee(
        self, tokenIn: Address, tokenOut: Address
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenIn, tokenOut = unsugar(tokenIn), unsugar(tokenOut)
        web3_fn = self.web3_contract.functions.getSpotPriceSansFee(tokenIn, tokenOut)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # joinPool (uint256, uint256[]) -> ()
    def joinPool(self, poolAmountOut: int, maxAmountsIn: List[int]):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        poolAmountOut, maxAmountsIn = unsugar(poolAmountOut), unsugar(maxAmountsIn)
        web3_fn = self.web3_contract.functions.joinPool(poolAmountOut, maxAmountsIn)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # exitPool (uint256, uint256[]) -> ()
    def exitPool(self, poolAmountIn: int, minAmountsOut: List[int]):
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        poolAmountIn, minAmountsOut = unsugar(poolAmountIn), unsugar(minAmountsOut)
        web3_fn = self.web3_contract.functions.exitPool(poolAmountIn, minAmountsOut)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactAmountIn (address, uint256, address, uint256, uint256) -> (uint256, uint256)
    def swapExactAmountIn(
        self,
        tokenIn: Address,
        tokenAmountIn: int,
        tokenOut: Address,
        minAmountOut: int,
        maxPrice: int,
    ) -> Function[SwapExactAmountInOutput, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenIn, tokenAmountIn, tokenOut, minAmountOut, maxPrice = (
            unsugar(tokenIn),
            unsugar(tokenAmountIn),
            unsugar(tokenOut),
            unsugar(minAmountOut),
            unsugar(maxPrice),
        )
        web3_fn = self.web3_contract.functions.swapExactAmountIn(
            tokenIn, tokenAmountIn, tokenOut, minAmountOut, maxPrice
        )

        def convert(args) -> SwapExactAmountInOutput:
            return SwapExactAmountInOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # swapExactAmountOut (address, uint256, address, uint256, uint256) -> (uint256, uint256)
    def swapExactAmountOut(
        self,
        tokenIn: Address,
        maxAmountIn: int,
        tokenOut: Address,
        tokenAmountOut: int,
        maxPrice: int,
    ) -> Function[SwapExactAmountOutOutput, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenIn, maxAmountIn, tokenOut, tokenAmountOut, maxPrice = (
            unsugar(tokenIn),
            unsugar(maxAmountIn),
            unsugar(tokenOut),
            unsugar(tokenAmountOut),
            unsugar(maxPrice),
        )
        web3_fn = self.web3_contract.functions.swapExactAmountOut(
            tokenIn, maxAmountIn, tokenOut, tokenAmountOut, maxPrice
        )

        def convert(args) -> SwapExactAmountOutOutput:
            return SwapExactAmountOutOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # joinswapExternAmountIn (address, uint256, uint256) -> (uint256)
    def joinswapExternAmountIn(
        self, tokenIn: Address, tokenAmountIn: int, minPoolAmountOut: int
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenIn, tokenAmountIn, minPoolAmountOut = (
            unsugar(tokenIn),
            unsugar(tokenAmountIn),
            unsugar(minPoolAmountOut),
        )
        web3_fn = self.web3_contract.functions.joinswapExternAmountIn(
            tokenIn, tokenAmountIn, minPoolAmountOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # joinswapPoolAmountOut (address, uint256, uint256) -> (uint256)
    def joinswapPoolAmountOut(
        self, tokenIn: Address, poolAmountOut: int, maxAmountIn: int
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenIn, poolAmountOut, maxAmountIn = (
            unsugar(tokenIn),
            unsugar(poolAmountOut),
            unsugar(maxAmountIn),
        )
        web3_fn = self.web3_contract.functions.joinswapPoolAmountOut(
            tokenIn, poolAmountOut, maxAmountIn
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # exitswapPoolAmountIn (address, uint256, uint256) -> (uint256)
    def exitswapPoolAmountIn(
        self, tokenOut: Address, poolAmountIn: int, minAmountOut: int
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenOut, poolAmountIn, minAmountOut = (
            unsugar(tokenOut),
            unsugar(poolAmountIn),
            unsugar(minAmountOut),
        )
        web3_fn = self.web3_contract.functions.exitswapPoolAmountIn(
            tokenOut, poolAmountIn, minAmountOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # exitswapExternAmountOut (address, uint256, uint256) -> (uint256)
    def exitswapExternAmountOut(
        self, tokenOut: Address, tokenAmountOut: int, maxPoolAmountIn: int
    ) -> Function[int, BPoolReceipt]:
        def make_receipt(receipt: TxReceipt) -> BPoolReceipt:
            return BPoolReceipt(receipt, BPoolReceiptEvents(self.contract, receipt))

        tokenOut, tokenAmountOut, maxPoolAmountIn = (
            unsugar(tokenOut),
            unsugar(tokenAmountOut),
            unsugar(maxPoolAmountIn),
        )
        web3_fn = self.web3_contract.functions.exitswapExternAmountOut(
            tokenOut, tokenAmountOut, maxPoolAmountIn
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BPoolCaller:
    def __init__(self, functions: BPoolFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BPoolCaller":
        return BPoolCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> int:
        return self.functions.allowance(src, dst).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> bool:
        return self.functions.approve(dst, amt).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> int:
        return self.functions.balanceOf(whom).call(self.transaction)

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        ).call(self.transaction)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # decreaseApproval (address, uint256) -> (bool)
    def decreaseApproval(self, dst: Address, amt: int) -> bool:
        return self.functions.decreaseApproval(dst, amt).call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # increaseApproval (address, uint256) -> (bool)
    def increaseApproval(self, dst: Address, amt: int) -> bool:
        return self.functions.increaseApproval(dst, amt).call(self.transaction)

    # name () -> (string)
    def name(
        self,
    ) -> Any:
        return self.functions.name().call(self.transaction)

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
    def transfer(self, dst: Address, amt: int) -> bool:
        return self.functions.transfer(dst, amt).call(self.transaction)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> bool:
        return self.functions.transferFrom(src, dst, amt).call(self.transaction)

    # isPublicSwap () -> (bool)
    def isPublicSwap(
        self,
    ) -> bool:
        return self.functions.isPublicSwap().call(self.transaction)

    # isFinalized () -> (bool)
    def isFinalized(
        self,
    ) -> bool:
        return self.functions.isFinalized().call(self.transaction)

    # isBound (address) -> (bool)
    def isBound(self, t: Address) -> bool:
        return self.functions.isBound(t).call(self.transaction)

    # getNumTokens () -> (uint256)
    def getNumTokens(
        self,
    ) -> int:
        return self.functions.getNumTokens().call(self.transaction)

    # getCurrentTokens () -> (address[])
    def getCurrentTokens(
        self,
    ) -> List[Address]:
        return self.functions.getCurrentTokens().call(self.transaction)

    # getFinalTokens () -> (address[])
    def getFinalTokens(
        self,
    ) -> List[Address]:
        return self.functions.getFinalTokens().call(self.transaction)

    # getDenormalizedWeight (address) -> (uint256)
    def getDenormalizedWeight(self, token: Address) -> int:
        return self.functions.getDenormalizedWeight(token).call(self.transaction)

    # getTotalDenormalizedWeight () -> (uint256)
    def getTotalDenormalizedWeight(
        self,
    ) -> int:
        return self.functions.getTotalDenormalizedWeight().call(self.transaction)

    # getNormalizedWeight (address) -> (uint256)
    def getNormalizedWeight(self, token: Address) -> int:
        return self.functions.getNormalizedWeight(token).call(self.transaction)

    # getBalance (address) -> (uint256)
    def getBalance(self, token: Address) -> int:
        return self.functions.getBalance(token).call(self.transaction)

    # getSwapFee () -> (uint256)
    def getSwapFee(
        self,
    ) -> int:
        return self.functions.getSwapFee().call(self.transaction)

    # getController () -> (address)
    def getController(
        self,
    ) -> Address:
        return self.functions.getController().call(self.transaction)

    # setSwapFee (uint256) -> ()
    def setSwapFee(self, swapFee: int):
        return self.functions.setSwapFee(swapFee).call(self.transaction)

    # setController (address) -> ()
    def setController(self, manager: Address):
        return self.functions.setController(manager).call(self.transaction)

    # setPublicSwap (bool) -> ()
    def setPublicSwap(self, public_: bool):
        return self.functions.setPublicSwap(public_).call(self.transaction)

    # finalize () -> ()
    def finalize(
        self,
    ):
        return self.functions.finalize().call(self.transaction)

    # bind (address, uint256, uint256) -> ()
    def bind(self, token: Address, balance: int, denorm: int):
        return self.functions.bind(token, balance, denorm).call(self.transaction)

    # rebind (address, uint256, uint256) -> ()
    def rebind(self, token: Address, balance: int, denorm: int):
        return self.functions.rebind(token, balance, denorm).call(self.transaction)

    # unbind (address) -> ()
    def unbind(self, token: Address):
        return self.functions.unbind(token).call(self.transaction)

    # gulp (address) -> ()
    def gulp(self, token: Address):
        return self.functions.gulp(token).call(self.transaction)

    # getSpotPrice (address, address) -> (uint256)
    def getSpotPrice(self, tokenIn: Address, tokenOut: Address) -> int:
        return self.functions.getSpotPrice(tokenIn, tokenOut).call(self.transaction)

    # getSpotPriceSansFee (address, address) -> (uint256)
    def getSpotPriceSansFee(self, tokenIn: Address, tokenOut: Address) -> int:
        return self.functions.getSpotPriceSansFee(tokenIn, tokenOut).call(
            self.transaction
        )

    # joinPool (uint256, uint256[]) -> ()
    def joinPool(self, poolAmountOut: int, maxAmountsIn: List[int]):
        return self.functions.joinPool(poolAmountOut, maxAmountsIn).call(
            self.transaction
        )

    # exitPool (uint256, uint256[]) -> ()
    def exitPool(self, poolAmountIn: int, minAmountsOut: List[int]):
        return self.functions.exitPool(poolAmountIn, minAmountsOut).call(
            self.transaction
        )

    # swapExactAmountIn (address, uint256, address, uint256, uint256) -> (uint256, uint256)
    def swapExactAmountIn(
        self,
        tokenIn: Address,
        tokenAmountIn: int,
        tokenOut: Address,
        minAmountOut: int,
        maxPrice: int,
    ) -> SwapExactAmountInOutput:
        return self.functions.swapExactAmountIn(
            tokenIn, tokenAmountIn, tokenOut, minAmountOut, maxPrice
        ).call(self.transaction)

    # swapExactAmountOut (address, uint256, address, uint256, uint256) -> (uint256, uint256)
    def swapExactAmountOut(
        self,
        tokenIn: Address,
        maxAmountIn: int,
        tokenOut: Address,
        tokenAmountOut: int,
        maxPrice: int,
    ) -> SwapExactAmountOutOutput:
        return self.functions.swapExactAmountOut(
            tokenIn, maxAmountIn, tokenOut, tokenAmountOut, maxPrice
        ).call(self.transaction)

    # joinswapExternAmountIn (address, uint256, uint256) -> (uint256)
    def joinswapExternAmountIn(
        self, tokenIn: Address, tokenAmountIn: int, minPoolAmountOut: int
    ) -> int:
        return self.functions.joinswapExternAmountIn(
            tokenIn, tokenAmountIn, minPoolAmountOut
        ).call(self.transaction)

    # joinswapPoolAmountOut (address, uint256, uint256) -> (uint256)
    def joinswapPoolAmountOut(
        self, tokenIn: Address, poolAmountOut: int, maxAmountIn: int
    ) -> int:
        return self.functions.joinswapPoolAmountOut(
            tokenIn, poolAmountOut, maxAmountIn
        ).call(self.transaction)

    # exitswapPoolAmountIn (address, uint256, uint256) -> (uint256)
    def exitswapPoolAmountIn(
        self, tokenOut: Address, poolAmountIn: int, minAmountOut: int
    ) -> int:
        return self.functions.exitswapPoolAmountIn(
            tokenOut, poolAmountIn, minAmountOut
        ).call(self.transaction)

    # exitswapExternAmountOut (address, uint256, uint256) -> (uint256)
    def exitswapExternAmountOut(
        self, tokenOut: Address, tokenAmountOut: int, maxPoolAmountIn: int
    ) -> int:
        return self.functions.exitswapExternAmountOut(
            tokenOut, tokenAmountOut, maxPoolAmountIn
        ).call(self.transaction)


# ---


class BPool(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BPool"]:
        if w3 is None:
            raise ValueError("In method BPool.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BPool.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BPool":
            return BPool(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BPool.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BPoolFunctions(w3, address, self.contract, self)
        self.call = BPoolCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> BPoolReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> BPoolReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> BPoolReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> BPoolReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> BPoolReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> BPoolReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> BPoolReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> BPoolReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> BPoolReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> BPoolReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> BPoolReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> BPoolReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> BPoolReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> BPoolReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> BPoolReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> BPoolReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> BPoolReceipt:
        return self.functions.allowance(src, dst).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> BPoolReceipt:
        return self.functions.approve(dst, amt).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> BPoolReceipt:
        return self.functions.balanceOf(whom).waitForReceipt()

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> BPoolReceipt:
        return self.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> BPoolReceipt:
        return self.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> BPoolReceipt:
        return self.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> BPoolReceipt:
        return self.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> BPoolReceipt:
        return self.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> BPoolReceipt:
        return self.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> BPoolReceipt:
        return self.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        ).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> BPoolReceipt:
        return self.functions.decimals().waitForReceipt()

    # decreaseApproval (address, uint256) -> (bool)
    def decreaseApproval(self, dst: Address, amt: int) -> BPoolReceipt:
        return self.functions.decreaseApproval(dst, amt).waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BPoolReceipt:
        return self.functions.getColor().waitForReceipt()

    # increaseApproval (address, uint256) -> (bool)
    def increaseApproval(self, dst: Address, amt: int) -> BPoolReceipt:
        return self.functions.increaseApproval(dst, amt).waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> BPoolReceipt:
        return self.functions.name().waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> BPoolReceipt:
        return self.functions.symbol().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> BPoolReceipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> BPoolReceipt:
        return self.functions.transfer(dst, amt).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> BPoolReceipt:
        return self.functions.transferFrom(src, dst, amt).waitForReceipt()

    # isPublicSwap () -> (bool)
    def isPublicSwap(
        self,
    ) -> BPoolReceipt:
        return self.functions.isPublicSwap().waitForReceipt()

    # isFinalized () -> (bool)
    def isFinalized(
        self,
    ) -> BPoolReceipt:
        return self.functions.isFinalized().waitForReceipt()

    # isBound (address) -> (bool)
    def isBound(self, t: Address) -> BPoolReceipt:
        return self.functions.isBound(t).waitForReceipt()

    # getNumTokens () -> (uint256)
    def getNumTokens(
        self,
    ) -> BPoolReceipt:
        return self.functions.getNumTokens().waitForReceipt()

    # getCurrentTokens () -> (address[])
    def getCurrentTokens(
        self,
    ) -> BPoolReceipt:
        return self.functions.getCurrentTokens().waitForReceipt()

    # getFinalTokens () -> (address[])
    def getFinalTokens(
        self,
    ) -> BPoolReceipt:
        return self.functions.getFinalTokens().waitForReceipt()

    # getDenormalizedWeight (address) -> (uint256)
    def getDenormalizedWeight(self, token: Address) -> BPoolReceipt:
        return self.functions.getDenormalizedWeight(token).waitForReceipt()

    # getTotalDenormalizedWeight () -> (uint256)
    def getTotalDenormalizedWeight(
        self,
    ) -> BPoolReceipt:
        return self.functions.getTotalDenormalizedWeight().waitForReceipt()

    # getNormalizedWeight (address) -> (uint256)
    def getNormalizedWeight(self, token: Address) -> BPoolReceipt:
        return self.functions.getNormalizedWeight(token).waitForReceipt()

    # getBalance (address) -> (uint256)
    def getBalance(self, token: Address) -> BPoolReceipt:
        return self.functions.getBalance(token).waitForReceipt()

    # getSwapFee () -> (uint256)
    def getSwapFee(
        self,
    ) -> BPoolReceipt:
        return self.functions.getSwapFee().waitForReceipt()

    # getController () -> (address)
    def getController(
        self,
    ) -> BPoolReceipt:
        return self.functions.getController().waitForReceipt()

    # setSwapFee (uint256) -> ()
    def setSwapFee(self, swapFee: int) -> BPoolReceipt:
        return self.functions.setSwapFee(swapFee).waitForReceipt()

    # setController (address) -> ()
    def setController(self, manager: Address) -> BPoolReceipt:
        return self.functions.setController(manager).waitForReceipt()

    # setPublicSwap (bool) -> ()
    def setPublicSwap(self, public_: bool) -> BPoolReceipt:
        return self.functions.setPublicSwap(public_).waitForReceipt()

    # finalize () -> ()
    def finalize(
        self,
    ) -> BPoolReceipt:
        return self.functions.finalize().waitForReceipt()

    # bind (address, uint256, uint256) -> ()
    def bind(self, token: Address, balance: int, denorm: int) -> BPoolReceipt:
        return self.functions.bind(token, balance, denorm).waitForReceipt()

    # rebind (address, uint256, uint256) -> ()
    def rebind(self, token: Address, balance: int, denorm: int) -> BPoolReceipt:
        return self.functions.rebind(token, balance, denorm).waitForReceipt()

    # unbind (address) -> ()
    def unbind(self, token: Address) -> BPoolReceipt:
        return self.functions.unbind(token).waitForReceipt()

    # gulp (address) -> ()
    def gulp(self, token: Address) -> BPoolReceipt:
        return self.functions.gulp(token).waitForReceipt()

    # getSpotPrice (address, address) -> (uint256)
    def getSpotPrice(self, tokenIn: Address, tokenOut: Address) -> BPoolReceipt:
        return self.functions.getSpotPrice(tokenIn, tokenOut).waitForReceipt()

    # getSpotPriceSansFee (address, address) -> (uint256)
    def getSpotPriceSansFee(self, tokenIn: Address, tokenOut: Address) -> BPoolReceipt:
        return self.functions.getSpotPriceSansFee(tokenIn, tokenOut).waitForReceipt()

    # joinPool (uint256, uint256[]) -> ()
    def joinPool(self, poolAmountOut: int, maxAmountsIn: List[int]) -> BPoolReceipt:
        return self.functions.joinPool(poolAmountOut, maxAmountsIn).waitForReceipt()

    # exitPool (uint256, uint256[]) -> ()
    def exitPool(self, poolAmountIn: int, minAmountsOut: List[int]) -> BPoolReceipt:
        return self.functions.exitPool(poolAmountIn, minAmountsOut).waitForReceipt()

    # swapExactAmountIn (address, uint256, address, uint256, uint256) -> (uint256, uint256)
    def swapExactAmountIn(
        self,
        tokenIn: Address,
        tokenAmountIn: int,
        tokenOut: Address,
        minAmountOut: int,
        maxPrice: int,
    ) -> BPoolReceipt:
        return self.functions.swapExactAmountIn(
            tokenIn, tokenAmountIn, tokenOut, minAmountOut, maxPrice
        ).waitForReceipt()

    # swapExactAmountOut (address, uint256, address, uint256, uint256) -> (uint256, uint256)
    def swapExactAmountOut(
        self,
        tokenIn: Address,
        maxAmountIn: int,
        tokenOut: Address,
        tokenAmountOut: int,
        maxPrice: int,
    ) -> BPoolReceipt:
        return self.functions.swapExactAmountOut(
            tokenIn, maxAmountIn, tokenOut, tokenAmountOut, maxPrice
        ).waitForReceipt()

    # joinswapExternAmountIn (address, uint256, uint256) -> (uint256)
    def joinswapExternAmountIn(
        self, tokenIn: Address, tokenAmountIn: int, minPoolAmountOut: int
    ) -> BPoolReceipt:
        return self.functions.joinswapExternAmountIn(
            tokenIn, tokenAmountIn, minPoolAmountOut
        ).waitForReceipt()

    # joinswapPoolAmountOut (address, uint256, uint256) -> (uint256)
    def joinswapPoolAmountOut(
        self, tokenIn: Address, poolAmountOut: int, maxAmountIn: int
    ) -> BPoolReceipt:
        return self.functions.joinswapPoolAmountOut(
            tokenIn, poolAmountOut, maxAmountIn
        ).waitForReceipt()

    # exitswapPoolAmountIn (address, uint256, uint256) -> (uint256)
    def exitswapPoolAmountIn(
        self, tokenOut: Address, poolAmountIn: int, minAmountOut: int
    ) -> BPoolReceipt:
        return self.functions.exitswapPoolAmountIn(
            tokenOut, poolAmountIn, minAmountOut
        ).waitForReceipt()

    # exitswapExternAmountOut (address, uint256, uint256) -> (uint256)
    def exitswapExternAmountOut(
        self, tokenOut: Address, tokenAmountOut: int, maxPoolAmountIn: int
    ) -> BPoolReceipt:
        return self.functions.exitswapExternAmountOut(
            tokenOut, tokenAmountOut, maxPoolAmountIn
        ).waitForReceipt()


# --------- end BPool ----------


# ---------------------------------------------------------------
# BToken

# ---
@dataclass
class BTokenReceiptEvents:
    contract: "BToken"
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
class BTokenReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: BTokenReceiptEvents


# ---


class BTokenFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "BToken"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        src, dst = unsugar(src), unsugar(dst)
        web3_fn = self.web3_contract.functions.allowance(src, dst)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        whom = unsugar(whom)
        web3_fn = self.web3_contract.functions.balanceOf(whom)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> Function[bool, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.approve(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # increaseApproval (address, uint256) -> (bool)
    def increaseApproval(self, dst: Address, amt: int) -> Function[bool, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.increaseApproval(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decreaseApproval (address, uint256) -> (bool)
    def decreaseApproval(self, dst: Address, amt: int) -> Function[bool, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.decreaseApproval(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> Function[bool, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        dst, amt = unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transfer(dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, src: Address, dst: Address, amt: int
    ) -> Function[bool, BTokenReceipt]:
        def make_receipt(receipt: TxReceipt) -> BTokenReceipt:
            return BTokenReceipt(receipt, BTokenReceiptEvents(self.contract, receipt))

        src, dst, amt = unsugar(src), unsugar(dst), unsugar(amt)
        web3_fn = self.web3_contract.functions.transferFrom(src, dst, amt)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BTokenCaller:
    def __init__(self, functions: BTokenFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BTokenCaller":
        return BTokenCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # name () -> (string)
    def name(
        self,
    ) -> Any:
        return self.functions.name().call(self.transaction)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Any:
        return self.functions.symbol().call(self.transaction)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> int:
        return self.functions.allowance(src, dst).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> int:
        return self.functions.balanceOf(whom).call(self.transaction)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> int:
        return self.functions.totalSupply().call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> bool:
        return self.functions.approve(dst, amt).call(self.transaction)

    # increaseApproval (address, uint256) -> (bool)
    def increaseApproval(self, dst: Address, amt: int) -> bool:
        return self.functions.increaseApproval(dst, amt).call(self.transaction)

    # decreaseApproval (address, uint256) -> (bool)
    def decreaseApproval(self, dst: Address, amt: int) -> bool:
        return self.functions.decreaseApproval(dst, amt).call(self.transaction)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> bool:
        return self.functions.transfer(dst, amt).call(self.transaction)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> bool:
        return self.functions.transferFrom(src, dst, amt).call(self.transaction)


# ---


class BToken(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BToken"]:
        if w3 is None:
            raise ValueError("In method BToken.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BToken.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BToken":
            return BToken(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BToken.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BTokenFunctions(w3, address, self.contract, self)
        self.call = BTokenCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> BTokenReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> BTokenReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> BTokenReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> BTokenReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> BTokenReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> BTokenReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> BTokenReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> BTokenReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> BTokenReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> BTokenReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> BTokenReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> BTokenReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> BTokenReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> BTokenReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> BTokenReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> BTokenReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BTokenReceipt:
        return self.functions.getColor().waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> BTokenReceipt:
        return self.functions.name().waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> BTokenReceipt:
        return self.functions.symbol().waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> BTokenReceipt:
        return self.functions.decimals().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, src: Address, dst: Address) -> BTokenReceipt:
        return self.functions.allowance(src, dst).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, whom: Address) -> BTokenReceipt:
        return self.functions.balanceOf(whom).waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> BTokenReceipt:
        return self.functions.totalSupply().waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, dst: Address, amt: int) -> BTokenReceipt:
        return self.functions.approve(dst, amt).waitForReceipt()

    # increaseApproval (address, uint256) -> (bool)
    def increaseApproval(self, dst: Address, amt: int) -> BTokenReceipt:
        return self.functions.increaseApproval(dst, amt).waitForReceipt()

    # decreaseApproval (address, uint256) -> (bool)
    def decreaseApproval(self, dst: Address, amt: int) -> BTokenReceipt:
        return self.functions.decreaseApproval(dst, amt).waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, amt: int) -> BTokenReceipt:
        return self.functions.transfer(dst, amt).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, amt: int) -> BTokenReceipt:
        return self.functions.transferFrom(src, dst, amt).waitForReceipt()


# --------- end BToken ----------


# ---------------------------------------------------------------
# BMath

# ---
@dataclass
class BMathReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class BMathFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "BMath"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.BONE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.BPOW_PRECISION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.EXIT_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.INIT_POOL_SUPPLY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_IN_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_OUT_RATIO()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_TOTAL_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MAX_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BALANCE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BOUND_TOKENS()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_BPOW_BASE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_FEE()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.MIN_WEIGHT()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        web3_fn = self.web3_contract.functions.getColor()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(tokenAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(tokenAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(tokenAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        (
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceIn),
            unsugar(tokenWeightIn),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(poolAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        (
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ) = (
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(poolAmountIn),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> Function[int, BMathReceipt]:
        def make_receipt(receipt: TxReceipt) -> BMathReceipt:
            return BMathReceipt(receipt)

        (
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ) = (
            unsugar(tokenBalanceOut),
            unsugar(tokenWeightOut),
            unsugar(poolSupply),
            unsugar(totalWeight),
            unsugar(tokenAmountOut),
            unsugar(swapFee),
        )
        web3_fn = self.web3_contract.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class BMathCaller:
    def __init__(self, functions: BMathFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "BMathCaller":
        return BMathCaller(functions=self.functions, transaction=transaction)

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> int:
        return self.functions.BONE().call(self.transaction)

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> int:
        return self.functions.BPOW_PRECISION().call(self.transaction)

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> int:
        return self.functions.EXIT_FEE().call(self.transaction)

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> int:
        return self.functions.INIT_POOL_SUPPLY().call(self.transaction)

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MAX_BOUND_TOKENS().call(self.transaction)

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MAX_BPOW_BASE().call(self.transaction)

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> int:
        return self.functions.MAX_FEE().call(self.transaction)

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_IN_RATIO().call(self.transaction)

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> int:
        return self.functions.MAX_OUT_RATIO().call(self.transaction)

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_TOTAL_WEIGHT().call(self.transaction)

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> int:
        return self.functions.MAX_WEIGHT().call(self.transaction)

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> int:
        return self.functions.MIN_BALANCE().call(self.transaction)

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> int:
        return self.functions.MIN_BOUND_TOKENS().call(self.transaction)

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> int:
        return self.functions.MIN_BPOW_BASE().call(self.transaction)

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> int:
        return self.functions.MIN_FEE().call(self.transaction)

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> int:
        return self.functions.MIN_WEIGHT().call(self.transaction)

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.getColor().call(self.transaction)

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        ).call(self.transaction)

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ).call(self.transaction)

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ).call(self.transaction)

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> int:
        return self.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ).call(self.transaction)


# ---


class BMath(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["BMath"]:
        if w3 is None:
            raise ValueError("In method BMath.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("core/BMath.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "BMath":
            return BMath(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/BMath.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = BMathFunctions(w3, address, self.contract, self)
        self.call = BMathCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # BONE () -> (uint256)
    def BONE(
        self,
    ) -> BMathReceipt:
        return self.functions.BONE().waitForReceipt()

    # BPOW_PRECISION () -> (uint256)
    def BPOW_PRECISION(
        self,
    ) -> BMathReceipt:
        return self.functions.BPOW_PRECISION().waitForReceipt()

    # EXIT_FEE () -> (uint256)
    def EXIT_FEE(
        self,
    ) -> BMathReceipt:
        return self.functions.EXIT_FEE().waitForReceipt()

    # INIT_POOL_SUPPLY () -> (uint256)
    def INIT_POOL_SUPPLY(
        self,
    ) -> BMathReceipt:
        return self.functions.INIT_POOL_SUPPLY().waitForReceipt()

    # MAX_BOUND_TOKENS () -> (uint256)
    def MAX_BOUND_TOKENS(
        self,
    ) -> BMathReceipt:
        return self.functions.MAX_BOUND_TOKENS().waitForReceipt()

    # MAX_BPOW_BASE () -> (uint256)
    def MAX_BPOW_BASE(
        self,
    ) -> BMathReceipt:
        return self.functions.MAX_BPOW_BASE().waitForReceipt()

    # MAX_FEE () -> (uint256)
    def MAX_FEE(
        self,
    ) -> BMathReceipt:
        return self.functions.MAX_FEE().waitForReceipt()

    # MAX_IN_RATIO () -> (uint256)
    def MAX_IN_RATIO(
        self,
    ) -> BMathReceipt:
        return self.functions.MAX_IN_RATIO().waitForReceipt()

    # MAX_OUT_RATIO () -> (uint256)
    def MAX_OUT_RATIO(
        self,
    ) -> BMathReceipt:
        return self.functions.MAX_OUT_RATIO().waitForReceipt()

    # MAX_TOTAL_WEIGHT () -> (uint256)
    def MAX_TOTAL_WEIGHT(
        self,
    ) -> BMathReceipt:
        return self.functions.MAX_TOTAL_WEIGHT().waitForReceipt()

    # MAX_WEIGHT () -> (uint256)
    def MAX_WEIGHT(
        self,
    ) -> BMathReceipt:
        return self.functions.MAX_WEIGHT().waitForReceipt()

    # MIN_BALANCE () -> (uint256)
    def MIN_BALANCE(
        self,
    ) -> BMathReceipt:
        return self.functions.MIN_BALANCE().waitForReceipt()

    # MIN_BOUND_TOKENS () -> (uint256)
    def MIN_BOUND_TOKENS(
        self,
    ) -> BMathReceipt:
        return self.functions.MIN_BOUND_TOKENS().waitForReceipt()

    # MIN_BPOW_BASE () -> (uint256)
    def MIN_BPOW_BASE(
        self,
    ) -> BMathReceipt:
        return self.functions.MIN_BPOW_BASE().waitForReceipt()

    # MIN_FEE () -> (uint256)
    def MIN_FEE(
        self,
    ) -> BMathReceipt:
        return self.functions.MIN_FEE().waitForReceipt()

    # MIN_WEIGHT () -> (uint256)
    def MIN_WEIGHT(
        self,
    ) -> BMathReceipt:
        return self.functions.MIN_WEIGHT().waitForReceipt()

    # getColor () -> (bytes32)
    def getColor(
        self,
    ) -> BMathReceipt:
        return self.functions.getColor().waitForReceipt()

    # calcSpotPrice (uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSpotPrice(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        swapFee: int,
    ) -> BMathReceipt:
        return self.functions.calcSpotPrice(
            tokenBalanceIn, tokenWeightIn, tokenBalanceOut, tokenWeightOut, swapFee
        ).waitForReceipt()

    # calcOutGivenIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcOutGivenIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> BMathReceipt:
        return self.functions.calcOutGivenIn(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcInGivenOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcInGivenOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> BMathReceipt:
        return self.functions.calcInGivenOut(
            tokenBalanceIn,
            tokenWeightIn,
            tokenBalanceOut,
            tokenWeightOut,
            tokenAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcPoolOutGivenSingleIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolOutGivenSingleIn(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountIn: int,
        swapFee: int,
    ) -> BMathReceipt:
        return self.functions.calcPoolOutGivenSingleIn(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            tokenAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcSingleInGivenPoolOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleInGivenPoolOut(
        self,
        tokenBalanceIn: int,
        tokenWeightIn: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountOut: int,
        swapFee: int,
    ) -> BMathReceipt:
        return self.functions.calcSingleInGivenPoolOut(
            tokenBalanceIn,
            tokenWeightIn,
            poolSupply,
            totalWeight,
            poolAmountOut,
            swapFee,
        ).waitForReceipt()

    # calcSingleOutGivenPoolIn (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcSingleOutGivenPoolIn(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        poolAmountIn: int,
        swapFee: int,
    ) -> BMathReceipt:
        return self.functions.calcSingleOutGivenPoolIn(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            poolAmountIn,
            swapFee,
        ).waitForReceipt()

    # calcPoolInGivenSingleOut (uint256, uint256, uint256, uint256, uint256, uint256) -> (uint256)
    def calcPoolInGivenSingleOut(
        self,
        tokenBalanceOut: int,
        tokenWeightOut: int,
        poolSupply: int,
        totalWeight: int,
        tokenAmountOut: int,
        swapFee: int,
    ) -> BMathReceipt:
        return self.functions.calcPoolInGivenSingleOut(
            tokenBalanceOut,
            tokenWeightOut,
            poolSupply,
            totalWeight,
            tokenAmountOut,
            swapFee,
        ).waitForReceipt()


# --------- end BMath ----------
