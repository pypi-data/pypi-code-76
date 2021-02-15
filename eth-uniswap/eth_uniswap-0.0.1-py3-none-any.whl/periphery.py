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

        json_path = BUILD_DIR.joinpath("periphery/IERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IERC20":
            return IERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IERC20.json").resolve()
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
# UniswapV2Router02

AddLiquidityOutput = namedtuple(
    "AddLiquidityOutput", [x.strip() for x in " amountA, amountB, liquidity".split(",")]
)
AddLiquidityETHOutput = namedtuple(
    "AddLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH, liquidity".split(",")],
)
RemoveLiquidityOutput = namedtuple(
    "RemoveLiquidityOutput", [x.strip() for x in " amountA, amountB".split(",")]
)
RemoveLiquidityETHOutput = namedtuple(
    "RemoveLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityETHWithPermitOutput = namedtuple(
    "RemoveLiquidityETHWithPermitOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityWithPermitOutput = namedtuple(
    "RemoveLiquidityWithPermitOutput",
    [x.strip() for x in " amountA, amountB".split(",")],
)
# ---
@dataclass
class UniswapV2Router02Receipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class UniswapV2Router02Functions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV2Router02"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Function[Address, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        web3_fn = self.web3_contract.functions.WETH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityOutput, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        (
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(amountADesired),
            unsugar(amountBDesired),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        )

        def convert(args) -> AddLiquidityOutput:
            return AddLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityETHOutput, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(amountTokenDesired),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> AddLiquidityETHOutput:
            return AddLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> Function[int, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountOut, reserveIn, reserveOut = (
            unsugar(amountOut),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> Function[int, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountIn, reserveIn, reserveOut = (
            unsugar(amountIn),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountOut, path = unsugar(amountOut), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsIn(amountOut, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountIn, path = unsugar(amountIn), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsOut(amountIn, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> Function[int, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountA, reserveA, reserveB = (
            unsugar(amountA),
            unsugar(reserveA),
            unsugar(reserveB),
        )
        web3_fn = self.web3_contract.functions.quote(amountA, reserveA, reserveB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityOutput, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityOutput:
            return RemoveLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityETHOutput, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        token, liquidity, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityETHOutput:
            return RemoveLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETHSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256) -> (uint256)
    def removeLiquidityETHSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[int, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        token, liquidity, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHSupportingFeeOnTransferTokens(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityETHWithPermitOutput, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        (
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityETHWithPermitOutput:
            return RemoveLiquidityETHWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETHWithPermitSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256)
    def removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[int, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        (
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityWithPermitOutput, UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        (
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityWithPermitOutput:
            return RemoveLiquidityWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountOut, path, to, deadline = (
            unsugar(amountOut),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountOutMin, path, to, deadline = (
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactETHForTokensSupportingFeeOnTransferTokens (uint256, address[], address, uint256) -> ()
    def swapExactETHForTokensSupportingFeeOnTransferTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ):
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountOutMin, path, to, deadline = (
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForETHSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETHSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForTokensSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokensSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router02Receipt:
            return UniswapV2Router02Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV2Router02Caller:
    def __init__(self, functions: UniswapV2Router02Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV2Router02Caller":
        return UniswapV2Router02Caller(
            functions=self.functions, transaction=transaction
        )

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Address:
        return self.functions.WETH().call(self.transaction)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityOutput:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).call(self.transaction)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityETHOutput:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(self, amountOut: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountIn(amountOut, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(self, amountIn: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountOut(amountIn, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(self, amountOut: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsIn(amountOut, path).call(self.transaction)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(self, amountIn: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsOut(amountIn, path).call(self.transaction)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(self, amountA: int, reserveA: int, reserveB: int) -> int:
        return self.functions.quote(amountA, reserveA, reserveB).call(self.transaction)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityOutput:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityETHOutput:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETHSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256) -> (uint256)
    def removeLiquidityETHSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> int:
        return self.functions.removeLiquidityETHSupportingFeeOnTransferTokens(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityETHWithPermitOutput:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # removeLiquidityETHWithPermitSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256)
    def removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> int:
        return self.functions.removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityWithPermitOutput:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapETHForExactTokens(amountOut, path, to, deadline).call(
            self.transaction
        )

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactETHForTokensSupportingFeeOnTransferTokens (uint256, address[], address, uint256) -> ()
    def swapExactETHForTokensSupportingFeeOnTransferTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ):
        return self.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForETHSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETHSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForTokensSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokensSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)


# ---


class UniswapV2Router02(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factory: Address, WETH: Address
    ) -> PendingDeployment["UniswapV2Router02"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV2Router02.deploy(w3, ...) w3 must not be None"
            )

        factory, WETH = unsugar(factory), unsugar(WETH)
        json_path = BUILD_DIR.joinpath("periphery/UniswapV2Router02.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factory, WETH).transact()

        def on_receipt(receipt) -> "UniswapV2Router02":
            return UniswapV2Router02(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/UniswapV2Router02.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV2Router02Functions(w3, address, self.contract, self)
        self.call = UniswapV2Router02Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> UniswapV2Router02Receipt:
        return self.functions.WETH().waitForReceipt()

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).waitForReceipt()

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # factory () -> (address)
    def factory(
        self,
    ) -> UniswapV2Router02Receipt:
        return self.functions.factory().waitForReceipt()

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> UniswapV2Router02Receipt:
        return self.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> UniswapV2Router02Receipt:
        return self.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> UniswapV2Router02Receipt:
        return self.functions.getAmountsIn(amountOut, path).waitForReceipt()

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> UniswapV2Router02Receipt:
        return self.functions.getAmountsOut(amountIn, path).waitForReceipt()

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> UniswapV2Router02Receipt:
        return self.functions.quote(amountA, reserveA, reserveB).waitForReceipt()

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETHSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256) -> (uint256)
    def removeLiquidityETHSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.removeLiquidityETHSupportingFeeOnTransferTokens(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> UniswapV2Router02Receipt:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # removeLiquidityETHWithPermitSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256)
    def removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> UniswapV2Router02Receipt:
        return self.functions.removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> UniswapV2Router02Receipt:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        ).waitForReceipt()

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactETHForTokensSupportingFeeOnTransferTokens (uint256, address[], address, uint256) -> ()
    def swapExactETHForTokensSupportingFeeOnTransferTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForETHSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETHSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForTokensSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokensSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router02Receipt:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()


# --------- end UniswapV2Router02 ----------


# ---------------------------------------------------------------
# ExampleSwapToPrice

# ---
@dataclass
class ExampleSwapToPriceReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class ExampleSwapToPriceFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "ExampleSwapToPrice",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, ExampleSwapToPriceReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSwapToPriceReceipt:
            return ExampleSwapToPriceReceipt(receipt)

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # router () -> (address)
    def router(
        self,
    ) -> Function[Address, ExampleSwapToPriceReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSwapToPriceReceipt:
            return ExampleSwapToPriceReceipt(receipt)

        web3_fn = self.web3_contract.functions.router()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapToPrice (address, address, uint256, uint256, uint256, uint256, address, uint256) -> ()
    def swapToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        maxSpendTokenA: int,
        maxSpendTokenB: int,
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> ExampleSwapToPriceReceipt:
            return ExampleSwapToPriceReceipt(receipt)

        (
            tokenA,
            tokenB,
            truePriceTokenA,
            truePriceTokenB,
            maxSpendTokenA,
            maxSpendTokenB,
            to,
            deadline,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(truePriceTokenA),
            unsugar(truePriceTokenB),
            unsugar(maxSpendTokenA),
            unsugar(maxSpendTokenB),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapToPrice(
            tokenA,
            tokenB,
            truePriceTokenA,
            truePriceTokenB,
            maxSpendTokenA,
            maxSpendTokenB,
            to,
            deadline,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class ExampleSwapToPriceCaller:
    def __init__(self, functions: ExampleSwapToPriceFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "ExampleSwapToPriceCaller":
        return ExampleSwapToPriceCaller(
            functions=self.functions, transaction=transaction
        )

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # router () -> (address)
    def router(
        self,
    ) -> Address:
        return self.functions.router().call(self.transaction)

    # swapToPrice (address, address, uint256, uint256, uint256, uint256, address, uint256) -> ()
    def swapToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        maxSpendTokenA: int,
        maxSpendTokenB: int,
        to: Address,
        deadline: int,
    ):
        return self.functions.swapToPrice(
            tokenA,
            tokenB,
            truePriceTokenA,
            truePriceTokenB,
            maxSpendTokenA,
            maxSpendTokenB,
            to,
            deadline,
        ).call(self.transaction)


# ---


class ExampleSwapToPrice(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factory_: Address, router_: Address
    ) -> PendingDeployment["ExampleSwapToPrice"]:
        if w3 is None:
            raise ValueError(
                "In method ExampleSwapToPrice.deploy(w3, ...) w3 must not be None"
            )

        factory_, router_ = unsugar(factory_), unsugar(router_)
        json_path = BUILD_DIR.joinpath("periphery/ExampleSwapToPrice.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factory_, router_).transact()

        def on_receipt(receipt) -> "ExampleSwapToPrice":
            return ExampleSwapToPrice(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/ExampleSwapToPrice.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = ExampleSwapToPriceFunctions(w3, address, self.contract, self)
        self.call = ExampleSwapToPriceCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # factory () -> (address)
    def factory(
        self,
    ) -> ExampleSwapToPriceReceipt:
        return self.functions.factory().waitForReceipt()

    # router () -> (address)
    def router(
        self,
    ) -> ExampleSwapToPriceReceipt:
        return self.functions.router().waitForReceipt()

    # swapToPrice (address, address, uint256, uint256, uint256, uint256, address, uint256) -> ()
    def swapToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        maxSpendTokenA: int,
        maxSpendTokenB: int,
        to: Address,
        deadline: int,
    ) -> ExampleSwapToPriceReceipt:
        return self.functions.swapToPrice(
            tokenA,
            tokenB,
            truePriceTokenA,
            truePriceTokenB,
            maxSpendTokenA,
            maxSpendTokenB,
            to,
            deadline,
        ).waitForReceipt()


# --------- end ExampleSwapToPrice ----------


# ---------------------------------------------------------------
# ExampleFlashSwap

# ---
@dataclass
class ExampleFlashSwapReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class ExampleFlashSwapFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "ExampleFlashSwap"
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
        def make_receipt(receipt: TxReceipt) -> ExampleFlashSwapReceipt:
            return ExampleFlashSwapReceipt(receipt)

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


class ExampleFlashSwapCaller:
    def __init__(self, functions: ExampleFlashSwapFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "ExampleFlashSwapCaller":
        return ExampleFlashSwapCaller(functions=self.functions, transaction=transaction)

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


class ExampleFlashSwap(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factory: Address, factoryV1: Address, router: Address
    ) -> PendingDeployment["ExampleFlashSwap"]:
        if w3 is None:
            raise ValueError(
                "In method ExampleFlashSwap.deploy(w3, ...) w3 must not be None"
            )

        factory, factoryV1, router = (
            unsugar(factory),
            unsugar(factoryV1),
            unsugar(router),
        )
        json_path = BUILD_DIR.joinpath("periphery/ExampleFlashSwap.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factory, factoryV1, router).transact()

        def on_receipt(receipt) -> "ExampleFlashSwap":
            return ExampleFlashSwap(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/ExampleFlashSwap.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = ExampleFlashSwapFunctions(w3, address, self.contract, self)
        self.call = ExampleFlashSwapCaller(self.functions)

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
    ) -> ExampleFlashSwapReceipt:
        return self.functions.uniswapV2Call(
            sender, amount0, amount1, data
        ).waitForReceipt()


# --------- end ExampleFlashSwap ----------


# ---------------------------------------------------------------
# IUniswapV2Router02

AddLiquidityOutput = namedtuple(
    "AddLiquidityOutput", [x.strip() for x in " amountA, amountB, liquidity".split(",")]
)
AddLiquidityETHOutput = namedtuple(
    "AddLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH, liquidity".split(",")],
)
RemoveLiquidityOutput = namedtuple(
    "RemoveLiquidityOutput", [x.strip() for x in " amountA, amountB".split(",")]
)
RemoveLiquidityETHOutput = namedtuple(
    "RemoveLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityETHWithPermitOutput = namedtuple(
    "RemoveLiquidityETHWithPermitOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityWithPermitOutput = namedtuple(
    "RemoveLiquidityWithPermitOutput",
    [x.strip() for x in " amountA, amountB".split(",")],
)
# ---
@dataclass
class IUniswapV2Router02Receipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class IUniswapV2Router02Functions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "IUniswapV2Router02",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Function[Address, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        web3_fn = self.web3_contract.functions.WETH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityOutput, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        (
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(amountADesired),
            unsugar(amountBDesired),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        )

        def convert(args) -> AddLiquidityOutput:
            return AddLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityETHOutput, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(amountTokenDesired),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> AddLiquidityETHOutput:
            return AddLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> Function[int, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountOut, reserveIn, reserveOut = (
            unsugar(amountOut),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> Function[int, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountIn, reserveIn, reserveOut = (
            unsugar(amountIn),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountOut, path = unsugar(amountOut), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsIn(amountOut, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountIn, path = unsugar(amountIn), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsOut(amountIn, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> Function[int, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountA, reserveA, reserveB = (
            unsugar(amountA),
            unsugar(reserveA),
            unsugar(reserveB),
        )
        web3_fn = self.web3_contract.functions.quote(amountA, reserveA, reserveB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityOutput, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityOutput:
            return RemoveLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityETHOutput, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        token, liquidity, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityETHOutput:
            return RemoveLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETHSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256) -> (uint256)
    def removeLiquidityETHSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[int, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        token, liquidity, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHSupportingFeeOnTransferTokens(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityETHWithPermitOutput, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        (
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityETHWithPermitOutput:
            return RemoveLiquidityETHWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETHWithPermitSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256)
    def removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[int, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        (
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityWithPermitOutput, IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        (
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityWithPermitOutput:
            return RemoveLiquidityWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountOut, path, to, deadline = (
            unsugar(amountOut),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountOutMin, path, to, deadline = (
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactETHForTokensSupportingFeeOnTransferTokens (uint256, address[], address, uint256) -> ()
    def swapExactETHForTokensSupportingFeeOnTransferTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountOutMin, path, to, deadline = (
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForETHSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETHSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForTokensSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokensSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router02Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router02Receipt:
            return IUniswapV2Router02Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV2Router02Caller:
    def __init__(self, functions: IUniswapV2Router02Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV2Router02Caller":
        return IUniswapV2Router02Caller(
            functions=self.functions, transaction=transaction
        )

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Address:
        return self.functions.WETH().call(self.transaction)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityOutput:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).call(self.transaction)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityETHOutput:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(self, amountOut: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountIn(amountOut, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(self, amountIn: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountOut(amountIn, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(self, amountOut: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsIn(amountOut, path).call(self.transaction)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(self, amountIn: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsOut(amountIn, path).call(self.transaction)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(self, amountA: int, reserveA: int, reserveB: int) -> int:
        return self.functions.quote(amountA, reserveA, reserveB).call(self.transaction)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityOutput:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityETHOutput:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETHSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256) -> (uint256)
    def removeLiquidityETHSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> int:
        return self.functions.removeLiquidityETHSupportingFeeOnTransferTokens(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityETHWithPermitOutput:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # removeLiquidityETHWithPermitSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256)
    def removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> int:
        return self.functions.removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityWithPermitOutput:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapETHForExactTokens(amountOut, path, to, deadline).call(
            self.transaction
        )

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactETHForTokensSupportingFeeOnTransferTokens (uint256, address[], address, uint256) -> ()
    def swapExactETHForTokensSupportingFeeOnTransferTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ):
        return self.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForETHSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETHSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForTokensSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokensSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)


# ---


class IUniswapV2Router02(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV2Router02"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV2Router02.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Router02.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Router02":
            return IUniswapV2Router02(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Router02.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV2Router02Functions(w3, address, self.contract, self)
        self.call = IUniswapV2Router02Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.WETH().waitForReceipt()

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).waitForReceipt()

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # factory () -> (address)
    def factory(
        self,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.factory().waitForReceipt()

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> IUniswapV2Router02Receipt:
        return self.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> IUniswapV2Router02Receipt:
        return self.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> IUniswapV2Router02Receipt:
        return self.functions.getAmountsIn(amountOut, path).waitForReceipt()

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> IUniswapV2Router02Receipt:
        return self.functions.getAmountsOut(amountIn, path).waitForReceipt()

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> IUniswapV2Router02Receipt:
        return self.functions.quote(amountA, reserveA, reserveB).waitForReceipt()

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETHSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256) -> (uint256)
    def removeLiquidityETHSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.removeLiquidityETHSupportingFeeOnTransferTokens(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> IUniswapV2Router02Receipt:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # removeLiquidityETHWithPermitSupportingFeeOnTransferTokens (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256)
    def removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> IUniswapV2Router02Receipt:
        return self.functions.removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> IUniswapV2Router02Receipt:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        ).waitForReceipt()

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactETHForTokensSupportingFeeOnTransferTokens (uint256, address[], address, uint256) -> ()
    def swapExactETHForTokensSupportingFeeOnTransferTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForETHSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETHSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForTokensSupportingFeeOnTransferTokens (uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokensSupportingFeeOnTransferTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router02Receipt:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()


# --------- end IUniswapV2Router02 ----------


# ---------------------------------------------------------------
# UniswapV2Migrator

# ---
@dataclass
class UniswapV2MigratorReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class UniswapV2MigratorFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV2Migrator"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # migrate (address, uint256, uint256, address, uint256) -> ()
    def migrate(
        self,
        token: Address,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> UniswapV2MigratorReceipt:
            return UniswapV2MigratorReceipt(receipt)

        token, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.migrate(
            token, amountTokenMin, amountETHMin, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV2MigratorCaller:
    def __init__(self, functions: UniswapV2MigratorFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV2MigratorCaller":
        return UniswapV2MigratorCaller(
            functions=self.functions, transaction=transaction
        )

    # migrate (address, uint256, uint256, address, uint256) -> ()
    def migrate(
        self,
        token: Address,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ):
        return self.functions.migrate(
            token, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)


# ---


class UniswapV2Migrator(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factoryV1: Address, router: Address
    ) -> PendingDeployment["UniswapV2Migrator"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV2Migrator.deploy(w3, ...) w3 must not be None"
            )

        factoryV1, router = unsugar(factoryV1), unsugar(router)
        json_path = BUILD_DIR.joinpath("periphery/UniswapV2Migrator.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factoryV1, router).transact()

        def on_receipt(receipt) -> "UniswapV2Migrator":
            return UniswapV2Migrator(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/UniswapV2Migrator.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV2MigratorFunctions(w3, address, self.contract, self)
        self.call = UniswapV2MigratorCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # migrate (address, uint256, uint256, address, uint256) -> ()
    def migrate(
        self,
        token: Address,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2MigratorReceipt:
        return self.functions.migrate(
            token, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()


# --------- end UniswapV2Migrator ----------


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

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Pair.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Pair":
            return IUniswapV2Pair(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Pair.json").resolve()
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
# UniswapV1Factory

# ---
@dataclass
class UniswapV1FactoryReceiptEvents:
    contract: "UniswapV1Factory"
    web3_receipt: TxReceipt

    def NewExchange(self) -> Any:
        return (
            self.contract.to_web3()
            .events.NewExchange()
            .processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class UniswapV1FactoryReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: UniswapV1FactoryReceiptEvents


# ---


class UniswapV1FactoryFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV1Factory"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # initializeFactory (address) -> ()
    def initializeFactory(self, template: Address):
        def make_receipt(receipt: TxReceipt) -> UniswapV1FactoryReceipt:
            return UniswapV1FactoryReceipt(
                receipt, UniswapV1FactoryReceiptEvents(self.contract, receipt)
            )

        template = unsugar(template)
        web3_fn = self.web3_contract.functions.initializeFactory(template)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # createExchange (address) -> (address)
    def createExchange(
        self, token: Address
    ) -> Function[Address, UniswapV1FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1FactoryReceipt:
            return UniswapV1FactoryReceipt(
                receipt, UniswapV1FactoryReceiptEvents(self.contract, receipt)
            )

        token = unsugar(token)
        web3_fn = self.web3_contract.functions.createExchange(token)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getExchange (address) -> (address)
    def getExchange(self, token: Address) -> Function[Address, UniswapV1FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1FactoryReceipt:
            return UniswapV1FactoryReceipt(
                receipt, UniswapV1FactoryReceiptEvents(self.contract, receipt)
            )

        token = unsugar(token)
        web3_fn = self.web3_contract.functions.getExchange(token)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getToken (address) -> (address)
    def getToken(self, exchange: Address) -> Function[Address, UniswapV1FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1FactoryReceipt:
            return UniswapV1FactoryReceipt(
                receipt, UniswapV1FactoryReceiptEvents(self.contract, receipt)
            )

        exchange = unsugar(exchange)
        web3_fn = self.web3_contract.functions.getToken(exchange)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getTokenWithId (uint256) -> (address)
    def getTokenWithId(
        self, token_id: int
    ) -> Function[Address, UniswapV1FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1FactoryReceipt:
            return UniswapV1FactoryReceipt(
                receipt, UniswapV1FactoryReceiptEvents(self.contract, receipt)
            )

        token_id = unsugar(token_id)
        web3_fn = self.web3_contract.functions.getTokenWithId(token_id)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # exchangeTemplate () -> (address)
    def exchangeTemplate(
        self,
    ) -> Function[Address, UniswapV1FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1FactoryReceipt:
            return UniswapV1FactoryReceipt(
                receipt, UniswapV1FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.exchangeTemplate()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenCount () -> (uint256)
    def tokenCount(
        self,
    ) -> Function[int, UniswapV1FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1FactoryReceipt:
            return UniswapV1FactoryReceipt(
                receipt, UniswapV1FactoryReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.tokenCount()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV1FactoryCaller:
    def __init__(self, functions: UniswapV1FactoryFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV1FactoryCaller":
        return UniswapV1FactoryCaller(functions=self.functions, transaction=transaction)

    # initializeFactory (address) -> ()
    def initializeFactory(self, template: Address):
        return self.functions.initializeFactory(template).call(self.transaction)

    # createExchange (address) -> (address)
    def createExchange(self, token: Address) -> Address:
        return self.functions.createExchange(token).call(self.transaction)

    # getExchange (address) -> (address)
    def getExchange(self, token: Address) -> Address:
        return self.functions.getExchange(token).call(self.transaction)

    # getToken (address) -> (address)
    def getToken(self, exchange: Address) -> Address:
        return self.functions.getToken(exchange).call(self.transaction)

    # getTokenWithId (uint256) -> (address)
    def getTokenWithId(self, token_id: int) -> Address:
        return self.functions.getTokenWithId(token_id).call(self.transaction)

    # exchangeTemplate () -> (address)
    def exchangeTemplate(
        self,
    ) -> Address:
        return self.functions.exchangeTemplate().call(self.transaction)

    # tokenCount () -> (uint256)
    def tokenCount(
        self,
    ) -> int:
        return self.functions.tokenCount().call(self.transaction)


# ---


class UniswapV1Factory(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["UniswapV1Factory"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV1Factory.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/UniswapV1Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "UniswapV1Factory":
            return UniswapV1Factory(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/UniswapV1Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV1FactoryFunctions(w3, address, self.contract, self)
        self.call = UniswapV1FactoryCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # initializeFactory (address) -> ()
    def initializeFactory(self, template: Address) -> UniswapV1FactoryReceipt:
        return self.functions.initializeFactory(template).waitForReceipt()

    # createExchange (address) -> (address)
    def createExchange(self, token: Address) -> UniswapV1FactoryReceipt:
        return self.functions.createExchange(token).waitForReceipt()

    # getExchange (address) -> (address)
    def getExchange(self, token: Address) -> UniswapV1FactoryReceipt:
        return self.functions.getExchange(token).waitForReceipt()

    # getToken (address) -> (address)
    def getToken(self, exchange: Address) -> UniswapV1FactoryReceipt:
        return self.functions.getToken(exchange).waitForReceipt()

    # getTokenWithId (uint256) -> (address)
    def getTokenWithId(self, token_id: int) -> UniswapV1FactoryReceipt:
        return self.functions.getTokenWithId(token_id).waitForReceipt()

    # exchangeTemplate () -> (address)
    def exchangeTemplate(
        self,
    ) -> UniswapV1FactoryReceipt:
        return self.functions.exchangeTemplate().waitForReceipt()

    # tokenCount () -> (uint256)
    def tokenCount(
        self,
    ) -> UniswapV1FactoryReceipt:
        return self.functions.tokenCount().waitForReceipt()


# --------- end UniswapV1Factory ----------


# ---------------------------------------------------------------
# IUniswapV1Factory

# ---
@dataclass
class IUniswapV1FactoryReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class IUniswapV1FactoryFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "IUniswapV1Factory"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # getExchange (address) -> (address)
    def getExchange(
        self, item0: Address
    ) -> Function[Address, IUniswapV1FactoryReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV1FactoryReceipt:
            return IUniswapV1FactoryReceipt(receipt)

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.getExchange(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV1FactoryCaller:
    def __init__(self, functions: IUniswapV1FactoryFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV1FactoryCaller":
        return IUniswapV1FactoryCaller(
            functions=self.functions, transaction=transaction
        )

    # getExchange (address) -> (address)
    def getExchange(self, item0: Address) -> Address:
        return self.functions.getExchange(item0).call(self.transaction)


# ---


class IUniswapV1Factory(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV1Factory"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV1Factory.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV1Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV1Factory":
            return IUniswapV1Factory(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV1Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV1FactoryFunctions(w3, address, self.contract, self)
        self.call = IUniswapV1FactoryCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # getExchange (address) -> (address)
    def getExchange(self, item0: Address) -> IUniswapV1FactoryReceipt:
        return self.functions.getExchange(item0).waitForReceipt()


# --------- end IUniswapV1Factory ----------


# ---------------------------------------------------------------
# UniswapV1Exchange

RemoveLiquidityOutput = namedtuple(
    "RemoveLiquidityOutput", [x.strip() for x in " out, out2".split(",")]
)
# ---
@dataclass
class UniswapV1ExchangeReceiptEvents:
    contract: "UniswapV1Exchange"
    web3_receipt: TxReceipt

    def TokenPurchase(self) -> Any:
        return (
            self.contract.to_web3()
            .events.TokenPurchase()
            .processReceipt(self.web3_receipt)
        )

    def EthPurchase(self) -> Any:
        return (
            self.contract.to_web3()
            .events.EthPurchase()
            .processReceipt(self.web3_receipt)
        )

    def AddLiquidity(self) -> Any:
        return (
            self.contract.to_web3()
            .events.AddLiquidity()
            .processReceipt(self.web3_receipt)
        )

    def RemoveLiquidity(self) -> Any:
        return (
            self.contract.to_web3()
            .events.RemoveLiquidity()
            .processReceipt(self.web3_receipt)
        )

    def Transfer(self) -> Any:
        return (
            self.contract.to_web3().events.Transfer().processReceipt(self.web3_receipt)
        )

    def Approval(self) -> Any:
        return (
            self.contract.to_web3().events.Approval().processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class UniswapV1ExchangeReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: UniswapV1ExchangeReceiptEvents


# ---


class UniswapV1ExchangeFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV1Exchange"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # setup (address) -> ()
    def setup(self, token_addr: Address):
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        token_addr = unsugar(token_addr)
        web3_fn = self.web3_contract.functions.setup(token_addr)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # addLiquidity (uint256, uint256, uint256) -> (uint256)
    def addLiquidity(
        self, min_liquidity: int, max_tokens: int, deadline: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        min_liquidity, max_tokens, deadline = (
            unsugar(min_liquidity),
            unsugar(max_tokens),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidity(
            min_liquidity, max_tokens, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidity (uint256, uint256, uint256, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self, amount: int, min_eth: int, min_tokens: int, deadline: int
    ) -> Function[RemoveLiquidityOutput, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        amount, min_eth, min_tokens, deadline = (
            unsugar(amount),
            unsugar(min_eth),
            unsugar(min_tokens),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidity(
            amount, min_eth, min_tokens, deadline
        )

        def convert(args) -> RemoveLiquidityOutput:
            return RemoveLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # __default__ () -> ()
    def __default__(
        self,
    ):
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.__default__()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # ethToTokenSwapInput (uint256, uint256) -> (uint256)
    def ethToTokenSwapInput(
        self, min_tokens: int, deadline: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        min_tokens, deadline = unsugar(min_tokens), unsugar(deadline)
        web3_fn = self.web3_contract.functions.ethToTokenSwapInput(min_tokens, deadline)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # ethToTokenTransferInput (uint256, uint256, address) -> (uint256)
    def ethToTokenTransferInput(
        self, min_tokens: int, deadline: int, recipient: Address
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        min_tokens, deadline, recipient = (
            unsugar(min_tokens),
            unsugar(deadline),
            unsugar(recipient),
        )
        web3_fn = self.web3_contract.functions.ethToTokenTransferInput(
            min_tokens, deadline, recipient
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # ethToTokenSwapOutput (uint256, uint256) -> (uint256)
    def ethToTokenSwapOutput(
        self, tokens_bought: int, deadline: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_bought, deadline = unsugar(tokens_bought), unsugar(deadline)
        web3_fn = self.web3_contract.functions.ethToTokenSwapOutput(
            tokens_bought, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # ethToTokenTransferOutput (uint256, uint256, address) -> (uint256)
    def ethToTokenTransferOutput(
        self, tokens_bought: int, deadline: int, recipient: Address
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_bought, deadline, recipient = (
            unsugar(tokens_bought),
            unsugar(deadline),
            unsugar(recipient),
        )
        web3_fn = self.web3_contract.functions.ethToTokenTransferOutput(
            tokens_bought, deadline, recipient
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToEthSwapInput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapInput(
        self, tokens_sold: int, min_eth: int, deadline: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_sold, min_eth, deadline = (
            unsugar(tokens_sold),
            unsugar(min_eth),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.tokenToEthSwapInput(
            tokens_sold, min_eth, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToEthTransferInput (uint256, uint256, uint256, address) -> (uint256)
    def tokenToEthTransferInput(
        self, tokens_sold: int, min_eth: int, deadline: int, recipient: Address
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_sold, min_eth, deadline, recipient = (
            unsugar(tokens_sold),
            unsugar(min_eth),
            unsugar(deadline),
            unsugar(recipient),
        )
        web3_fn = self.web3_contract.functions.tokenToEthTransferInput(
            tokens_sold, min_eth, deadline, recipient
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToEthSwapOutput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapOutput(
        self, eth_bought: int, max_tokens: int, deadline: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        eth_bought, max_tokens, deadline = (
            unsugar(eth_bought),
            unsugar(max_tokens),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.tokenToEthSwapOutput(
            eth_bought, max_tokens, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToEthTransferOutput (uint256, uint256, uint256, address) -> (uint256)
    def tokenToEthTransferOutput(
        self, eth_bought: int, max_tokens: int, deadline: int, recipient: Address
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        eth_bought, max_tokens, deadline, recipient = (
            unsugar(eth_bought),
            unsugar(max_tokens),
            unsugar(deadline),
            unsugar(recipient),
        )
        web3_fn = self.web3_contract.functions.tokenToEthTransferOutput(
            eth_bought, max_tokens, deadline, recipient
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToTokenSwapInput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToTokenSwapInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        token_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_sold, min_tokens_bought, min_eth_bought, deadline, token_addr = (
            unsugar(tokens_sold),
            unsugar(min_tokens_bought),
            unsugar(min_eth_bought),
            unsugar(deadline),
            unsugar(token_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToTokenSwapInput(
            tokens_sold, min_tokens_bought, min_eth_bought, deadline, token_addr
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToTokenTransferInput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToTokenTransferInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        recipient: Address,
        token_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        (
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            token_addr,
        ) = (
            unsugar(tokens_sold),
            unsugar(min_tokens_bought),
            unsugar(min_eth_bought),
            unsugar(deadline),
            unsugar(recipient),
            unsugar(token_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToTokenTransferInput(
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            token_addr,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToTokenSwapOutput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToTokenSwapOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        token_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_bought, max_tokens_sold, max_eth_sold, deadline, token_addr = (
            unsugar(tokens_bought),
            unsugar(max_tokens_sold),
            unsugar(max_eth_sold),
            unsugar(deadline),
            unsugar(token_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToTokenSwapOutput(
            tokens_bought, max_tokens_sold, max_eth_sold, deadline, token_addr
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToTokenTransferOutput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToTokenTransferOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        recipient: Address,
        token_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        (
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            token_addr,
        ) = (
            unsugar(tokens_bought),
            unsugar(max_tokens_sold),
            unsugar(max_eth_sold),
            unsugar(deadline),
            unsugar(recipient),
            unsugar(token_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToTokenTransferOutput(
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            token_addr,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToExchangeSwapInput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToExchangeSwapInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        exchange_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_sold, min_tokens_bought, min_eth_bought, deadline, exchange_addr = (
            unsugar(tokens_sold),
            unsugar(min_tokens_bought),
            unsugar(min_eth_bought),
            unsugar(deadline),
            unsugar(exchange_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToExchangeSwapInput(
            tokens_sold, min_tokens_bought, min_eth_bought, deadline, exchange_addr
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToExchangeTransferInput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToExchangeTransferInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        recipient: Address,
        exchange_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        (
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            exchange_addr,
        ) = (
            unsugar(tokens_sold),
            unsugar(min_tokens_bought),
            unsugar(min_eth_bought),
            unsugar(deadline),
            unsugar(recipient),
            unsugar(exchange_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToExchangeTransferInput(
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            exchange_addr,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToExchangeSwapOutput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToExchangeSwapOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        exchange_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_bought, max_tokens_sold, max_eth_sold, deadline, exchange_addr = (
            unsugar(tokens_bought),
            unsugar(max_tokens_sold),
            unsugar(max_eth_sold),
            unsugar(deadline),
            unsugar(exchange_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToExchangeSwapOutput(
            tokens_bought, max_tokens_sold, max_eth_sold, deadline, exchange_addr
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenToExchangeTransferOutput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToExchangeTransferOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        recipient: Address,
        exchange_addr: Address,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        (
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            exchange_addr,
        ) = (
            unsugar(tokens_bought),
            unsugar(max_tokens_sold),
            unsugar(max_eth_sold),
            unsugar(deadline),
            unsugar(recipient),
            unsugar(exchange_addr),
        )
        web3_fn = self.web3_contract.functions.tokenToExchangeTransferOutput(
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            exchange_addr,
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getEthToTokenInputPrice (uint256) -> (uint256)
    def getEthToTokenInputPrice(
        self, eth_sold: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        eth_sold = unsugar(eth_sold)
        web3_fn = self.web3_contract.functions.getEthToTokenInputPrice(eth_sold)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getEthToTokenOutputPrice (uint256) -> (uint256)
    def getEthToTokenOutputPrice(
        self, tokens_bought: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_bought = unsugar(tokens_bought)
        web3_fn = self.web3_contract.functions.getEthToTokenOutputPrice(tokens_bought)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getTokenToEthInputPrice (uint256) -> (uint256)
    def getTokenToEthInputPrice(
        self, tokens_sold: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        tokens_sold = unsugar(tokens_sold)
        web3_fn = self.web3_contract.functions.getTokenToEthInputPrice(tokens_sold)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getTokenToEthOutputPrice (uint256) -> (uint256)
    def getTokenToEthOutputPrice(
        self, eth_bought: int
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        eth_bought = unsugar(eth_bought)
        web3_fn = self.web3_contract.functions.getTokenToEthOutputPrice(eth_bought)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # tokenAddress () -> (address)
    def tokenAddress(
        self,
    ) -> Function[Address, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.tokenAddress()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # factoryAddress () -> (address)
    def factoryAddress(
        self,
    ) -> Function[Address, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.factoryAddress()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        owner = unsugar(owner)
        web3_fn = self.web3_contract.functions.balanceOf(owner)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(
        self, to: Address, value: int
    ) -> Function[bool, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(
        self, spender: Address, value: int
    ) -> Function[bool, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(
        self, owner: Address, spender: Address
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        owner, spender = unsugar(owner), unsugar(spender)
        web3_fn = self.web3_contract.functions.allowance(owner, spender)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (bytes32)
    def name(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (bytes32)
    def symbol(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint256)
    def decimals(
        self,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, UniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV1ExchangeReceipt:
            return UniswapV1ExchangeReceipt(
                receipt, UniswapV1ExchangeReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV1ExchangeCaller:
    def __init__(self, functions: UniswapV1ExchangeFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV1ExchangeCaller":
        return UniswapV1ExchangeCaller(
            functions=self.functions, transaction=transaction
        )

    # setup (address) -> ()
    def setup(self, token_addr: Address):
        return self.functions.setup(token_addr).call(self.transaction)

    # addLiquidity (uint256, uint256, uint256) -> (uint256)
    def addLiquidity(self, min_liquidity: int, max_tokens: int, deadline: int) -> int:
        return self.functions.addLiquidity(min_liquidity, max_tokens, deadline).call(
            self.transaction
        )

    # removeLiquidity (uint256, uint256, uint256, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self, amount: int, min_eth: int, min_tokens: int, deadline: int
    ) -> RemoveLiquidityOutput:
        return self.functions.removeLiquidity(
            amount, min_eth, min_tokens, deadline
        ).call(self.transaction)

    # __default__ () -> ()
    def __default__(
        self,
    ):
        return self.functions.__default__().call(self.transaction)

    # ethToTokenSwapInput (uint256, uint256) -> (uint256)
    def ethToTokenSwapInput(self, min_tokens: int, deadline: int) -> int:
        return self.functions.ethToTokenSwapInput(min_tokens, deadline).call(
            self.transaction
        )

    # ethToTokenTransferInput (uint256, uint256, address) -> (uint256)
    def ethToTokenTransferInput(
        self, min_tokens: int, deadline: int, recipient: Address
    ) -> int:
        return self.functions.ethToTokenTransferInput(
            min_tokens, deadline, recipient
        ).call(self.transaction)

    # ethToTokenSwapOutput (uint256, uint256) -> (uint256)
    def ethToTokenSwapOutput(self, tokens_bought: int, deadline: int) -> int:
        return self.functions.ethToTokenSwapOutput(tokens_bought, deadline).call(
            self.transaction
        )

    # ethToTokenTransferOutput (uint256, uint256, address) -> (uint256)
    def ethToTokenTransferOutput(
        self, tokens_bought: int, deadline: int, recipient: Address
    ) -> int:
        return self.functions.ethToTokenTransferOutput(
            tokens_bought, deadline, recipient
        ).call(self.transaction)

    # tokenToEthSwapInput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapInput(self, tokens_sold: int, min_eth: int, deadline: int) -> int:
        return self.functions.tokenToEthSwapInput(tokens_sold, min_eth, deadline).call(
            self.transaction
        )

    # tokenToEthTransferInput (uint256, uint256, uint256, address) -> (uint256)
    def tokenToEthTransferInput(
        self, tokens_sold: int, min_eth: int, deadline: int, recipient: Address
    ) -> int:
        return self.functions.tokenToEthTransferInput(
            tokens_sold, min_eth, deadline, recipient
        ).call(self.transaction)

    # tokenToEthSwapOutput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapOutput(
        self, eth_bought: int, max_tokens: int, deadline: int
    ) -> int:
        return self.functions.tokenToEthSwapOutput(
            eth_bought, max_tokens, deadline
        ).call(self.transaction)

    # tokenToEthTransferOutput (uint256, uint256, uint256, address) -> (uint256)
    def tokenToEthTransferOutput(
        self, eth_bought: int, max_tokens: int, deadline: int, recipient: Address
    ) -> int:
        return self.functions.tokenToEthTransferOutput(
            eth_bought, max_tokens, deadline, recipient
        ).call(self.transaction)

    # tokenToTokenSwapInput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToTokenSwapInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        token_addr: Address,
    ) -> int:
        return self.functions.tokenToTokenSwapInput(
            tokens_sold, min_tokens_bought, min_eth_bought, deadline, token_addr
        ).call(self.transaction)

    # tokenToTokenTransferInput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToTokenTransferInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        recipient: Address,
        token_addr: Address,
    ) -> int:
        return self.functions.tokenToTokenTransferInput(
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            token_addr,
        ).call(self.transaction)

    # tokenToTokenSwapOutput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToTokenSwapOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        token_addr: Address,
    ) -> int:
        return self.functions.tokenToTokenSwapOutput(
            tokens_bought, max_tokens_sold, max_eth_sold, deadline, token_addr
        ).call(self.transaction)

    # tokenToTokenTransferOutput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToTokenTransferOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        recipient: Address,
        token_addr: Address,
    ) -> int:
        return self.functions.tokenToTokenTransferOutput(
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            token_addr,
        ).call(self.transaction)

    # tokenToExchangeSwapInput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToExchangeSwapInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        exchange_addr: Address,
    ) -> int:
        return self.functions.tokenToExchangeSwapInput(
            tokens_sold, min_tokens_bought, min_eth_bought, deadline, exchange_addr
        ).call(self.transaction)

    # tokenToExchangeTransferInput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToExchangeTransferInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        recipient: Address,
        exchange_addr: Address,
    ) -> int:
        return self.functions.tokenToExchangeTransferInput(
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            exchange_addr,
        ).call(self.transaction)

    # tokenToExchangeSwapOutput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToExchangeSwapOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        exchange_addr: Address,
    ) -> int:
        return self.functions.tokenToExchangeSwapOutput(
            tokens_bought, max_tokens_sold, max_eth_sold, deadline, exchange_addr
        ).call(self.transaction)

    # tokenToExchangeTransferOutput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToExchangeTransferOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        recipient: Address,
        exchange_addr: Address,
    ) -> int:
        return self.functions.tokenToExchangeTransferOutput(
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            exchange_addr,
        ).call(self.transaction)

    # getEthToTokenInputPrice (uint256) -> (uint256)
    def getEthToTokenInputPrice(self, eth_sold: int) -> int:
        return self.functions.getEthToTokenInputPrice(eth_sold).call(self.transaction)

    # getEthToTokenOutputPrice (uint256) -> (uint256)
    def getEthToTokenOutputPrice(self, tokens_bought: int) -> int:
        return self.functions.getEthToTokenOutputPrice(tokens_bought).call(
            self.transaction
        )

    # getTokenToEthInputPrice (uint256) -> (uint256)
    def getTokenToEthInputPrice(self, tokens_sold: int) -> int:
        return self.functions.getTokenToEthInputPrice(tokens_sold).call(
            self.transaction
        )

    # getTokenToEthOutputPrice (uint256) -> (uint256)
    def getTokenToEthOutputPrice(self, eth_bought: int) -> int:
        return self.functions.getTokenToEthOutputPrice(eth_bought).call(
            self.transaction
        )

    # tokenAddress () -> (address)
    def tokenAddress(
        self,
    ) -> Address:
        return self.functions.tokenAddress().call(self.transaction)

    # factoryAddress () -> (address)
    def factoryAddress(
        self,
    ) -> Address:
        return self.functions.factoryAddress().call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> int:
        return self.functions.balanceOf(owner).call(self.transaction)

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> bool:
        return self.functions.transfer(to, value).call(self.transaction)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, from_: Address, to: Address, value: int) -> bool:
        return self.functions.transferFrom(from_, to, value).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> bool:
        return self.functions.approve(spender, value).call(self.transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, owner: Address, spender: Address) -> int:
        return self.functions.allowance(owner, spender).call(self.transaction)

    # name () -> (bytes32)
    def name(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.name().call(self.transaction)

    # symbol () -> (bytes32)
    def symbol(
        self,
    ) -> Union[bytearray, str, HexBytes]:
        return self.functions.symbol().call(self.transaction)

    # decimals () -> (uint256)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> int:
        return self.functions.totalSupply().call(self.transaction)


# ---


class UniswapV1Exchange(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["UniswapV1Exchange"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV1Exchange.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/UniswapV1Exchange.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "UniswapV1Exchange":
            return UniswapV1Exchange(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/UniswapV1Exchange.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV1ExchangeFunctions(w3, address, self.contract, self)
        self.call = UniswapV1ExchangeCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # setup (address) -> ()
    def setup(self, token_addr: Address) -> UniswapV1ExchangeReceipt:
        return self.functions.setup(token_addr).waitForReceipt()

    # addLiquidity (uint256, uint256, uint256) -> (uint256)
    def addLiquidity(
        self, min_liquidity: int, max_tokens: int, deadline: int
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.addLiquidity(
            min_liquidity, max_tokens, deadline
        ).waitForReceipt()

    # removeLiquidity (uint256, uint256, uint256, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self, amount: int, min_eth: int, min_tokens: int, deadline: int
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.removeLiquidity(
            amount, min_eth, min_tokens, deadline
        ).waitForReceipt()

    # __default__ () -> ()
    def __default__(
        self,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.__default__().waitForReceipt()

    # ethToTokenSwapInput (uint256, uint256) -> (uint256)
    def ethToTokenSwapInput(
        self, min_tokens: int, deadline: int
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.ethToTokenSwapInput(min_tokens, deadline).waitForReceipt()

    # ethToTokenTransferInput (uint256, uint256, address) -> (uint256)
    def ethToTokenTransferInput(
        self, min_tokens: int, deadline: int, recipient: Address
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.ethToTokenTransferInput(
            min_tokens, deadline, recipient
        ).waitForReceipt()

    # ethToTokenSwapOutput (uint256, uint256) -> (uint256)
    def ethToTokenSwapOutput(
        self, tokens_bought: int, deadline: int
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.ethToTokenSwapOutput(
            tokens_bought, deadline
        ).waitForReceipt()

    # ethToTokenTransferOutput (uint256, uint256, address) -> (uint256)
    def ethToTokenTransferOutput(
        self, tokens_bought: int, deadline: int, recipient: Address
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.ethToTokenTransferOutput(
            tokens_bought, deadline, recipient
        ).waitForReceipt()

    # tokenToEthSwapInput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapInput(
        self, tokens_sold: int, min_eth: int, deadline: int
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToEthSwapInput(
            tokens_sold, min_eth, deadline
        ).waitForReceipt()

    # tokenToEthTransferInput (uint256, uint256, uint256, address) -> (uint256)
    def tokenToEthTransferInput(
        self, tokens_sold: int, min_eth: int, deadline: int, recipient: Address
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToEthTransferInput(
            tokens_sold, min_eth, deadline, recipient
        ).waitForReceipt()

    # tokenToEthSwapOutput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapOutput(
        self, eth_bought: int, max_tokens: int, deadline: int
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToEthSwapOutput(
            eth_bought, max_tokens, deadline
        ).waitForReceipt()

    # tokenToEthTransferOutput (uint256, uint256, uint256, address) -> (uint256)
    def tokenToEthTransferOutput(
        self, eth_bought: int, max_tokens: int, deadline: int, recipient: Address
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToEthTransferOutput(
            eth_bought, max_tokens, deadline, recipient
        ).waitForReceipt()

    # tokenToTokenSwapInput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToTokenSwapInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        token_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToTokenSwapInput(
            tokens_sold, min_tokens_bought, min_eth_bought, deadline, token_addr
        ).waitForReceipt()

    # tokenToTokenTransferInput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToTokenTransferInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        recipient: Address,
        token_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToTokenTransferInput(
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            token_addr,
        ).waitForReceipt()

    # tokenToTokenSwapOutput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToTokenSwapOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        token_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToTokenSwapOutput(
            tokens_bought, max_tokens_sold, max_eth_sold, deadline, token_addr
        ).waitForReceipt()

    # tokenToTokenTransferOutput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToTokenTransferOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        recipient: Address,
        token_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToTokenTransferOutput(
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            token_addr,
        ).waitForReceipt()

    # tokenToExchangeSwapInput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToExchangeSwapInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        exchange_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToExchangeSwapInput(
            tokens_sold, min_tokens_bought, min_eth_bought, deadline, exchange_addr
        ).waitForReceipt()

    # tokenToExchangeTransferInput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToExchangeTransferInput(
        self,
        tokens_sold: int,
        min_tokens_bought: int,
        min_eth_bought: int,
        deadline: int,
        recipient: Address,
        exchange_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToExchangeTransferInput(
            tokens_sold,
            min_tokens_bought,
            min_eth_bought,
            deadline,
            recipient,
            exchange_addr,
        ).waitForReceipt()

    # tokenToExchangeSwapOutput (uint256, uint256, uint256, uint256, address) -> (uint256)
    def tokenToExchangeSwapOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        exchange_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToExchangeSwapOutput(
            tokens_bought, max_tokens_sold, max_eth_sold, deadline, exchange_addr
        ).waitForReceipt()

    # tokenToExchangeTransferOutput (uint256, uint256, uint256, uint256, address, address) -> (uint256)
    def tokenToExchangeTransferOutput(
        self,
        tokens_bought: int,
        max_tokens_sold: int,
        max_eth_sold: int,
        deadline: int,
        recipient: Address,
        exchange_addr: Address,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenToExchangeTransferOutput(
            tokens_bought,
            max_tokens_sold,
            max_eth_sold,
            deadline,
            recipient,
            exchange_addr,
        ).waitForReceipt()

    # getEthToTokenInputPrice (uint256) -> (uint256)
    def getEthToTokenInputPrice(self, eth_sold: int) -> UniswapV1ExchangeReceipt:
        return self.functions.getEthToTokenInputPrice(eth_sold).waitForReceipt()

    # getEthToTokenOutputPrice (uint256) -> (uint256)
    def getEthToTokenOutputPrice(self, tokens_bought: int) -> UniswapV1ExchangeReceipt:
        return self.functions.getEthToTokenOutputPrice(tokens_bought).waitForReceipt()

    # getTokenToEthInputPrice (uint256) -> (uint256)
    def getTokenToEthInputPrice(self, tokens_sold: int) -> UniswapV1ExchangeReceipt:
        return self.functions.getTokenToEthInputPrice(tokens_sold).waitForReceipt()

    # getTokenToEthOutputPrice (uint256) -> (uint256)
    def getTokenToEthOutputPrice(self, eth_bought: int) -> UniswapV1ExchangeReceipt:
        return self.functions.getTokenToEthOutputPrice(eth_bought).waitForReceipt()

    # tokenAddress () -> (address)
    def tokenAddress(
        self,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.tokenAddress().waitForReceipt()

    # factoryAddress () -> (address)
    def factoryAddress(
        self,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.factoryAddress().waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> UniswapV1ExchangeReceipt:
        return self.functions.balanceOf(owner).waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> UniswapV1ExchangeReceipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> UniswapV1ExchangeReceipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, owner: Address, spender: Address) -> UniswapV1ExchangeReceipt:
        return self.functions.allowance(owner, spender).waitForReceipt()

    # name () -> (bytes32)
    def name(
        self,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.name().waitForReceipt()

    # symbol () -> (bytes32)
    def symbol(
        self,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.symbol().waitForReceipt()

    # decimals () -> (uint256)
    def decimals(
        self,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.decimals().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> UniswapV1ExchangeReceipt:
        return self.functions.totalSupply().waitForReceipt()


# --------- end UniswapV1Exchange ----------


# ---------------------------------------------------------------
# WETH9

# ---
@dataclass
class WETH9ReceiptEvents:
    contract: "WETH9"
    web3_receipt: TxReceipt

    def Approval(self) -> Any:
        return (
            self.contract.to_web3().events.Approval().processReceipt(self.web3_receipt)
        )

    def Deposit(self) -> Any:
        return (
            self.contract.to_web3().events.Deposit().processReceipt(self.web3_receipt)
        )

    def Transfer(self) -> Any:
        return (
            self.contract.to_web3().events.Transfer().processReceipt(self.web3_receipt)
        )

    def Withdrawal(self) -> Any:
        return (
            self.contract.to_web3()
            .events.Withdrawal()
            .processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class WETH9Receipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: WETH9ReceiptEvents


# ---


class WETH9Functions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "WETH9"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> Function[int, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.allowance(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(self, guy: Address, wad: int) -> Function[bool, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        guy, wad = unsugar(guy), unsugar(wad)
        web3_fn = self.web3_contract.functions.approve(guy, wad)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> Function[int, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.balanceOf(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # deposit () -> ()
    def deposit(
        self,
    ):
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.deposit()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # symbol () -> (string)
    def symbol(
        self,
    ) -> Function[Any, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, wad: int) -> Function[bool, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        dst, wad = unsugar(dst), unsugar(wad)
        web3_fn = self.web3_contract.functions.transfer(dst, wad)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, src: Address, dst: Address, wad: int
    ) -> Function[bool, WETH9Receipt]:
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        src, dst, wad = unsugar(src), unsugar(dst), unsugar(wad)
        web3_fn = self.web3_contract.functions.transferFrom(src, dst, wad)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # withdraw (uint256) -> ()
    def withdraw(self, wad: int):
        def make_receipt(receipt: TxReceipt) -> WETH9Receipt:
            return WETH9Receipt(receipt, WETH9ReceiptEvents(self.contract, receipt))

        wad = unsugar(wad)
        web3_fn = self.web3_contract.functions.withdraw(wad)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class WETH9Caller:
    def __init__(self, functions: WETH9Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "WETH9Caller":
        return WETH9Caller(functions=self.functions, transaction=transaction)

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> int:
        return self.functions.allowance(item0, item1).call(self.transaction)

    # approve (address, uint256) -> (bool)
    def approve(self, guy: Address, wad: int) -> bool:
        return self.functions.approve(guy, wad).call(self.transaction)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> int:
        return self.functions.balanceOf(item0).call(self.transaction)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> int:
        return self.functions.decimals().call(self.transaction)

    # deposit () -> ()
    def deposit(
        self,
    ):
        return self.functions.deposit().call(self.transaction)

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
    def transfer(self, dst: Address, wad: int) -> bool:
        return self.functions.transfer(dst, wad).call(self.transaction)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, wad: int) -> bool:
        return self.functions.transferFrom(src, dst, wad).call(self.transaction)

    # withdraw (uint256) -> ()
    def withdraw(self, wad: int):
        return self.functions.withdraw(wad).call(self.transaction)


# ---


class WETH9(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["WETH9"]:
        if w3 is None:
            raise ValueError("In method WETH9.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("periphery/WETH9.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "WETH9":
            return WETH9(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/WETH9.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = WETH9Functions(w3, address, self.contract, self)
        self.call = WETH9Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> WETH9Receipt:
        return self.functions.allowance(item0, item1).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, guy: Address, wad: int) -> WETH9Receipt:
        return self.functions.approve(guy, wad).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> WETH9Receipt:
        return self.functions.balanceOf(item0).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> WETH9Receipt:
        return self.functions.decimals().waitForReceipt()

    # deposit () -> ()
    def deposit(
        self,
    ) -> WETH9Receipt:
        return self.functions.deposit().waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> WETH9Receipt:
        return self.functions.name().waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> WETH9Receipt:
        return self.functions.symbol().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> WETH9Receipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, dst: Address, wad: int) -> WETH9Receipt:
        return self.functions.transfer(dst, wad).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, src: Address, dst: Address, wad: int) -> WETH9Receipt:
        return self.functions.transferFrom(src, dst, wad).waitForReceipt()

    # withdraw (uint256) -> ()
    def withdraw(self, wad: int) -> WETH9Receipt:
        return self.functions.withdraw(wad).waitForReceipt()


# --------- end WETH9 ----------


# ---------------------------------------------------------------
# UniswapV2Router01

AddLiquidityOutput = namedtuple(
    "AddLiquidityOutput", [x.strip() for x in " amountA, amountB, liquidity".split(",")]
)
AddLiquidityETHOutput = namedtuple(
    "AddLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH, liquidity".split(",")],
)
RemoveLiquidityOutput = namedtuple(
    "RemoveLiquidityOutput", [x.strip() for x in " amountA, amountB".split(",")]
)
RemoveLiquidityETHOutput = namedtuple(
    "RemoveLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityETHWithPermitOutput = namedtuple(
    "RemoveLiquidityETHWithPermitOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityWithPermitOutput = namedtuple(
    "RemoveLiquidityWithPermitOutput",
    [x.strip() for x in " amountA, amountB".split(",")],
)
# ---
@dataclass
class UniswapV2Router01Receipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class UniswapV2Router01Functions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "UniswapV2Router01"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Function[Address, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        web3_fn = self.web3_contract.functions.WETH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityOutput, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        (
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(amountADesired),
            unsugar(amountBDesired),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        )

        def convert(args) -> AddLiquidityOutput:
            return AddLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityETHOutput, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(amountTokenDesired),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> AddLiquidityETHOutput:
            return AddLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> Function[int, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountOut, reserveIn, reserveOut = (
            unsugar(amountOut),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> Function[int, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountIn, reserveIn, reserveOut = (
            unsugar(amountIn),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountOut, path = unsugar(amountOut), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsIn(amountOut, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountIn, path = unsugar(amountIn), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsOut(amountIn, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> Function[int, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountA, reserveA, reserveB = (
            unsugar(amountA),
            unsugar(reserveA),
            unsugar(reserveB),
        )
        web3_fn = self.web3_contract.functions.quote(amountA, reserveA, reserveB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityOutput, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityOutput:
            return RemoveLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityETHOutput, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        token, liquidity, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityETHOutput:
            return RemoveLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityETHWithPermitOutput, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        (
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityETHWithPermitOutput:
            return RemoveLiquidityETHWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityWithPermitOutput, UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        (
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityWithPermitOutput:
            return RemoveLiquidityWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountOut, path, to, deadline = (
            unsugar(amountOut),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountOutMin, path, to, deadline = (
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], UniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> UniswapV2Router01Receipt:
            return UniswapV2Router01Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class UniswapV2Router01Caller:
    def __init__(self, functions: UniswapV2Router01Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "UniswapV2Router01Caller":
        return UniswapV2Router01Caller(
            functions=self.functions, transaction=transaction
        )

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Address:
        return self.functions.WETH().call(self.transaction)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityOutput:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).call(self.transaction)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityETHOutput:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(self, amountOut: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountIn(amountOut, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(self, amountIn: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountOut(amountIn, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(self, amountOut: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsIn(amountOut, path).call(self.transaction)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(self, amountIn: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsOut(amountIn, path).call(self.transaction)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(self, amountA: int, reserveA: int, reserveB: int) -> int:
        return self.functions.quote(amountA, reserveA, reserveB).call(self.transaction)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityOutput:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityETHOutput:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityETHWithPermitOutput:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityWithPermitOutput:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapETHForExactTokens(amountOut, path, to, deadline).call(
            self.transaction
        )

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)


# ---


class UniswapV2Router01(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factory: Address, WETH: Address
    ) -> PendingDeployment["UniswapV2Router01"]:
        if w3 is None:
            raise ValueError(
                "In method UniswapV2Router01.deploy(w3, ...) w3 must not be None"
            )

        factory, WETH = unsugar(factory), unsugar(WETH)
        json_path = BUILD_DIR.joinpath("periphery/UniswapV2Router01.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factory, WETH).transact()

        def on_receipt(receipt) -> "UniswapV2Router01":
            return UniswapV2Router01(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/UniswapV2Router01.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = UniswapV2Router01Functions(w3, address, self.contract, self)
        self.call = UniswapV2Router01Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> UniswapV2Router01Receipt:
        return self.functions.WETH().waitForReceipt()

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).waitForReceipt()

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # factory () -> (address)
    def factory(
        self,
    ) -> UniswapV2Router01Receipt:
        return self.functions.factory().waitForReceipt()

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> UniswapV2Router01Receipt:
        return self.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> UniswapV2Router01Receipt:
        return self.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> UniswapV2Router01Receipt:
        return self.functions.getAmountsIn(amountOut, path).waitForReceipt()

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> UniswapV2Router01Receipt:
        return self.functions.getAmountsOut(amountIn, path).waitForReceipt()

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> UniswapV2Router01Receipt:
        return self.functions.quote(amountA, reserveA, reserveB).waitForReceipt()

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> UniswapV2Router01Receipt:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> UniswapV2Router01Receipt:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> UniswapV2Router01Receipt:
        return self.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        ).waitForReceipt()

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> UniswapV2Router01Receipt:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> UniswapV2Router01Receipt:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()


# --------- end UniswapV2Router01 ----------


# ---------------------------------------------------------------
# ExampleOracleSimple

# ---
@dataclass
class ExampleOracleSimpleReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class ExampleOracleSimpleFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "ExampleOracleSimple",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # PERIOD () -> (uint256)
    def PERIOD(
        self,
    ) -> Function[int, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.PERIOD()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # blockTimestampLast () -> (uint32)
    def blockTimestampLast(
        self,
    ) -> Function[int, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.blockTimestampLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # consult (address, uint256) -> (uint256)
    def consult(
        self, token: Address, amountIn: int
    ) -> Function[int, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        token, amountIn = unsugar(token), unsugar(amountIn)
        web3_fn = self.web3_contract.functions.consult(token, amountIn)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # price0Average () -> (uint224)
    def price0Average(
        self,
    ) -> Function[Any, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.price0Average()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> Function[int, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.price0CumulativeLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # price1Average () -> (uint224)
    def price1Average(
        self,
    ) -> Function[Any, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.price1Average()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> Function[int, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.price1CumulativeLast()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # token0 () -> (address)
    def token0(
        self,
    ) -> Function[Address, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.token0()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # token1 () -> (address)
    def token1(
        self,
    ) -> Function[Address, ExampleOracleSimpleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.token1()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # update () -> ()
    def update(
        self,
    ):
        def make_receipt(receipt: TxReceipt) -> ExampleOracleSimpleReceipt:
            return ExampleOracleSimpleReceipt(receipt)

        web3_fn = self.web3_contract.functions.update()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class ExampleOracleSimpleCaller:
    def __init__(self, functions: ExampleOracleSimpleFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "ExampleOracleSimpleCaller":
        return ExampleOracleSimpleCaller(
            functions=self.functions, transaction=transaction
        )

    # PERIOD () -> (uint256)
    def PERIOD(
        self,
    ) -> int:
        return self.functions.PERIOD().call(self.transaction)

    # blockTimestampLast () -> (uint32)
    def blockTimestampLast(
        self,
    ) -> int:
        return self.functions.blockTimestampLast().call(self.transaction)

    # consult (address, uint256) -> (uint256)
    def consult(self, token: Address, amountIn: int) -> int:
        return self.functions.consult(token, amountIn).call(self.transaction)

    # price0Average () -> (uint224)
    def price0Average(
        self,
    ) -> Any:
        return self.functions.price0Average().call(self.transaction)

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> int:
        return self.functions.price0CumulativeLast().call(self.transaction)

    # price1Average () -> (uint224)
    def price1Average(
        self,
    ) -> Any:
        return self.functions.price1Average().call(self.transaction)

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> int:
        return self.functions.price1CumulativeLast().call(self.transaction)

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

    # update () -> ()
    def update(
        self,
    ):
        return self.functions.update().call(self.transaction)


# ---


class ExampleOracleSimple(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factory: Address, tokenA: Address, tokenB: Address
    ) -> PendingDeployment["ExampleOracleSimple"]:
        if w3 is None:
            raise ValueError(
                "In method ExampleOracleSimple.deploy(w3, ...) w3 must not be None"
            )

        factory, tokenA, tokenB = unsugar(factory), unsugar(tokenA), unsugar(tokenB)
        json_path = BUILD_DIR.joinpath("periphery/ExampleOracleSimple.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factory, tokenA, tokenB).transact()

        def on_receipt(receipt) -> "ExampleOracleSimple":
            return ExampleOracleSimple(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/ExampleOracleSimple.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = ExampleOracleSimpleFunctions(w3, address, self.contract, self)
        self.call = ExampleOracleSimpleCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # PERIOD () -> (uint256)
    def PERIOD(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.PERIOD().waitForReceipt()

    # blockTimestampLast () -> (uint32)
    def blockTimestampLast(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.blockTimestampLast().waitForReceipt()

    # consult (address, uint256) -> (uint256)
    def consult(self, token: Address, amountIn: int) -> ExampleOracleSimpleReceipt:
        return self.functions.consult(token, amountIn).waitForReceipt()

    # price0Average () -> (uint224)
    def price0Average(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.price0Average().waitForReceipt()

    # price0CumulativeLast () -> (uint256)
    def price0CumulativeLast(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.price0CumulativeLast().waitForReceipt()

    # price1Average () -> (uint224)
    def price1Average(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.price1Average().waitForReceipt()

    # price1CumulativeLast () -> (uint256)
    def price1CumulativeLast(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.price1CumulativeLast().waitForReceipt()

    # token0 () -> (address)
    def token0(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.token0().waitForReceipt()

    # token1 () -> (address)
    def token1(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.token1().waitForReceipt()

    # update () -> ()
    def update(
        self,
    ) -> ExampleOracleSimpleReceipt:
        return self.functions.update().waitForReceipt()


# --------- end ExampleOracleSimple ----------


# ---------------------------------------------------------------
# IUniswapV2Migrator

# ---
@dataclass
class IUniswapV2MigratorReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class IUniswapV2MigratorFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "IUniswapV2Migrator",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # migrate (address, uint256, uint256, address, uint256) -> ()
    def migrate(
        self,
        token: Address,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> IUniswapV2MigratorReceipt:
            return IUniswapV2MigratorReceipt(receipt)

        token, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.migrate(
            token, amountTokenMin, amountETHMin, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV2MigratorCaller:
    def __init__(self, functions: IUniswapV2MigratorFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV2MigratorCaller":
        return IUniswapV2MigratorCaller(
            functions=self.functions, transaction=transaction
        )

    # migrate (address, uint256, uint256, address, uint256) -> ()
    def migrate(
        self,
        token: Address,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ):
        return self.functions.migrate(
            token, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)


# ---


class IUniswapV2Migrator(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV2Migrator"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV2Migrator.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Migrator.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Migrator":
            return IUniswapV2Migrator(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Migrator.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV2MigratorFunctions(w3, address, self.contract, self)
        self.call = IUniswapV2MigratorCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # migrate (address, uint256, uint256, address, uint256) -> ()
    def migrate(
        self,
        token: Address,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2MigratorReceipt:
        return self.functions.migrate(
            token, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()


# --------- end IUniswapV2Migrator ----------


# ---------------------------------------------------------------
# ExampleSlidingWindowOracle

PairObservationsOutput = namedtuple(
    "PairObservationsOutput",
    [x.strip() for x in " timestamp, price0Cumulative, price1Cumulative".split(",")],
)
# ---
@dataclass
class ExampleSlidingWindowOracleReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class ExampleSlidingWindowOracleFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "ExampleSlidingWindowOracle",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # consult (address, uint256, address) -> (uint256)
    def consult(
        self, tokenIn: Address, amountIn: int, tokenOut: Address
    ) -> Function[int, ExampleSlidingWindowOracleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        tokenIn, amountIn, tokenOut = (
            unsugar(tokenIn),
            unsugar(amountIn),
            unsugar(tokenOut),
        )
        web3_fn = self.web3_contract.functions.consult(tokenIn, amountIn, tokenOut)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, ExampleSlidingWindowOracleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # granularity () -> (uint8)
    def granularity(
        self,
    ) -> Function[int, ExampleSlidingWindowOracleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        web3_fn = self.web3_contract.functions.granularity()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # observationIndexOf (uint256) -> (uint8)
    def observationIndexOf(
        self, timestamp: int
    ) -> Function[int, ExampleSlidingWindowOracleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        timestamp = unsugar(timestamp)
        web3_fn = self.web3_contract.functions.observationIndexOf(timestamp)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # pairObservations (address, uint256) -> (uint256, uint256, uint256)
    def pairObservations(
        self, item0: Address, item1: int
    ) -> Function[PairObservationsOutput, ExampleSlidingWindowOracleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.pairObservations(item0, item1)

        def convert(args) -> PairObservationsOutput:
            return PairObservationsOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # periodSize () -> (uint256)
    def periodSize(
        self,
    ) -> Function[int, ExampleSlidingWindowOracleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        web3_fn = self.web3_contract.functions.periodSize()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # update (address, address) -> ()
    def update(self, tokenA: Address, tokenB: Address):
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        tokenA, tokenB = unsugar(tokenA), unsugar(tokenB)
        web3_fn = self.web3_contract.functions.update(tokenA, tokenB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # windowSize () -> (uint256)
    def windowSize(
        self,
    ) -> Function[int, ExampleSlidingWindowOracleReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleSlidingWindowOracleReceipt:
            return ExampleSlidingWindowOracleReceipt(receipt)

        web3_fn = self.web3_contract.functions.windowSize()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class ExampleSlidingWindowOracleCaller:
    def __init__(
        self, functions: ExampleSlidingWindowOracleFunctions, transaction=None
    ):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "ExampleSlidingWindowOracleCaller":
        return ExampleSlidingWindowOracleCaller(
            functions=self.functions, transaction=transaction
        )

    # consult (address, uint256, address) -> (uint256)
    def consult(self, tokenIn: Address, amountIn: int, tokenOut: Address) -> int:
        return self.functions.consult(tokenIn, amountIn, tokenOut).call(
            self.transaction
        )

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # granularity () -> (uint8)
    def granularity(
        self,
    ) -> int:
        return self.functions.granularity().call(self.transaction)

    # observationIndexOf (uint256) -> (uint8)
    def observationIndexOf(self, timestamp: int) -> int:
        return self.functions.observationIndexOf(timestamp).call(self.transaction)

    # pairObservations (address, uint256) -> (uint256, uint256, uint256)
    def pairObservations(self, item0: Address, item1: int) -> PairObservationsOutput:
        return self.functions.pairObservations(item0, item1).call(self.transaction)

    # periodSize () -> (uint256)
    def periodSize(
        self,
    ) -> int:
        return self.functions.periodSize().call(self.transaction)

    # update (address, address) -> ()
    def update(self, tokenA: Address, tokenB: Address):
        return self.functions.update(tokenA, tokenB).call(self.transaction)

    # windowSize () -> (uint256)
    def windowSize(
        self,
    ) -> int:
        return self.functions.windowSize().call(self.transaction)


# ---


class ExampleSlidingWindowOracle(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factory_: Address, windowSize_: int, granularity_: int
    ) -> PendingDeployment["ExampleSlidingWindowOracle"]:
        if w3 is None:
            raise ValueError(
                "In method ExampleSlidingWindowOracle.deploy(w3, ...) w3 must not be None"
            )

        factory_, windowSize_, granularity_ = (
            unsugar(factory_),
            unsugar(windowSize_),
            unsugar(granularity_),
        )
        json_path = BUILD_DIR.joinpath(
            "periphery/ExampleSlidingWindowOracle.json"
        ).resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factory_, windowSize_, granularity_).transact()

        def on_receipt(receipt) -> "ExampleSlidingWindowOracle":
            return ExampleSlidingWindowOracle(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath(
            "periphery/ExampleSlidingWindowOracle.json"
        ).resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = ExampleSlidingWindowOracleFunctions(
            w3, address, self.contract, self
        )
        self.call = ExampleSlidingWindowOracleCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # consult (address, uint256, address) -> (uint256)
    def consult(
        self, tokenIn: Address, amountIn: int, tokenOut: Address
    ) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.consult(tokenIn, amountIn, tokenOut).waitForReceipt()

    # factory () -> (address)
    def factory(
        self,
    ) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.factory().waitForReceipt()

    # granularity () -> (uint8)
    def granularity(
        self,
    ) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.granularity().waitForReceipt()

    # observationIndexOf (uint256) -> (uint8)
    def observationIndexOf(self, timestamp: int) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.observationIndexOf(timestamp).waitForReceipt()

    # pairObservations (address, uint256) -> (uint256, uint256, uint256)
    def pairObservations(
        self, item0: Address, item1: int
    ) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.pairObservations(item0, item1).waitForReceipt()

    # periodSize () -> (uint256)
    def periodSize(
        self,
    ) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.periodSize().waitForReceipt()

    # update (address, address) -> ()
    def update(
        self, tokenA: Address, tokenB: Address
    ) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.update(tokenA, tokenB).waitForReceipt()

    # windowSize () -> (uint256)
    def windowSize(
        self,
    ) -> ExampleSlidingWindowOracleReceipt:
        return self.functions.windowSize().waitForReceipt()


# --------- end ExampleSlidingWindowOracle ----------


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
        json_path = BUILD_DIR.joinpath("periphery/ERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(totalSupply).transact()

        def on_receipt(receipt) -> "ERC20":
            return ERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/ERC20.json").resolve()
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
# FixedPoint

# ---
@dataclass
class FixedPointReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class FixedPointFunctions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "FixedPoint"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # Q112 () -> (uint256)
    def Q112(
        self,
    ) -> Function[int, FixedPointReceipt]:
        def make_receipt(receipt: TxReceipt) -> FixedPointReceipt:
            return FixedPointReceipt(receipt)

        web3_fn = self.web3_contract.functions.Q112()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # RESOLUTION () -> (uint8)
    def RESOLUTION(
        self,
    ) -> Function[int, FixedPointReceipt]:
        def make_receipt(receipt: TxReceipt) -> FixedPointReceipt:
            return FixedPointReceipt(receipt)

        web3_fn = self.web3_contract.functions.RESOLUTION()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class FixedPointCaller:
    def __init__(self, functions: FixedPointFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "FixedPointCaller":
        return FixedPointCaller(functions=self.functions, transaction=transaction)

    # Q112 () -> (uint256)
    def Q112(
        self,
    ) -> int:
        return self.functions.Q112().call(self.transaction)

    # RESOLUTION () -> (uint8)
    def RESOLUTION(
        self,
    ) -> int:
        return self.functions.RESOLUTION().call(self.transaction)


# ---


class FixedPoint(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["FixedPoint"]:
        if w3 is None:
            raise ValueError("In method FixedPoint.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("periphery/FixedPoint.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "FixedPoint":
            return FixedPoint(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/FixedPoint.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = FixedPointFunctions(w3, address, self.contract, self)
        self.call = FixedPointCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # Q112 () -> (uint256)
    def Q112(
        self,
    ) -> FixedPointReceipt:
        return self.functions.Q112().waitForReceipt()

    # RESOLUTION () -> (uint8)
    def RESOLUTION(
        self,
    ) -> FixedPointReceipt:
        return self.functions.RESOLUTION().waitForReceipt()


# --------- end FixedPoint ----------


# ---------------------------------------------------------------
# IUniswapV1Exchange

RemoveLiquidityOutput = namedtuple(
    "RemoveLiquidityOutput", [x.strip() for x in " item0, item1".split(",")]
)
# ---
@dataclass
class IUniswapV1ExchangeReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class IUniswapV1ExchangeFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "IUniswapV1Exchange",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> Function[int, IUniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV1ExchangeReceipt:
            return IUniswapV1ExchangeReceipt(receipt)

        owner = unsugar(owner)
        web3_fn = self.web3_contract.functions.balanceOf(owner)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # ethToTokenSwapInput (uint256, uint256) -> (uint256)
    def ethToTokenSwapInput(
        self, item0: int, item1: int
    ) -> Function[int, IUniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV1ExchangeReceipt:
            return IUniswapV1ExchangeReceipt(receipt)

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.ethToTokenSwapInput(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidity (uint256, uint256, uint256, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self, item0: int, item1: int, item2: int, item3: int
    ) -> Function[RemoveLiquidityOutput, IUniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV1ExchangeReceipt:
            return IUniswapV1ExchangeReceipt(receipt)

        item0, item1, item2, item3 = (
            unsugar(item0),
            unsugar(item1),
            unsugar(item2),
            unsugar(item3),
        )
        web3_fn = self.web3_contract.functions.removeLiquidity(
            item0, item1, item2, item3
        )

        def convert(args) -> RemoveLiquidityOutput:
            return RemoveLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # tokenToEthSwapInput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapInput(
        self, item0: int, item1: int, item2: int
    ) -> Function[int, IUniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV1ExchangeReceipt:
            return IUniswapV1ExchangeReceipt(receipt)

        item0, item1, item2 = unsugar(item0), unsugar(item1), unsugar(item2)
        web3_fn = self.web3_contract.functions.tokenToEthSwapInput(item0, item1, item2)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, IUniswapV1ExchangeReceipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV1ExchangeReceipt:
            return IUniswapV1ExchangeReceipt(receipt)

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV1ExchangeCaller:
    def __init__(self, functions: IUniswapV1ExchangeFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV1ExchangeCaller":
        return IUniswapV1ExchangeCaller(
            functions=self.functions, transaction=transaction
        )

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> int:
        return self.functions.balanceOf(owner).call(self.transaction)

    # ethToTokenSwapInput (uint256, uint256) -> (uint256)
    def ethToTokenSwapInput(self, item0: int, item1: int) -> int:
        return self.functions.ethToTokenSwapInput(item0, item1).call(self.transaction)

    # removeLiquidity (uint256, uint256, uint256, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self, item0: int, item1: int, item2: int, item3: int
    ) -> RemoveLiquidityOutput:
        return self.functions.removeLiquidity(item0, item1, item2, item3).call(
            self.transaction
        )

    # tokenToEthSwapInput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapInput(self, item0: int, item1: int, item2: int) -> int:
        return self.functions.tokenToEthSwapInput(item0, item1, item2).call(
            self.transaction
        )

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(self, from_: Address, to: Address, value: int) -> bool:
        return self.functions.transferFrom(from_, to, value).call(self.transaction)


# ---


class IUniswapV1Exchange(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV1Exchange"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV1Exchange.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV1Exchange.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV1Exchange":
            return IUniswapV1Exchange(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV1Exchange.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV1ExchangeFunctions(w3, address, self.contract, self)
        self.call = IUniswapV1ExchangeCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # balanceOf (address) -> (uint256)
    def balanceOf(self, owner: Address) -> IUniswapV1ExchangeReceipt:
        return self.functions.balanceOf(owner).waitForReceipt()

    # ethToTokenSwapInput (uint256, uint256) -> (uint256)
    def ethToTokenSwapInput(self, item0: int, item1: int) -> IUniswapV1ExchangeReceipt:
        return self.functions.ethToTokenSwapInput(item0, item1).waitForReceipt()

    # removeLiquidity (uint256, uint256, uint256, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self, item0: int, item1: int, item2: int, item3: int
    ) -> IUniswapV1ExchangeReceipt:
        return self.functions.removeLiquidity(
            item0, item1, item2, item3
        ).waitForReceipt()

    # tokenToEthSwapInput (uint256, uint256, uint256) -> (uint256)
    def tokenToEthSwapInput(
        self, item0: int, item1: int, item2: int
    ) -> IUniswapV1ExchangeReceipt:
        return self.functions.tokenToEthSwapInput(item0, item1, item2).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> IUniswapV1ExchangeReceipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end IUniswapV1Exchange ----------


# ---------------------------------------------------------------
# IUniswapV2Router01

AddLiquidityOutput = namedtuple(
    "AddLiquidityOutput", [x.strip() for x in " amountA, amountB, liquidity".split(",")]
)
AddLiquidityETHOutput = namedtuple(
    "AddLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH, liquidity".split(",")],
)
RemoveLiquidityOutput = namedtuple(
    "RemoveLiquidityOutput", [x.strip() for x in " amountA, amountB".split(",")]
)
RemoveLiquidityETHOutput = namedtuple(
    "RemoveLiquidityETHOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityETHWithPermitOutput = namedtuple(
    "RemoveLiquidityETHWithPermitOutput",
    [x.strip() for x in " amountToken, amountETH".split(",")],
)
RemoveLiquidityWithPermitOutput = namedtuple(
    "RemoveLiquidityWithPermitOutput",
    [x.strip() for x in " amountA, amountB".split(",")],
)
# ---
@dataclass
class IUniswapV2Router01Receipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class IUniswapV2Router01Functions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "IUniswapV2Router01",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Function[Address, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        web3_fn = self.web3_contract.functions.WETH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityOutput, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        (
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(amountADesired),
            unsugar(amountBDesired),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        )

        def convert(args) -> AddLiquidityOutput:
            return AddLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[AddLiquidityETHOutput, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(amountTokenDesired),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> AddLiquidityETHOutput:
            return AddLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> Function[int, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountOut, reserveIn, reserveOut = (
            unsugar(amountOut),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> Function[int, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountIn, reserveIn, reserveOut = (
            unsugar(amountIn),
            unsugar(reserveIn),
            unsugar(reserveOut),
        )
        web3_fn = self.web3_contract.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountOut, path = unsugar(amountOut), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsIn(amountOut, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountIn, path = unsugar(amountIn), unsugar(path)
        web3_fn = self.web3_contract.functions.getAmountsOut(amountIn, path)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> Function[int, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountA, reserveA, reserveB = (
            unsugar(amountA),
            unsugar(reserveA),
            unsugar(reserveB),
        )
        web3_fn = self.web3_contract.functions.quote(amountA, reserveA, reserveB)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityOutput, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityOutput:
            return RemoveLiquidityOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> Function[RemoveLiquidityETHOutput, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        token, liquidity, amountTokenMin, amountETHMin, to, deadline = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        )

        def convert(args) -> RemoveLiquidityETHOutput:
            return RemoveLiquidityETHOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityETHWithPermitOutput, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        (
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(token),
            unsugar(liquidity),
            unsugar(amountTokenMin),
            unsugar(amountETHMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityETHWithPermitOutput:
            return RemoveLiquidityETHWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> Function[RemoveLiquidityWithPermitOutput, IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        (
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ) = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidity),
            unsugar(amountAMin),
            unsugar(amountBMin),
            unsugar(to),
            unsugar(deadline),
            unsugar(approveMax),
            unsugar(v),
            unsugar(r),
            unsugar(s),
        )
        web3_fn = self.web3_contract.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        )

        def convert(args) -> RemoveLiquidityWithPermitOutput:
            return RemoveLiquidityWithPermitOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountOut, path, to, deadline = (
            unsugar(amountOut),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountOutMin, path, to, deadline = (
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountIn, amountOutMin, path, to, deadline = (
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> Function[List[int], IUniswapV2Router01Receipt]:
        def make_receipt(receipt: TxReceipt) -> IUniswapV2Router01Receipt:
            return IUniswapV2Router01Receipt(receipt)

        amountOut, amountInMax, path, to, deadline = (
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IUniswapV2Router01Caller:
    def __init__(self, functions: IUniswapV2Router01Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IUniswapV2Router01Caller":
        return IUniswapV2Router01Caller(
            functions=self.functions, transaction=transaction
        )

    # WETH () -> (address)
    def WETH(
        self,
    ) -> Address:
        return self.functions.WETH().call(self.transaction)

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityOutput:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).call(self.transaction)

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> AddLiquidityETHOutput:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(self, amountOut: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountIn(amountOut, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(self, amountIn: int, reserveIn: int, reserveOut: int) -> int:
        return self.functions.getAmountOut(amountIn, reserveIn, reserveOut).call(
            self.transaction
        )

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(self, amountOut: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsIn(amountOut, path).call(self.transaction)

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(self, amountIn: int, path: List[Address]) -> List[int]:
        return self.functions.getAmountsOut(amountIn, path).call(self.transaction)

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(self, amountA: int, reserveA: int, reserveB: int) -> int:
        return self.functions.quote(amountA, reserveA, reserveB).call(self.transaction)

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityOutput:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> RemoveLiquidityETHOutput:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).call(self.transaction)

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityETHWithPermitOutput:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> RemoveLiquidityWithPermitOutput:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).call(self.transaction)

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapETHForExactTokens(amountOut, path, to, deadline).call(
            self.transaction
        )

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> List[int]:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> List[int]:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)


# ---


class IUniswapV2Router01(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IUniswapV2Router01"]:
        if w3 is None:
            raise ValueError(
                "In method IUniswapV2Router01.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Router01.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Router01":
            return IUniswapV2Router01(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Router01.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IUniswapV2Router01Functions(w3, address, self.contract, self)
        self.call = IUniswapV2Router01Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # WETH () -> (address)
    def WETH(
        self,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.WETH().waitForReceipt()

    # addLiquidity (address, address, uint256, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        amountADesired: int,
        amountBDesired: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.addLiquidity(
            tokenA,
            tokenB,
            amountADesired,
            amountBDesired,
            amountAMin,
            amountBMin,
            to,
            deadline,
        ).waitForReceipt()

    # addLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256, uint256)
    def addLiquidityETH(
        self,
        token: Address,
        amountTokenDesired: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.addLiquidityETH(
            token, amountTokenDesired, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # factory () -> (address)
    def factory(
        self,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.factory().waitForReceipt()

    # getAmountIn (uint256, uint256, uint256) -> (uint256)
    def getAmountIn(
        self, amountOut: int, reserveIn: int, reserveOut: int
    ) -> IUniswapV2Router01Receipt:
        return self.functions.getAmountIn(
            amountOut, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountOut (uint256, uint256, uint256) -> (uint256)
    def getAmountOut(
        self, amountIn: int, reserveIn: int, reserveOut: int
    ) -> IUniswapV2Router01Receipt:
        return self.functions.getAmountOut(
            amountIn, reserveIn, reserveOut
        ).waitForReceipt()

    # getAmountsIn (uint256, address[]) -> (uint256[])
    def getAmountsIn(
        self, amountOut: int, path: List[Address]
    ) -> IUniswapV2Router01Receipt:
        return self.functions.getAmountsIn(amountOut, path).waitForReceipt()

    # getAmountsOut (uint256, address[]) -> (uint256[])
    def getAmountsOut(
        self, amountIn: int, path: List[Address]
    ) -> IUniswapV2Router01Receipt:
        return self.functions.getAmountsOut(amountIn, path).waitForReceipt()

    # quote (uint256, uint256, uint256) -> (uint256)
    def quote(
        self, amountA: int, reserveA: int, reserveB: int
    ) -> IUniswapV2Router01Receipt:
        return self.functions.quote(amountA, reserveA, reserveB).waitForReceipt()

    # removeLiquidity (address, address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidity(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.removeLiquidity(
            tokenA, tokenB, liquidity, amountAMin, amountBMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETH (address, uint256, uint256, uint256, address, uint256) -> (uint256, uint256)
    def removeLiquidityETH(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.removeLiquidityETH(
            token, liquidity, amountTokenMin, amountETHMin, to, deadline
        ).waitForReceipt()

    # removeLiquidityETHWithPermit (address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityETHWithPermit(
        self,
        token: Address,
        liquidity: int,
        amountTokenMin: int,
        amountETHMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> IUniswapV2Router01Receipt:
        return self.functions.removeLiquidityETHWithPermit(
            token,
            liquidity,
            amountTokenMin,
            amountETHMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # removeLiquidityWithPermit (address, address, uint256, uint256, uint256, address, uint256, bool, uint8, bytes32, bytes32) -> (uint256, uint256)
    def removeLiquidityWithPermit(
        self,
        tokenA: Address,
        tokenB: Address,
        liquidity: int,
        amountAMin: int,
        amountBMin: int,
        to: Address,
        deadline: int,
        approveMax: bool,
        v: int,
        r: Union[bytearray, str, HexBytes],
        s: Union[bytearray, str, HexBytes],
    ) -> IUniswapV2Router01Receipt:
        return self.functions.removeLiquidityWithPermit(
            tokenA,
            tokenB,
            liquidity,
            amountAMin,
            amountBMin,
            to,
            deadline,
            approveMax,
            v,
            r,
            s,
        ).waitForReceipt()

    # swapETHForExactTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapETHForExactTokens(
        self, amountOut: int, path: List[Address], to: Address, deadline: int
    ) -> IUniswapV2Router01Receipt:
        return self.functions.swapETHForExactTokens(
            amountOut, path, to, deadline
        ).waitForReceipt()

    # swapExactETHForTokens (uint256, address[], address, uint256) -> (uint256[])
    def swapExactETHForTokens(
        self, amountOutMin: int, path: List[Address], to: Address, deadline: int
    ) -> IUniswapV2Router01Receipt:
        return self.functions.swapExactETHForTokens(
            amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForETH(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.swapExactTokensForETH(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapExactTokensForTokens(
        self,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.swapExactTokensForTokens(
            amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactETH (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactETH(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.swapTokensForExactETH(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactTokens (uint256, uint256, address[], address, uint256) -> (uint256[])
    def swapTokensForExactTokens(
        self,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> IUniswapV2Router01Receipt:
        return self.functions.swapTokensForExactTokens(
            amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()


# --------- end IUniswapV2Router01 ----------


# ---------------------------------------------------------------
# IWETH

# ---
@dataclass
class IWETHReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class IWETHFunctions:
    def __init__(self, w3: Web3, address: str, web3_contract: Web3, contract: "IWETH"):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # deposit () -> ()
    def deposit(
        self,
    ):
        def make_receipt(receipt: TxReceipt) -> IWETHReceipt:
            return IWETHReceipt(receipt)

        web3_fn = self.web3_contract.functions.deposit()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> Function[bool, IWETHReceipt]:
        def make_receipt(receipt: TxReceipt) -> IWETHReceipt:
            return IWETHReceipt(receipt)

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # withdraw (uint256) -> ()
    def withdraw(self, item0: int):
        def make_receipt(receipt: TxReceipt) -> IWETHReceipt:
            return IWETHReceipt(receipt)

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.withdraw(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class IWETHCaller:
    def __init__(self, functions: IWETHFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "IWETHCaller":
        return IWETHCaller(functions=self.functions, transaction=transaction)

    # deposit () -> ()
    def deposit(
        self,
    ):
        return self.functions.deposit().call(self.transaction)

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> bool:
        return self.functions.transfer(to, value).call(self.transaction)

    # withdraw (uint256) -> ()
    def withdraw(self, item0: int):
        return self.functions.withdraw(item0).call(self.transaction)


# ---


class IWETH(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["IWETH"]:
        if w3 is None:
            raise ValueError("In method IWETH.deploy(w3, ...) w3 must not be None")

        json_path = BUILD_DIR.joinpath("periphery/IWETH.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IWETH":
            return IWETH(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IWETH.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = IWETHFunctions(w3, address, self.contract, self)
        self.call = IWETHCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # deposit () -> ()
    def deposit(
        self,
    ) -> IWETHReceipt:
        return self.functions.deposit().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> IWETHReceipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # withdraw (uint256) -> ()
    def withdraw(self, item0: int) -> IWETHReceipt:
        return self.functions.withdraw(item0).waitForReceipt()


# --------- end IWETH ----------


# ---------------------------------------------------------------
# ExampleComputeLiquidityValue

GetLiquidityValueOutput = namedtuple(
    "GetLiquidityValueOutput",
    [x.strip() for x in " tokenAAmount, tokenBAmount".split(",")],
)
GetLiquidityValueAfterArbitrageToPriceOutput = namedtuple(
    "GetLiquidityValueAfterArbitrageToPriceOutput",
    [x.strip() for x in " tokenAAmount, tokenBAmount".split(",")],
)
GetReservesAfterArbitrageOutput = namedtuple(
    "GetReservesAfterArbitrageOutput",
    [x.strip() for x in " reserveA, reserveB".split(",")],
)
# ---
@dataclass
class ExampleComputeLiquidityValueReceipt(TransactionReceipt):
    web3_receipt: TxReceipt


# ---


class ExampleComputeLiquidityValueFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "ExampleComputeLiquidityValue",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # factory () -> (address)
    def factory(
        self,
    ) -> Function[Address, ExampleComputeLiquidityValueReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleComputeLiquidityValueReceipt:
            return ExampleComputeLiquidityValueReceipt(receipt)

        web3_fn = self.web3_contract.functions.factory()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getGasCostOfGetLiquidityValueAfterArbitrageToPrice (address, address, uint256, uint256, uint256) -> (uint256)
    def getGasCostOfGetLiquidityValueAfterArbitrageToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        liquidityAmount: int,
    ) -> Function[int, ExampleComputeLiquidityValueReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleComputeLiquidityValueReceipt:
            return ExampleComputeLiquidityValueReceipt(receipt)

        tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(truePriceTokenA),
            unsugar(truePriceTokenB),
            unsugar(liquidityAmount),
        )
        web3_fn = self.web3_contract.functions.getGasCostOfGetLiquidityValueAfterArbitrageToPrice(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # getLiquidityValue (address, address, uint256) -> (uint256, uint256)
    def getLiquidityValue(
        self, tokenA: Address, tokenB: Address, liquidityAmount: int
    ) -> Function[GetLiquidityValueOutput, ExampleComputeLiquidityValueReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleComputeLiquidityValueReceipt:
            return ExampleComputeLiquidityValueReceipt(receipt)

        tokenA, tokenB, liquidityAmount = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(liquidityAmount),
        )
        web3_fn = self.web3_contract.functions.getLiquidityValue(
            tokenA, tokenB, liquidityAmount
        )

        def convert(args) -> GetLiquidityValueOutput:
            return GetLiquidityValueOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # getLiquidityValueAfterArbitrageToPrice (address, address, uint256, uint256, uint256) -> (uint256, uint256)
    def getLiquidityValueAfterArbitrageToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        liquidityAmount: int,
    ) -> Function[
        GetLiquidityValueAfterArbitrageToPriceOutput,
        ExampleComputeLiquidityValueReceipt,
    ]:
        def make_receipt(receipt: TxReceipt) -> ExampleComputeLiquidityValueReceipt:
            return ExampleComputeLiquidityValueReceipt(receipt)

        tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(truePriceTokenA),
            unsugar(truePriceTokenB),
            unsugar(liquidityAmount),
        )
        web3_fn = self.web3_contract.functions.getLiquidityValueAfterArbitrageToPrice(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount
        )

        def convert(args) -> GetLiquidityValueAfterArbitrageToPriceOutput:
            return GetLiquidityValueAfterArbitrageToPriceOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)

    # getReservesAfterArbitrage (address, address, uint256, uint256) -> (uint256, uint256)
    def getReservesAfterArbitrage(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
    ) -> Function[GetReservesAfterArbitrageOutput, ExampleComputeLiquidityValueReceipt]:
        def make_receipt(receipt: TxReceipt) -> ExampleComputeLiquidityValueReceipt:
            return ExampleComputeLiquidityValueReceipt(receipt)

        tokenA, tokenB, truePriceTokenA, truePriceTokenB = (
            unsugar(tokenA),
            unsugar(tokenB),
            unsugar(truePriceTokenA),
            unsugar(truePriceTokenB),
        )
        web3_fn = self.web3_contract.functions.getReservesAfterArbitrage(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB
        )

        def convert(args) -> GetReservesAfterArbitrageOutput:
            return GetReservesAfterArbitrageOutput(*args)

        return Function(self.w3, web3_fn, convert=convert, make_receipt=make_receipt)


# ---


class ExampleComputeLiquidityValueCaller:
    def __init__(
        self, functions: ExampleComputeLiquidityValueFunctions, transaction=None
    ):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "ExampleComputeLiquidityValueCaller":
        return ExampleComputeLiquidityValueCaller(
            functions=self.functions, transaction=transaction
        )

    # factory () -> (address)
    def factory(
        self,
    ) -> Address:
        return self.functions.factory().call(self.transaction)

    # getGasCostOfGetLiquidityValueAfterArbitrageToPrice (address, address, uint256, uint256, uint256) -> (uint256)
    def getGasCostOfGetLiquidityValueAfterArbitrageToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        liquidityAmount: int,
    ) -> int:
        return self.functions.getGasCostOfGetLiquidityValueAfterArbitrageToPrice(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount
        ).call(self.transaction)

    # getLiquidityValue (address, address, uint256) -> (uint256, uint256)
    def getLiquidityValue(
        self, tokenA: Address, tokenB: Address, liquidityAmount: int
    ) -> GetLiquidityValueOutput:
        return self.functions.getLiquidityValue(tokenA, tokenB, liquidityAmount).call(
            self.transaction
        )

    # getLiquidityValueAfterArbitrageToPrice (address, address, uint256, uint256, uint256) -> (uint256, uint256)
    def getLiquidityValueAfterArbitrageToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        liquidityAmount: int,
    ) -> GetLiquidityValueAfterArbitrageToPriceOutput:
        return self.functions.getLiquidityValueAfterArbitrageToPrice(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount
        ).call(self.transaction)

    # getReservesAfterArbitrage (address, address, uint256, uint256) -> (uint256, uint256)
    def getReservesAfterArbitrage(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
    ) -> GetReservesAfterArbitrageOutput:
        return self.functions.getReservesAfterArbitrage(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB
        ).call(self.transaction)


# ---


class ExampleComputeLiquidityValue(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3, factory_: Address
    ) -> PendingDeployment["ExampleComputeLiquidityValue"]:
        if w3 is None:
            raise ValueError(
                "In method ExampleComputeLiquidityValue.deploy(w3, ...) w3 must not be None"
            )

        factory_ = unsugar(factory_)
        json_path = BUILD_DIR.joinpath(
            "periphery/ExampleComputeLiquidityValue.json"
        ).resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(factory_).transact()

        def on_receipt(receipt) -> "ExampleComputeLiquidityValue":
            return ExampleComputeLiquidityValue(
                address=receipt["contractAddress"], w3=w3
            )

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath(
            "periphery/ExampleComputeLiquidityValue.json"
        ).resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = ExampleComputeLiquidityValueFunctions(
            w3, address, self.contract, self
        )
        self.call = ExampleComputeLiquidityValueCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # factory () -> (address)
    def factory(
        self,
    ) -> ExampleComputeLiquidityValueReceipt:
        return self.functions.factory().waitForReceipt()

    # getGasCostOfGetLiquidityValueAfterArbitrageToPrice (address, address, uint256, uint256, uint256) -> (uint256)
    def getGasCostOfGetLiquidityValueAfterArbitrageToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        liquidityAmount: int,
    ) -> ExampleComputeLiquidityValueReceipt:
        return self.functions.getGasCostOfGetLiquidityValueAfterArbitrageToPrice(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount
        ).waitForReceipt()

    # getLiquidityValue (address, address, uint256) -> (uint256, uint256)
    def getLiquidityValue(
        self, tokenA: Address, tokenB: Address, liquidityAmount: int
    ) -> ExampleComputeLiquidityValueReceipt:
        return self.functions.getLiquidityValue(
            tokenA, tokenB, liquidityAmount
        ).waitForReceipt()

    # getLiquidityValueAfterArbitrageToPrice (address, address, uint256, uint256, uint256) -> (uint256, uint256)
    def getLiquidityValueAfterArbitrageToPrice(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
        liquidityAmount: int,
    ) -> ExampleComputeLiquidityValueReceipt:
        return self.functions.getLiquidityValueAfterArbitrageToPrice(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB, liquidityAmount
        ).waitForReceipt()

    # getReservesAfterArbitrage (address, address, uint256, uint256) -> (uint256, uint256)
    def getReservesAfterArbitrage(
        self,
        tokenA: Address,
        tokenB: Address,
        truePriceTokenA: int,
        truePriceTokenB: int,
    ) -> ExampleComputeLiquidityValueReceipt:
        return self.functions.getReservesAfterArbitrage(
            tokenA, tokenB, truePriceTokenA, truePriceTokenB
        ).waitForReceipt()


# --------- end ExampleComputeLiquidityValue ----------


# ---------------------------------------------------------------
# RouterEventEmitter

# ---
@dataclass
class RouterEventEmitterReceiptEvents:
    contract: "RouterEventEmitter"
    web3_receipt: TxReceipt

    def Amounts(self) -> Any:
        return (
            self.contract.to_web3().events.Amounts().processReceipt(self.web3_receipt)
        )


# ---


@dataclass
class RouterEventEmitterReceipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: RouterEventEmitterReceiptEvents


# ---


class RouterEventEmitterFunctions:
    def __init__(
        self,
        w3: Web3,
        address: str,
        web3_contract: Web3,
        contract: "RouterEventEmitter",
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # swapETHForExactTokens (address, uint256, address[], address, uint256) -> ()
    def swapETHForExactTokens(
        self,
        router: Address,
        amountOut: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> RouterEventEmitterReceipt:
            return RouterEventEmitterReceipt(
                receipt, RouterEventEmitterReceiptEvents(self.contract, receipt)
            )

        router, amountOut, path, to, deadline = (
            unsugar(router),
            unsugar(amountOut),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapETHForExactTokens(
            router, amountOut, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactETHForTokens (address, uint256, address[], address, uint256) -> ()
    def swapExactETHForTokens(
        self,
        router: Address,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> RouterEventEmitterReceipt:
            return RouterEventEmitterReceipt(
                receipt, RouterEventEmitterReceiptEvents(self.contract, receipt)
            )

        router, amountOutMin, path, to, deadline = (
            unsugar(router),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactETHForTokens(
            router, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForETH (address, uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETH(
        self,
        router: Address,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> RouterEventEmitterReceipt:
            return RouterEventEmitterReceipt(
                receipt, RouterEventEmitterReceiptEvents(self.contract, receipt)
            )

        router, amountIn, amountOutMin, path, to, deadline = (
            unsugar(router),
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForETH(
            router, amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapExactTokensForTokens (address, uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokens(
        self,
        router: Address,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> RouterEventEmitterReceipt:
            return RouterEventEmitterReceipt(
                receipt, RouterEventEmitterReceiptEvents(self.contract, receipt)
            )

        router, amountIn, amountOutMin, path, to, deadline = (
            unsugar(router),
            unsugar(amountIn),
            unsugar(amountOutMin),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapExactTokensForTokens(
            router, amountIn, amountOutMin, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactETH (address, uint256, uint256, address[], address, uint256) -> ()
    def swapTokensForExactETH(
        self,
        router: Address,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> RouterEventEmitterReceipt:
            return RouterEventEmitterReceipt(
                receipt, RouterEventEmitterReceiptEvents(self.contract, receipt)
            )

        router, amountOut, amountInMax, path, to, deadline = (
            unsugar(router),
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactETH(
            router, amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # swapTokensForExactTokens (address, uint256, uint256, address[], address, uint256) -> ()
    def swapTokensForExactTokens(
        self,
        router: Address,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        def make_receipt(receipt: TxReceipt) -> RouterEventEmitterReceipt:
            return RouterEventEmitterReceipt(
                receipt, RouterEventEmitterReceiptEvents(self.contract, receipt)
            )

        router, amountOut, amountInMax, path, to, deadline = (
            unsugar(router),
            unsugar(amountOut),
            unsugar(amountInMax),
            unsugar(path),
            unsugar(to),
            unsugar(deadline),
        )
        web3_fn = self.web3_contract.functions.swapTokensForExactTokens(
            router, amountOut, amountInMax, path, to, deadline
        )
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class RouterEventEmitterCaller:
    def __init__(self, functions: RouterEventEmitterFunctions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "RouterEventEmitterCaller":
        return RouterEventEmitterCaller(
            functions=self.functions, transaction=transaction
        )

    # swapETHForExactTokens (address, uint256, address[], address, uint256) -> ()
    def swapETHForExactTokens(
        self,
        router: Address,
        amountOut: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapETHForExactTokens(
            router, amountOut, path, to, deadline
        ).call(self.transaction)

    # swapExactETHForTokens (address, uint256, address[], address, uint256) -> ()
    def swapExactETHForTokens(
        self,
        router: Address,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapExactETHForTokens(
            router, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForETH (address, uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETH(
        self,
        router: Address,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapExactTokensForETH(
            router, amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapExactTokensForTokens (address, uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokens(
        self,
        router: Address,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapExactTokensForTokens(
            router, amountIn, amountOutMin, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactETH (address, uint256, uint256, address[], address, uint256) -> ()
    def swapTokensForExactETH(
        self,
        router: Address,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapTokensForExactETH(
            router, amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)

    # swapTokensForExactTokens (address, uint256, uint256, address[], address, uint256) -> ()
    def swapTokensForExactTokens(
        self,
        router: Address,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ):
        return self.functions.swapTokensForExactTokens(
            router, amountOut, amountInMax, path, to, deadline
        ).call(self.transaction)


# ---


class RouterEventEmitter(HasAddress):
    #
    @staticmethod
    def deploy(
        w3: Web3,
    ) -> PendingDeployment["RouterEventEmitter"]:
        if w3 is None:
            raise ValueError(
                "In method RouterEventEmitter.deploy(w3, ...) w3 must not be None"
            )

        json_path = BUILD_DIR.joinpath("periphery/RouterEventEmitter.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "RouterEventEmitter":
            return RouterEventEmitter(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/RouterEventEmitter.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = RouterEventEmitterFunctions(w3, address, self.contract, self)
        self.call = RouterEventEmitterCaller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # swapETHForExactTokens (address, uint256, address[], address, uint256) -> ()
    def swapETHForExactTokens(
        self,
        router: Address,
        amountOut: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> RouterEventEmitterReceipt:
        return self.functions.swapETHForExactTokens(
            router, amountOut, path, to, deadline
        ).waitForReceipt()

    # swapExactETHForTokens (address, uint256, address[], address, uint256) -> ()
    def swapExactETHForTokens(
        self,
        router: Address,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> RouterEventEmitterReceipt:
        return self.functions.swapExactETHForTokens(
            router, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForETH (address, uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForETH(
        self,
        router: Address,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> RouterEventEmitterReceipt:
        return self.functions.swapExactTokensForETH(
            router, amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapExactTokensForTokens (address, uint256, uint256, address[], address, uint256) -> ()
    def swapExactTokensForTokens(
        self,
        router: Address,
        amountIn: int,
        amountOutMin: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> RouterEventEmitterReceipt:
        return self.functions.swapExactTokensForTokens(
            router, amountIn, amountOutMin, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactETH (address, uint256, uint256, address[], address, uint256) -> ()
    def swapTokensForExactETH(
        self,
        router: Address,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> RouterEventEmitterReceipt:
        return self.functions.swapTokensForExactETH(
            router, amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()

    # swapTokensForExactTokens (address, uint256, uint256, address[], address, uint256) -> ()
    def swapTokensForExactTokens(
        self,
        router: Address,
        amountOut: int,
        amountInMax: int,
        path: List[Address],
        to: Address,
        deadline: int,
    ) -> RouterEventEmitterReceipt:
        return self.functions.swapTokensForExactTokens(
            router, amountOut, amountInMax, path, to, deadline
        ).waitForReceipt()


# --------- end RouterEventEmitter ----------


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

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Callee.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Callee":
            return IUniswapV2Callee(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Callee.json").resolve()
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

        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Factory.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor().transact()

        def on_receipt(receipt) -> "IUniswapV2Factory":
            return IUniswapV2Factory(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/IUniswapV2Factory.json").resolve()
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
# DeflatingERC20

# ---
@dataclass
class DeflatingERC20ReceiptEvents:
    contract: "DeflatingERC20"
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
class DeflatingERC20Receipt(TransactionReceipt):
    web3_receipt: TxReceipt
    events: DeflatingERC20ReceiptEvents


# ---


class DeflatingERC20Functions:
    def __init__(
        self, w3: Web3, address: str, web3_contract: Web3, contract: "DeflatingERC20"
    ):
        self.w3 = w3
        self.address = address
        self.contract = contract
        self.web3_contract = web3_contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.DOMAIN_SEPARATOR()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> Function[Union[bytearray, str, HexBytes], DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.PERMIT_TYPEHASH()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # allowance (address, address) -> (uint256)
    def allowance(
        self, item0: Address, item1: Address
    ) -> Function[int, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        item0, item1 = unsugar(item0), unsugar(item1)
        web3_fn = self.web3_contract.functions.allowance(item0, item1)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # approve (address, uint256) -> (bool)
    def approve(
        self, spender: Address, value: int
    ) -> Function[bool, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        spender, value = unsugar(spender), unsugar(value)
        web3_fn = self.web3_contract.functions.approve(spender, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> Function[int, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        item0 = unsugar(item0)
        web3_fn = self.web3_contract.functions.balanceOf(item0)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> Function[int, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.decimals()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # name () -> (string)
    def name(
        self,
    ) -> Function[Any, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.name()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> Function[int, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
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
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
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
    ) -> Function[Any, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.symbol()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> Function[int, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        web3_fn = self.web3_contract.functions.totalSupply()
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transfer (address, uint256) -> (bool)
    def transfer(
        self, to: Address, value: int
    ) -> Function[bool, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        to, value = unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transfer(to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> Function[bool, DeflatingERC20Receipt]:
        def make_receipt(receipt: TxReceipt) -> DeflatingERC20Receipt:
            return DeflatingERC20Receipt(
                receipt, DeflatingERC20ReceiptEvents(self.contract, receipt)
            )

        from_, to, value = unsugar(from_), unsugar(to), unsugar(value)
        web3_fn = self.web3_contract.functions.transferFrom(from_, to, value)
        return Function(self.w3, web3_fn, make_receipt=make_receipt)


# ---


class DeflatingERC20Caller:
    def __init__(self, functions: DeflatingERC20Functions, transaction=None):
        self.functions = functions
        self.transaction = transaction

    def __call__(self, transaction) -> "DeflatingERC20Caller":
        return DeflatingERC20Caller(functions=self.functions, transaction=transaction)

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


class DeflatingERC20(HasAddress):
    #
    @staticmethod
    def deploy(w3: Web3, totalSupply: int) -> PendingDeployment["DeflatingERC20"]:
        if w3 is None:
            raise ValueError(
                "In method DeflatingERC20.deploy(w3, ...) w3 must not be None"
            )

        totalSupply = unsugar(totalSupply)
        json_path = BUILD_DIR.joinpath("periphery/DeflatingERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        contract = w3.eth.contract(abi=json_data["abi"], bytecode=json_data["bytecode"])
        hash = contract.constructor(totalSupply).transact()

        def on_receipt(receipt) -> "DeflatingERC20":
            return DeflatingERC20(address=receipt["contractAddress"], w3=w3)

        return PendingDeployment(w3, hash, on_receipt)

    def __init__(self, w3: Web3, address: str):
        self.address_ = address
        self.w3 = w3
        json_path = BUILD_DIR.joinpath("periphery/DeflatingERC20.json").resolve()
        json_data = json.load(json_path.open("r"))
        self.contract = w3.eth.contract(address=address, abi=json_data["abi"])
        self.functions = DeflatingERC20Functions(w3, address, self.contract, self)
        self.call = DeflatingERC20Caller(self.functions)

    @property
    def address(self):
        return self.address_

    def to_web3(self):
        return self.contract

    # DOMAIN_SEPARATOR () -> (bytes32)
    def DOMAIN_SEPARATOR(
        self,
    ) -> DeflatingERC20Receipt:
        return self.functions.DOMAIN_SEPARATOR().waitForReceipt()

    # PERMIT_TYPEHASH () -> (bytes32)
    def PERMIT_TYPEHASH(
        self,
    ) -> DeflatingERC20Receipt:
        return self.functions.PERMIT_TYPEHASH().waitForReceipt()

    # allowance (address, address) -> (uint256)
    def allowance(self, item0: Address, item1: Address) -> DeflatingERC20Receipt:
        return self.functions.allowance(item0, item1).waitForReceipt()

    # approve (address, uint256) -> (bool)
    def approve(self, spender: Address, value: int) -> DeflatingERC20Receipt:
        return self.functions.approve(spender, value).waitForReceipt()

    # balanceOf (address) -> (uint256)
    def balanceOf(self, item0: Address) -> DeflatingERC20Receipt:
        return self.functions.balanceOf(item0).waitForReceipt()

    # decimals () -> (uint8)
    def decimals(
        self,
    ) -> DeflatingERC20Receipt:
        return self.functions.decimals().waitForReceipt()

    # name () -> (string)
    def name(
        self,
    ) -> DeflatingERC20Receipt:
        return self.functions.name().waitForReceipt()

    # nonces (address) -> (uint256)
    def nonces(self, item0: Address) -> DeflatingERC20Receipt:
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
    ) -> DeflatingERC20Receipt:
        return self.functions.permit(
            owner, spender, value, deadline, v, r, s
        ).waitForReceipt()

    # symbol () -> (string)
    def symbol(
        self,
    ) -> DeflatingERC20Receipt:
        return self.functions.symbol().waitForReceipt()

    # totalSupply () -> (uint256)
    def totalSupply(
        self,
    ) -> DeflatingERC20Receipt:
        return self.functions.totalSupply().waitForReceipt()

    # transfer (address, uint256) -> (bool)
    def transfer(self, to: Address, value: int) -> DeflatingERC20Receipt:
        return self.functions.transfer(to, value).waitForReceipt()

    # transferFrom (address, address, uint256) -> (bool)
    def transferFrom(
        self, from_: Address, to: Address, value: int
    ) -> DeflatingERC20Receipt:
        return self.functions.transferFrom(from_, to, value).waitForReceipt()


# --------- end DeflatingERC20 ----------
