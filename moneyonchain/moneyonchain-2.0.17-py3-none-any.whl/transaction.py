"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import logging
import requests
from hexbytes import HexBytes

from brownie.network.transaction import TransactionReceipt as _TransactionReceipt
from brownie._config import CONFIG
from brownie.exceptions import RPCRequestError
from brownie.network.web3 import web3


class TransactionReceipt(_TransactionReceipt):

    log = logging.getLogger()

    def __init__(self,
                 *args,
                 logger=None,
                 trace_enabled=False,
                 **parameters):

        if logger:
            self.log = logger

        self.trace_enabled = trace_enabled

        super().__init__(*args, **parameters)

    def info_to_log(self) -> None:
        """Displays verbose information about the transaction, including decoded event logs."""
        status = ""
        if not self.status:
            status = f"({self.revert_msg or 'reverted'})"

        result = (
            f"Transaction was Mined {status}\n---------------------\n"
            f"Tx Hash: {self.txid}\n"
            f"From: {self.sender}\n"
        )

        if self.contract_address and self.status:
            result += (
                f"New {self.contract_name} address: {self.contract_address}\n"
            )
        else:
            result += (
                f"To: {self.receiver}\n"
                f"Value: {self.value}\n"
            )
            if self.input != "0x" and int(self.input, 16):
                result += f"Function: {self._full_name()}\n"

        result += (
            f"Block: {self.block_number}\nGas Used: "
            f"{self.gas_used} / {self.gas_limit}"
            f"({self.gas_used / self.gas_limit:.1%})\n"
        )

        if self.events:
            result += "\n   Events In This Transaction\n   --------------------------"
            for event in self.events:  # type: ignore
                result += f"\n   {event.name}"  # type: ignore
                for key, value in event.items():  # type: ignore
                    result += f"\n      {key}: {value}"

        self.log.info(result)

    def _get_trace(self) -> None:
        """Retrieves the stack trace via debug_traceTransaction and finds the
        return value, revert message and event logs in the trace.
        """

        # check if trace has already been retrieved, or the tx warrants it
        if self._raw_trace is not None:
            return
        self._raw_trace = []
        if self.input == "0x" and self.gas_used == 21000:
            self._modified_state = False
            self._trace = []
            return

        if not self.trace_enabled:
            raise RPCRequestError("Node client does not support `debug_traceTransaction`")
        try:
            trace = web3.provider.make_request(  # type: ignore
                "debug_traceTransaction", [self.txid]
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            msg = f"Encountered a {type(e).__name__} while requesting "
            msg += "`debug_traceTransaction`. The local RPC client has likely crashed."
            if CONFIG.argv["coverage"]:
                msg += " If the error persists, add the `skip_coverage` marker to this test."
            raise RPCRequestError(msg) from None

        if "error" in trace:
            self._modified_state = None
            self._trace_exc = RPCRequestError(trace["error"]["message"])
            raise self._trace_exc

        self._raw_trace = trace = trace["result"]["structLogs"]
        if not trace:
            self._modified_state = False
            return

        if isinstance(trace[0]["gas"], str):
            # handle traces where numeric values are returned as hex (Nethermind)
            for step in trace:
                step["gas"] = int(step["gas"], 16)
                step["gasCost"] = int.from_bytes(HexBytes(step["gasCost"]), "big", signed=True)
                step["pc"] = int(step["pc"], 16)

        if self.status:
            self._confirmed_trace(trace)
        else:
            self._reverted_trace(trace)


def receipt_to_log(receipt, log):
    """ Receipt to logging """

    status = ""
    if not receipt.status:
        status = ""

    result = (
        f"Transaction was Mined {status}\n---------------------\n"
        f"Tx Hash: {receipt.txid}\n"
        f"From: {receipt.sender}\n"
    )

    if receipt.contract_address and receipt.status:
        result += (
            f"New {receipt.contract_name} address: {receipt.contract_address}\n"
        )
    else:
        result += (
            f"To: {receipt.receiver}\n"
            f"Value: {receipt.value}\n"
        )
        if receipt.input != "0x" and int(receipt.input, 16):
            result += f"Function: {receipt._full_name()}\n"

    result += (
        f"Block: {receipt.block_number}\nGas Used: "
        f"{receipt.gas_used} / {receipt.gas_limit}"
        f"({receipt.gas_used / receipt.gas_limit:.1%})\n"
    )

    if receipt.events:
        result += "\n   Events In This Transaction\n   --------------------------"
        for event in receipt.events:  # type: ignore
            result += f"\n   {event.name}"  # type: ignore
            for key, value in event.items():  # type: ignore
                result += f"\n      {key}: {value}"

    log.info(result)
