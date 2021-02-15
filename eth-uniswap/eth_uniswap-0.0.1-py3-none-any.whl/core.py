# SPDX-License-Identifier: GPL-3.0-only
# © Copyright 2021 Julien Harbulot
# see: https://github.com/julien-h/python-eth-uniswap
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
# IUniswapV2ERC20

# ---
@dataclass
class IUniswapV2ERC20ReceiptEvents:
    contract: "IUniswapV2ERC20"
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
class IUniswapV2ERC20Receipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: IUniswapV2ERC20ReceiptEvents


# ---


class IUniswapV2ERC20Functions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "IUniswapV2ERC20"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.DOMAIN_SEPARATOR()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.PERMIT_TYPEHASH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(
        self, owner: Address, spender: Address
    ) -> Function[int, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        owner, spender = unsugar(owner), unsugar(spender)
        web3_fn = self.web3_contract.functions.allowance(owner, spender)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(
        self, spender: Address, value: int
    ) -> Function[bool, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> Function[int, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        owner = unsugar(owner)
        web3_fn = self.web3_contract.functions.balanceOf(owner)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # nonces (address) -> (uint256)
    def nonces(self, owner: Address) -> Function[int, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        owner = unsugar(owner)
        web3_fn = self.web3_contract.functions.nonces(owner)
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
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

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
    ) -> Function[Any, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(
        self, to: Address, value: int
    ) -> Function[bool, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, IUniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2ERC20Receipt:
            return IUniswapV2ERC20Receipt(
                receipt, IUniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV2ERC20Caller:
    def __init__(self, functions: IUniswapV2ERC20Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV2ERC20Caller":
        return IUniswapV2ERC20Caller(functions=self.functions, transaction=transaction)

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
    def allowance(self, owner: Address, spender: Address) -> int:
        return self.functions.allowance(owner, spender).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> bool:
        return self.functions.approve(spender, value).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> int:
        return self.functions.balanceOf(owner).call(self.transaction)

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
    def nonces(self, owner: Address) -> int:
        return self.functions.nonces(owner).call(self.transaction)

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


class IUniswapV2ERC20(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV2ERC20"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV2ERC20.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/IUniswapV2ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2ERC20":
            return IUniswapV2ERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/IUniswapV2ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV2ERC20Functions(w3, address, self.contract, self)
        self.call = IUniswapV2ERC20Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.DOMAIN_SEPARATOR().waitForReceipt()

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.PERMIT_TYPEHASH().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, owner: Address, spender: Address) -> IUniswapV2ERC20Receipt:
        return self.functions.allowance(owner, spender).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> IUniswapV2ERC20Receipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> IUniswapV2ERC20Receipt:
        return self.functions.balanceOf(owner).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.decimals().waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.name().waitForReceipt()

    # nonces (address) -> (uint256)
    def nonces(self, owner: Address) -> IUniswapV2ERC20Receipt:
        return self.functions.nonces(owner).waitForReceipt()

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
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.permit(
            owner, spender, value, deadline, v, r, s
        ).waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.symbol().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> IUniswapV2ERC20Receipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> IUniswapV2ERC20Receipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end IUniswapV2ERC20 ----------


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

    # allowance (address, address) -> (uint256)
    def allowance(
        self, owner: Address, spender: Address
    ) -> Function[int, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        owner, spender = unsugar(owner), unsugar(spender)
        web3_fn = self.web3_contract.functions.allowance(owner, spender)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> Function[bool, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> Function[int, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        owner = unsugar(owner)
        web3_fn = self.web3_contract.functions.balanceOf(owner)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> Function[bool, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, IERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> IERC20Receipt:
            return IERC20Receipt(receipt, IERC20ReceiptEvents(self.contract, receipt))

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IERC20Caller:
    def __init__(self, functions: IERC20Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IERC20Caller":
        return IERC20Caller(functions=self.functions, transaction=transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, owner: Address, spender: Address) -> int:
        return self.functions.allowance(owner, spender).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> bool:
        return self.functions.approve(spender, value).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> int:
        return self.functions.balanceOf(owner).call(self.transaction)

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

    # allowance (address, address) -> (uint256)
    def allowance(self, owner: Address, spender: Address) -> IERC20Receipt:
        return self.functions.allowance(owner, spender).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> IERC20Receipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> IERC20Receipt:
        return self.functions.balanceOf(owner).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> IERC20Receipt:
        return self.functions.decimals().waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> IERC20Receipt:
        return self.functions.name().waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> IERC20Receipt:
        return self.functions.symbol().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> IERC20Receipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> IERC20Receipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, from_: Address, to: Address, value: int) -> IERC20Receipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end IERC20 ----------


# ---------------------------------------------------------------
# IUniswapV2Pair

BurnOutput = namedtuple(
    "BurnOutput", [x.strip() for x in " amount0, amount1".split(",")]
)
GetReservesOutput = namedtuple(
    "GetReservesOutput",
    [x.strip() for x in " reserve0, reserve1, blockTimestampLast".split(",")],
)
# ---
@dataclass
class IUniswapV2PairReceiptEvents:
    contract: "IUniswapV2Pair"
    web3_receipt: TxReceipt

    def Approval(self) -> Any:
        return (
            self.contract.to_web3().events.Approval().processReceipt(self.web3_receipt)
        )

    def Burn(self) -> Any:
        return self.contract.to_web3().events.Burn().processReceipt(self.web3_receipt)

    def Mint(self) -> Any:
        return self.contract.to_web3().events.Mint().processReceipt(self.web3_receipt)

    def Swap(self) -> Any:
        return self.contract.to_web3().events.Swap().processReceipt(self.web3_receipt)

    def Sync(self) -> Any:
        return self.contract.to_web3().events.Sync().processReceipt(self.web3_receipt)

    def Transfer(self) -> Any:
        return (
            self.contract.to_web3().events.Transfer().processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class IUniswapV2PairReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: IUniswapV2PairReceiptEvents


# ---


class IUniswapV2PairFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "IUniswapV2Pair"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.DOMAIN_SEPARATOR()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MINIMUM_LIQUIDITY () -> (uint256)
    def MINIMUM_LIQUIDITY(
        self,
    ) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MINIMUM_LIQUIDITY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.PERMIT_TYPEHASH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(
        self, owner: Address, spender: Address
    ) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        owner, spender = unsugar(owner), unsugar(spender)
        web3_fn = self.web3_contract.functions.allowance(owner, spender)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(
        self, spender: Address, value: int
    ) -> Function[bool, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        owner = unsugar(owner)
        web3_fn = self.web3_contract.functions.balanceOf(owner)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # burn (address) -> (uint256, uint256)
    def burn(self, to: Address) -> Function[BurnOutput, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to = unsugar(to)
        web3_fn = self.web3_contract.functions.burn(to)

        def convert(args) -> BurnOutput:
            return BurnOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getReserves () -> (uint112, uint112, uint32)
    def getReserves(
        self,
    ) -> Function[GetReservesOutput, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.getReserves()

        def convert(args) -> GetReservesOutput:
            return GetReservesOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # initialize (address, address) -> ()
    def initialize(self, item0: Address, item1: Address):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.initialize(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # kLast () -> (uint256)
    def kLast(
        self,
    ) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.kLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # mint (address) -> (uint256)
    def mint(self, to: Address) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to = unsugar(to)
        web3_fn = self.web3_contract.functions.mint(to)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # nonces (address) -> (uint256)
    def nonces(self, owner: Address) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        owner = unsugar(owner)
        web3_fn = self.web3_contract.functions.nonces(owner)
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
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

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

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.price0CumulativeLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.price1CumulativeLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # skim (address) -> ()
    def skim(self, to: Address):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to = unsugar(to)
        web3_fn = self.web3_contract.functions.skim(to)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swap (uint256, uint256, address, bytes) -> ()
    def swap(
        self,
        amount0Out: int,
        amount1Out: int,
        to: Address,
        data: Union[bytearray, str, HexBytes],
    ):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        amount0Out, amount1Out, to, data = (
            unsugar(amount0Out),
            unsugar(amount1Out),
            unsugar(to),
            unsugar(data),
        )
        web3_fn = self.web3_contract.functions.swap(amount0Out, amount1Out, to, data)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # sync () -> ()
    def sync(
        self,
    ):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.sync()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # token0 () -> (address)
    def token0(
        self,
    ) -> Function[Address, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.token0()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # token1 () -> (address)
    def token1(
        self,
    ) -> Function[Address, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.token1()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(
        self, to: Address, value: int
    ) -> Function[bool, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, IUniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2PairReceipt:
            return IUniswapV2PairReceipt(
                receipt, IUniswapV2PairReceiptEvents(self.contract, receipt)
            )

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV2PairCaller:
    def __init__(self, functions: IUniswapV2PairFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV2PairCaller":
        return IUniswapV2PairCaller(functions=self.functions, transaction=transaction)

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.DOMAIN_SEPARATOR().call(self.transaction)

    # MINIMUM_LIQUIDITY () -> (uint256)
    def MINIMUM_LIQUIDITY(
        self,
    ) -> int:
        return self.functions.MINIMUM_LIQUIDITY().call(self.transaction)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.PERMIT_TYPEHASH().call(self.transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, owner: Address, spender: Address) -> int:
        return self.functions.allowance(owner, spender).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> bool:
        return self.functions.approve(spender, value).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> int:
        return self.functions.balanceOf(owner).call(self.transaction)

    # burn (address) -> (uint256, uint256)
    def burn(self, to: Address) -> BurnOutput:
        return self.functions.burn(to).call(self.transaction)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # getReserves () -> (uint112, uint112, uint32)
    def getReserves(
        self,
    ) -> GetReservesOutput:
        return self.functions.getReserves().call(self.transaction)

    # initialize (address, address) -> ()
    def initialize(self, item0: Address, item1: Address):
        return self.functions.initialize(item0, item1).call(self.transaction)

    # kLast () -> (uint256)
    def kLast(
        self,
    ) -> int:
        return self.functions.kLast().call(self.transaction)

    # mint (address) -> (uint256)
    def mint(self, to: Address) -> int:
        return self.functions.mint(to).call(self.transaction)

    # name () -> (string)
    def name(
        self,
    ) -> Any:
        return self.functions.name().call(self.transaction)

    # nonces (address) -> (uint256)
    def nonces(self, owner: Address) -> int:
        return self.functions.nonces(owner).call(self.transaction)

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

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> int:
        return self.functions.price0CumulativeLast().call(self.transaction)

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> int:
        return self.functions.price1CumulativeLast().call(self.transaction)

    # skim (address) -> ()
    def skim(self, to: Address):
        return self.functions.skim(to).call(self.transaction)

    # swap (uint256, uint256, address, bytes) -> ()
    def swap(
        self,
        amount0Out: int,
        amount1Out: int,
        to: Address,
        data: Union[bytearray, str, HexBytes],
    ):
        return self.functions.swap(amount0Out, amount1Out, to, data).call(
            self.transaction
        )

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Any:
        return self.functions.symbol().call(self.transaction)

    # sync () -> ()
    def sync(
        self,
    ):
        return self.functions.sync().call(self.transaction)

    # token0 () -> (address)
    def token0(
        self,
    ) -> Address:
        return self.functions.token0().call(self.transaction)

    # token1 () -> (address)
    def token1(
        self,
    ) -> Address:
        return self.functions.token1().call(self.transaction)

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


class IUniswapV2Pair(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV2Pair"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV2Pair.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/IUniswapV2Pair.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Pair":
            return IUniswapV2Pair(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/IUniswapV2Pair.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV2PairFunctions(w3, address, self.contract, self)
        self.call = IUniswapV2PairCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.DOMAIN_SEPARATOR().waitForReceipt()

    # MINIMUM_LIQUIDITY () -> (uint256)
    def MINIMUM_LIQUIDITY(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.MINIMUM_LIQUIDITY().waitForReceipt()

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.PERMIT_TYPEHASH().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, owner: Address, spender: Address) -> IUniswapV2PairReceipt:
        return self.functions.allowance(owner, spender).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> IUniswapV2PairReceipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> IUniswapV2PairReceipt:
        return self.functions.balanceOf(owner).waitForReceipt()

    # burn (address) -> (uint256, uint256)
    def burn(self, to: Address) -> IUniswapV2PairReceipt:
        return self.functions.burn(to).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.decimals().waitForReceipt()

    # factory () -> (address)
    def factory(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.factory().waitForReceipt()

    # getReserves () -> (uint112, uint112, uint32)
    def getReserves(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.getReserves().waitForReceipt()

    # initialize (address, address) -> ()
    def initialize(self, item0: Address, item1: Address) -> IUniswapV2PairReceipt:
        return self.functions.initialize(item0, item1).waitForReceipt()

    # kLast () -> (uint256)
    def kLast(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.kLast().waitForReceipt()

    # mint (address) -> (uint256)
    def mint(self, to: Address) -> IUniswapV2PairReceipt:
        return self.functions.mint(to).waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.name().waitForReceipt()

    # nonces (address) -> (uint256)
    def nonces(self, owner: Address) -> IUniswapV2PairReceipt:
        return self.functions.nonces(owner).waitForReceipt()

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
    ) -> IUniswapV2PairReceipt:
        return self.functions.permit(
            owner, spender, value, deadline, v, r, s
        ).waitForReceipt()

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.price0CumulativeLast().waitForReceipt()

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.price1CumulativeLast().waitForReceipt()

    # skim (address) -> ()
    def skim(self, to: Address) -> IUniswapV2PairReceipt:
        return self.functions.skim(to).waitForReceipt()

    # swap (uint256, uint256, address, bytes) -> ()
    def swap(
        self,
        amount0Out: int,
        amount1Out: int,
        to: Address,
        data: Union[bytearray, str, HexBytes],
    ) -> IUniswapV2PairReceipt:
        return self.functions.swap(amount0Out, amount1Out, to, data).waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.symbol().waitForReceipt()

    # sync () -> ()
    def sync(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.sync().waitForReceipt()

    # token0 () -> (address)
    def token0(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.token0().waitForReceipt()

    # token1 () -> (address)
    def token1(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.token1().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> IUniswapV2PairReceipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> IUniswapV2PairReceipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> IUniswapV2PairReceipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end IUniswapV2Pair ----------


# ---------------------------------------------------------------
# UniswapV2Pair

BurnOutput = namedtuple(
    "BurnOutput", [x.strip() for x in " amount0, amount1".split(",")]
)
GetReservesOutput = namedtuple(
    "GetReservesOutput",
    [x.strip() for x in " reserve0, reserve1, blockTimestampLast".split(",")],
)
# ---
@dataclass
class UniswapV2PairReceiptEvents:
    contract: "UniswapV2Pair"
    web3_receipt: TxReceipt

    def Approval(self) -> Any:
        return (
            self.contract.to_web3().events.Approval().processReceipt(self.web3_receipt)
        )

    def Burn(self) -> Any:
        return self.contract.to_web3().events.Burn().processReceipt(self.web3_receipt)

    def Mint(self) -> Any:
        return self.contract.to_web3().events.Mint().processReceipt(self.web3_receipt)

    def Swap(self) -> Any:
        return self.contract.to_web3().events.Swap().processReceipt(self.web3_receipt)

    def Sync(self) -> Any:
        return self.contract.to_web3().events.Sync().processReceipt(self.web3_receipt)

    def Transfer(self) -> Any:
        return (
            self.contract.to_web3().events.Transfer().processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class UniswapV2PairReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: UniswapV2PairReceiptEvents


# ---


class UniswapV2PairFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV2Pair"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.DOMAIN_SEPARATOR()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # MINIMUM_LIQUIDITY () -> (uint256)
    def MINIMUM_LIQUIDITY(
        self,
    ) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.MINIMUM_LIQUIDITY()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.PERMIT_TYPEHASH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(
        self, item0: Address, item1: Address
    ) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.allowance(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(
        self, spender: Address, value: int
    ) -> Function[bool, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.balanceOf(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # burn (address) -> (uint256, uint256)
    def burn(self, to: Address) -> Function[BurnOutput, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to = unsugar(to)
        web3_fn = self.web3_contract.functions.burn(to)

        def convert(args) -> BurnOutput:
            return BurnOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getReserves () -> (uint112, uint112, uint32)
    def getReserves(
        self,
    ) -> Function[GetReservesOutput, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.getReserves()

        def convert(args) -> GetReservesOutput:
            return GetReservesOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # initialize (address, address) -> ()
    def initialize(self, token0: Address, token1: Address):
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        token0, token1 = unsugar(token0), unsugar(token1)
        web3_fn = self.web3_contract.functions.initialize(token0, token1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # kLast () -> (uint256)
    def kLast(
        self,
    ) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.kLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # mint (address) -> (uint256)
    def mint(self, to: Address) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to = unsugar(to)
        web3_fn = self.web3_contract.functions.mint(to)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

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
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

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

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.price0CumulativeLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.price1CumulativeLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # skim (address) -> ()
    def skim(self, to: Address):
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to = unsugar(to)
        web3_fn = self.web3_contract.functions.skim(to)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swap (uint256, uint256, address, bytes) -> ()
    def swap(
        self,
        amount0Out: int,
        amount1Out: int,
        to: Address,
        data: Union[bytearray, str, HexBytes],
    ):
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        amount0Out, amount1Out, to, data = (
            unsugar(amount0Out),
            unsugar(amount1Out),
            unsugar(to),
            unsugar(data),
        )
        web3_fn = self.web3_contract.functions.swap(amount0Out, amount1Out, to, data)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # sync () -> ()
    def sync(
        self,
    ):
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.sync()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # token0 () -> (address)
    def token0(
        self,
    ) -> Function[Address, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.token0()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # token1 () -> (address)
    def token1(
        self,
    ) -> Function[Address, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.token1()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> Function[bool, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, UniswapV2PairReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2PairReceipt:
            return UniswapV2PairReceipt(
                receipt, UniswapV2PairReceiptEvents(self.contract, receipt)
            )

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV2PairCaller:
    def __init__(self, functions: UniswapV2PairFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV2PairCaller":
        return UniswapV2PairCaller(functions=self.functions, transaction=transaction)

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.DOMAIN_SEPARATOR().call(self.transaction)

    # MINIMUM_LIQUIDITY () -> (uint256)
    def MINIMUM_LIQUIDITY(
        self,
    ) -> int:
        return self.functions.MINIMUM_LIQUIDITY().call(self.transaction)

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

    # burn (address) -> (uint256, uint256)
    def burn(self, to: Address) -> BurnOutput:
        return self.functions.burn(to).call(self.transaction)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # getReserves () -> (uint112, uint112, uint32)
    def getReserves(
        self,
    ) -> GetReservesOutput:
        return self.functions.getReserves().call(self.transaction)

    # initialize (address, address) -> ()
    def initialize(self, token0: Address, token1: Address):
        return self.functions.initialize(token0, token1).call(self.transaction)

    # kLast () -> (uint256)
    def kLast(
        self,
    ) -> int:
        return self.functions.kLast().call(self.transaction)

    # mint (address) -> (uint256)
    def mint(self, to: Address) -> int:
        return self.functions.mint(to).call(self.transaction)

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

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> int:
        return self.functions.price0CumulativeLast().call(self.transaction)

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> int:
        return self.functions.price1CumulativeLast().call(self.transaction)

    # skim (address) -> ()
    def skim(self, to: Address):
        return self.functions.skim(to).call(self.transaction)

    # swap (uint256, uint256, address, bytes) -> ()
    def swap(
        self,
        amount0Out: int,
        amount1Out: int,
        to: Address,
        data: Union[bytearray, str, HexBytes],
    ):
        return self.functions.swap(amount0Out, amount1Out, to, data).call(
            self.transaction
        )

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Any:
        return self.functions.symbol().call(self.transaction)

    # sync () -> ()
    def sync(
        self,
    ):
        return self.functions.sync().call(self.transaction)

    # token0 () -> (address)
    def token0(
        self,
    ) -> Address:
        return self.functions.token0().call(self.transaction)

    # token1 () -> (address)
    def token1(
        self,
    ) -> Address:
        return self.functions.token1().call(self.transaction)

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


class UniswapV2Pair(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["UniswapV2Pair"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV2Pair.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/UniswapV2Pair.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "UniswapV2Pair":
            return UniswapV2Pair(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/UniswapV2Pair.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV2PairFunctions(w3, address, self.contract, self)
        self.call = UniswapV2PairCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.DOMAIN_SEPARATOR().waitForReceipt()

    # MINIMUM_LIQUIDITY () -> (uint256)
    def MINIMUM_LIQUIDITY(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.MINIMUM_LIQUIDITY().waitForReceipt()

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.PERMIT_TYPEHASH().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> UniswapV2PairReceipt:
        return self.functions.allowance(item0, item1).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> UniswapV2PairReceipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> UniswapV2PairReceipt:
        return self.functions.balanceOf(item0).waitForReceipt()

    # burn (address) -> (uint256, uint256)
    def burn(self, to: Address) -> UniswapV2PairReceipt:
        return self.functions.burn(to).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.decimals().waitForReceipt()

    # factory () -> (address)
    def factory(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.factory().waitForReceipt()

    # getReserves () -> (uint112, uint112, uint32)
    def getReserves(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.getReserves().waitForReceipt()

    # initialize (address, address) -> ()
    def initialize(self, token0: Address, token1: Address) -> UniswapV2PairReceipt:
        return self.functions.initialize(token0, token1).waitForReceipt()

    # kLast () -> (uint256)
    def kLast(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.kLast().waitForReceipt()

    # mint (address) -> (uint256)
    def mint(self, to: Address) -> UniswapV2PairReceipt:
        return self.functions.mint(to).waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.name().waitForReceipt()

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> UniswapV2PairReceipt:
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
    ) -> UniswapV2PairReceipt:
        return self.functions.permit(
            owner, spender, value, deadline, v, r, s
        ).waitForReceipt()

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.price0CumulativeLast().waitForReceipt()

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.price1CumulativeLast().waitForReceipt()

    # skim (address) -> ()
    def skim(self, to: Address) -> UniswapV2PairReceipt:
        return self.functions.skim(to).waitForReceipt()

    # swap (uint256, uint256, address, bytes) -> ()
    def swap(
        self,
        amount0Out: int,
        amount1Out: int,
        to: Address,
        data: Union[bytearray, str, HexBytes],
    ) -> UniswapV2PairReceipt:
        return self.functions.swap(amount0Out, amount1Out, to, data).waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.symbol().waitForReceipt()

    # sync () -> ()
    def sync(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.sync().waitForReceipt()

    # token0 () -> (address)
    def token0(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.token0().waitForReceipt()

    # token1 () -> (address)
    def token1(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.token1().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> UniswapV2PairReceipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> UniswapV2PairReceipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> UniswapV2PairReceipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end UniswapV2Pair ----------


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
        json_path = BUILD_DIR.joinpath("core/ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(totalSupply).transact()

        def on_receipt(receipt) -> "ERC20":
            return ERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/ERC20.json").resolve()
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


# ---------------------------------------------------------------
# UniswapV2ERC20

# ---
@dataclass
class UniswapV2ERC20ReceiptEvents:
    contract: "UniswapV2ERC20"
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
class UniswapV2ERC20Receipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: UniswapV2ERC20ReceiptEvents


# ---


class UniswapV2ERC20Functions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV2ERC20"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.DOMAIN_SEPARATOR()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.PERMIT_TYPEHASH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(
        self, item0: Address, item1: Address
    ) -> Function[int, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.allowance(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(
        self, spender: Address, value: int
    ) -> Function[bool, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> Function[int, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.balanceOf(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> Function[int, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

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
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

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
    ) -> Function[Any, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(
        self, to: Address, value: int
    ) -> Function[bool, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, UniswapV2ERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2ERC20Receipt:
            return UniswapV2ERC20Receipt(
                receipt, UniswapV2ERC20ReceiptEvents(self.contract, receipt)
            )

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV2ERC20Caller:
    def __init__(self, functions: UniswapV2ERC20Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV2ERC20Caller":
        return UniswapV2ERC20Caller(functions=self.functions, transaction=transaction)

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


class UniswapV2ERC20(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["UniswapV2ERC20"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV2ERC20.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/UniswapV2ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "UniswapV2ERC20":
            return UniswapV2ERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/UniswapV2ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV2ERC20Functions(w3, address, self.contract, self)
        self.call = UniswapV2ERC20Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> UniswapV2ERC20Receipt:
        return self.functions.DOMAIN_SEPARATOR().waitForReceipt()

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> UniswapV2ERC20Receipt:
        return self.functions.PERMIT_TYPEHASH().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> UniswapV2ERC20Receipt:
        return self.functions.allowance(item0, item1).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> UniswapV2ERC20Receipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> UniswapV2ERC20Receipt:
        return self.functions.balanceOf(item0).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> UniswapV2ERC20Receipt:
        return self.functions.decimals().waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> UniswapV2ERC20Receipt:
        return self.functions.name().waitForReceipt()

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> UniswapV2ERC20Receipt:
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
    ) -> UniswapV2ERC20Receipt:
        return self.functions.permit(
            owner, spender, value, deadline, v, r, s
        ).waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> UniswapV2ERC20Receipt:
        return self.functions.symbol().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> UniswapV2ERC20Receipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> UniswapV2ERC20Receipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> UniswapV2ERC20Receipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end UniswapV2ERC20 ----------


# ---------------------------------------------------------------
# IUniswapV2Callee

# ---
@dataclass
class IUniswapV2CalleeReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class IUniswapV2CalleeFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "IUniswapV2Callee"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # uniswapV2Call (address, uint256, uint256, bytes) -> ()
    def uniswapV2Call(
        self,
        sender: Address,
        amount0: int,
        amount1: int,
        data: Union[bytearray, str, HexBytes],
    ):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2CalleeReceipt:
            return IUniswapV2CalleeReceipt(receipt)

        sender, amount0, amount1, data = (
            unsugar(sender),
            unsugar(amount0),
            unsugar(amount1),
            unsugar(data),
        )
        web3_fn = self.web3_contract.functions.uniswapV2Call(
            sender, amount0, amount1, data
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV2CalleeCaller:
    def __init__(self, functions: IUniswapV2CalleeFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV2CalleeCaller":
        return IUniswapV2CalleeCaller(functions=self.functions, transaction=transaction)

    # uniswapV2Call (address, uint256, uint256, bytes) -> ()
    def uniswapV2Call(
        self,
        sender: Address,
        amount0: int,
        amount1: int,
        data: Union[bytearray, str, HexBytes],
    ):
        return self.functions.uniswapV2Call(sender, amount0, amount1, data).call(
            self.transaction
        )


# ---


class IUniswapV2Callee(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV2Callee"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV2Callee.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/IUniswapV2Callee.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Callee":
            return IUniswapV2Callee(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/IUniswapV2Callee.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV2CalleeFunctions(w3, address, self.contract, self)
        self.call = IUniswapV2CalleeCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # uniswapV2Call (address, uint256, uint256, bytes) -> ()
    def uniswapV2Call(
        self,
        sender: Address,
        amount0: int,
        amount1: int,
        data: Union[bytearray, str, HexBytes],
    ) -> IUniswapV2CalleeReceipt:
        return self.functions.uniswapV2Call(
            sender, amount0, amount1, data
        ).waitForReceipt()


# --------- end IUniswapV2Callee ----------


# ---------------------------------------------------------------
# IUniswapV2Factory

# ---
@dataclass
class IUniswapV2FactoryReceiptEvents:
    contract: "IUniswapV2Factory"
    web3_receipt: TxReceipt

    def PairCreated(self) -> Any:
        return (
            self.contract.to_web3()
            .events.PairCreated()
            .processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class IUniswapV2FactoryReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: IUniswapV2FactoryReceiptEvents


# ---


class IUniswapV2FactoryFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "IUniswapV2Factory"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # allPairs (uint256) -> (address)
    def allPairs(self, item0: int) -> Function[Address, IUniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.allPairs(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allPairsLength () -> (uint256)
    def allPairsLength(
        self,
    ) -> Function[int, IUniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.allPairsLength()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # createPair (address, address) -> (address)
    def createPair(
        self, tokenA: Address, tokenB: Address
    ) -> Function[Address, IUniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        tokenA, tokenB = unsugar(tokenA), unsugar(tokenB)
        web3_fn = self.web3_contract.functions.createPair(tokenA, tokenB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # feeTo () -> (address)
    def feeTo(
        self,
    ) -> Function[Address, IUniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.feeTo()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # feeToSetter () -> (address)
    def feeToSetter(
        self,
    ) -> Function[Address, IUniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.feeToSetter()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getPair (address, address) -> (address)
    def getPair(
        self, tokenA: Address, tokenB: Address
    ) -> Function[Address, IUniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        tokenA, tokenB = unsugar(tokenA), unsugar(tokenB)
        web3_fn = self.web3_contract.functions.getPair(tokenA, tokenB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setFeeTo (address) -> ()
    def setFeeTo(self, item0: Address):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.setFeeTo(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setFeeToSetter (address) -> ()
    def setFeeToSetter(self, item0: Address):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2FactoryReceipt:
            return IUniswapV2FactoryReceipt(
                receipt, IUniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.setFeeToSetter(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV2FactoryCaller:
    def __init__(self, functions: IUniswapV2FactoryFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV2FactoryCaller":
        return IUniswapV2FactoryCaller(
            functions=self.functions, transaction=transaction
        )

    # allPairs (uint256) -> (address)
    def allPairs(self, item0: int) -> Address:
        return self.functions.allPairs(item0).call(self.transaction)

    # allPairsLength () -> (uint256)
    def allPairsLength(
        self,
    ) -> int:
        return self.functions.allPairsLength().call(self.transaction)

    # createPair (address, address) -> (address)
    def createPair(self, tokenA: Address, tokenB: Address) -> Address:
        return self.functions.createPair(tokenA, tokenB).call(self.transaction)

    # feeTo () -> (address)
    def feeTo(
        self,
    ) -> Address:
        return self.functions.feeTo().call(self.transaction)

    # feeToSetter () -> (address)
    def feeToSetter(
        self,
    ) -> Address:
        return self.functions.feeToSetter().call(self.transaction)

    # getPair (address, address) -> (address)
    def getPair(self, tokenA: Address, tokenB: Address) -> Address:
        return self.functions.getPair(tokenA, tokenB).call(self.transaction)

    # setFeeTo (address) -> ()
    def setFeeTo(self, item0: Address):
        return self.functions.setFeeTo(item0).call(self.transaction)

    # setFeeToSetter (address) -> ()
    def setFeeToSetter(self, item0: Address):
        return self.functions.setFeeToSetter(item0).call(self.transaction)


# ---


class IUniswapV2Factory(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV2Factory"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV2Factory.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("core/IUniswapV2Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Factory":
            return IUniswapV2Factory(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/IUniswapV2Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV2FactoryFunctions(w3, address, self.contract, self)
        self.call = IUniswapV2FactoryCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # allPairs (uint256) -> (address)
    def allPairs(self, item0: int) -> IUniswapV2FactoryReceipt:
        return self.functions.allPairs(item0).waitForReceipt()

    # allPairsLength () -> (uint256)
    def allPairsLength(
        self,
    ) -> IUniswapV2FactoryReceipt:
        return self.functions.allPairsLength().waitForReceipt()

    # createPair (address, address) -> (address)
    def createPair(self, tokenA: Address, tokenB: Address) -> IUniswapV2FactoryReceipt:
        return self.functions.createPair(tokenA, tokenB).waitForReceipt()

    # feeTo () -> (address)
    def feeTo(
        self,
    ) -> IUniswapV2FactoryReceipt:
        return self.functions.feeTo().waitForReceipt()

    # feeToSetter () -> (address)
    def feeToSetter(
        self,
    ) -> IUniswapV2FactoryReceipt:
        return self.functions.feeToSetter().waitForReceipt()

    # getPair (address, address) -> (address)
    def getPair(self, tokenA: Address, tokenB: Address) -> IUniswapV2FactoryReceipt:
        return self.functions.getPair(tokenA, tokenB).waitForReceipt()

    # setFeeTo (address) -> ()
    def setFeeTo(self, item0: Address) -> IUniswapV2FactoryReceipt:
        return self.functions.setFeeTo(item0).waitForReceipt()

    # setFeeToSetter (address) -> ()
    def setFeeToSetter(self, item0: Address) -> IUniswapV2FactoryReceipt:
        return self.functions.setFeeToSetter(item0).waitForReceipt()


# --------- end IUniswapV2Factory ----------


# ---------------------------------------------------------------
# UniswapV2Factory

# ---
@dataclass
class UniswapV2FactoryReceiptEvents:
    contract: "UniswapV2Factory"
    web3_receipt: TxReceipt

    def PairCreated(self) -> Any:
        return (
            self.contract.to_web3()
            .events.PairCreated()
            .processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class UniswapV2FactoryReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: UniswapV2FactoryReceiptEvents


# ---


class UniswapV2FactoryFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV2Factory"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # allPairs (uint256) -> (address)
    def allPairs(self, item0: int) -> Function[Address, UniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.allPairs(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allPairsLength () -> (uint256)
    def allPairsLength(
        self,
    ) -> Function[int, UniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.allPairsLength()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # createPair (address, address) -> (address)
    def createPair(
        self, tokenA: Address, tokenB: Address
    ) -> Function[Address, UniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        tokenA, tokenB = unsugar(tokenA), unsugar(tokenB)
        web3_fn = self.web3_contract.functions.createPair(tokenA, tokenB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # feeTo () -> (address)
    def feeTo(
        self,
    ) -> Function[Address, UniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.feeTo()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # feeToSetter () -> (address)
    def feeToSetter(
        self,
    ) -> Function[Address, UniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.feeToSetter()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getPair (address, address) -> (address)
    def getPair(
        self, item0: Address, item1: Address
    ) -> Function[Address, UniswapV2FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.getPair(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setFeeTo (address) -> ()
    def setFeeTo(self, feeTo: Address):
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        feeTo = unsugar(feeTo)
        web3_fn = self.web3_contract.functions.setFeeTo(feeTo)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # setFeeToSetter (address) -> ()
    def setFeeToSetter(self, feeToSetter: Address):
        def make_receipt(receipt: TxReceipt) -> UniswapV2FactoryReceipt:
            return UniswapV2FactoryReceipt(
                receipt, UniswapV2FactoryReceiptEvents(self.contract, receipt)
            )

        feeToSetter = unsugar(feeToSetter)
        web3_fn = self.web3_contract.functions.setFeeToSetter(feeToSetter)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV2FactoryCaller:
    def __init__(self, functions: UniswapV2FactoryFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV2FactoryCaller":
        return UniswapV2FactoryCaller(functions=self.functions, transaction=transaction)

    # allPairs (uint256) -> (address)
    def allPairs(self, item0: int) -> Address:
        return self.functions.allPairs(item0).call(self.transaction)

    # allPairsLength () -> (uint256)
    def allPairsLength(
        self,
    ) -> int:
        return self.functions.allPairsLength().call(self.transaction)

    # createPair (address, address) -> (address)
    def createPair(self, tokenA: Address, tokenB: Address) -> Address:
        return self.functions.createPair(tokenA, tokenB).call(self.transaction)

    # feeTo () -> (address)
    def feeTo(
        self,
    ) -> Address:
        return self.functions.feeTo().call(self.transaction)

    # feeToSetter () -> (address)
    def feeToSetter(
        self,
    ) -> Address:
        return self.functions.feeToSetter().call(self.transaction)

    # getPair (address, address) -> (address)
    def getPair(self, item0: Address, item1: Address) -> Address:
        return self.functions.getPair(item0, item1).call(self.transaction)

    # setFeeTo (address) -> ()
    def setFeeTo(self, feeTo: Address):
        return self.functions.setFeeTo(feeTo).call(self.transaction)

    # setFeeToSetter (address) -> ()
    def setFeeToSetter(self, feeToSetter: Address):
        return self.functions.setFeeToSetter(feeToSetter).call(self.transaction)


# ---


class UniswapV2Factory(HasAddress):
    #
    @staticmethod
    def deploy(w3: Web3, feeToSetter: Address) -> PendingDeployment["UniswapV2Factory"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV2Factory.deploy(w3, ...) w3 must not be None"
            )

        feeToSetter = unsugar(feeToSetter)
        json_path = BUILD_DIR.joinpath("core/UniswapV2Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(feeToSetter).transact()

        def on_receipt(receipt) -> "UniswapV2Factory":
            return UniswapV2Factory(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("core/UniswapV2Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV2FactoryFunctions(w3, address, self.contract, self)
        self.call = UniswapV2FactoryCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # allPairs (uint256) -> (address)
    def allPairs(self, item0: int) -> UniswapV2FactoryReceipt:
        return self.functions.allPairs(item0).waitForReceipt()

    # allPairsLength () -> (uint256)
    def allPairsLength(
        self,
    ) -> UniswapV2FactoryReceipt:
        return self.functions.allPairsLength().waitForReceipt()

    # createPair (address, address) -> (address)
    def createPair(self, tokenA: Address, tokenB: Address) -> UniswapV2FactoryReceipt:
        return self.functions.createPair(tokenA, tokenB).waitForReceipt()

    # feeTo () -> (address)
    def feeTo(
        self,
    ) -> UniswapV2FactoryReceipt:
        return self.functions.feeTo().waitForReceipt()

    # feeToSetter () -> (address)
    def feeToSetter(
        self,
    ) -> UniswapV2FactoryReceipt:
        return self.functions.feeToSetter().waitForReceipt()

    # getPair (address, address) -> (address)
    def getPair(self, item0: Address, item1: Address) -> UniswapV2FactoryReceipt:
        return self.functions.getPair(item0, item1).waitForReceipt()

    # setFeeTo (address) -> ()
    def setFeeTo(self, feeTo: Address) -> UniswapV2FactoryReceipt:
        return self.functions.setFeeTo(feeTo).waitForReceipt()

    # setFeeToSetter (address) -> ()
    def setFeeToSetter(self, feeToSetter: Address) -> UniswapV2FactoryReceipt:
        return self.functions.setFeeToSetter(feeToSetter).waitForReceipt()


# --------- end UniswapV2Factory ----------
