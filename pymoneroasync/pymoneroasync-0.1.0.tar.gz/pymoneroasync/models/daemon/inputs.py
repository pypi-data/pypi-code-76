from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from pymoneroasync.models.daemon.outputs import Ban


class OnGetBlockHashIn(BaseModel):
    """
    - block height (int array of length 1)
    """

    __root__: List[int] = Field(..., min_items=1, max_items=1)


class GetBlockTemplateIn(BaseModel):
    """
    - wallet_address - Address of wallet to receive coinbase transactions if block is successfully mined.
    - reserve_size - Reserve size.
    """

    reserve_size: int
    wallet_address: str
    prev_block: Optional[str]
    extra_nonce: Optional[str]


class SubmitBlockIn(BaseModel):
    """
    - Block blob data - list of block blobs which have been mined.

    See :meth:`pymoneroasync._abc.AsyncDaemon.get_block_template` to get a blob on which to mine.
    """

    __root__: List[str]


class GetBlockHeaderBaseIn(BaseModel):
    """
    - fill_pow_hash - default False
    """

    fill_pow_hash: Optional[bool] = False


class GetBlockHeaderByHashIn(GetBlockHeaderBaseIn):
    """
    - hash - The block's sha256 hash.
    """

    hash: Optional[str]
    hashes: Optional[List[str]]


class GetBlockHeaderByHeightIn(GetBlockHeaderBaseIn):
    """
    - height - The block's height.
    """

    height: int


class GetBlockHeadersIn(GetBlockHeaderBaseIn):
    """
    - start_height - The starting block's height.
    - end_height - The ending block's height.
    """

    start_height: int
    end_height: int


class GetBlockIn(GetBlockHeaderBaseIn):
    """
    - height - The block's height.
    - hash - The block's hash.
    """

    hash: Optional[str]
    height: Optional[int]


class BanIn(Ban):
    """
    - ban - set it to True to ban the opposite to unban
    """

    ban: bool


class SetBansIn(BaseModel):
    """
    - bans - A list of nodes to ban

    see :class:`pymoneroasync.models.daemon.outputs.Ban`
    """

    bans: List[BanIn]


class TxIn(BaseModel):
    """
    - txids - array of strings, list of transactions IDs to flush from pool (all tx ids flushed if empty).
    """

    txids: List[str]


class GetOutputHistogramIn(BaseModel):
    amounts: List[int]
    min_count: Optional[int]
    max_count: Optional[int]
    unlocked: Optional[bool]
    recent_cutoff: Optional[int]


class GetCoinbaseTxSumIn(BaseModel):
    """
    - height - Block height from which getting the amounts
    - count - number of blocks to include in the sum
    """

    height: int
    count: int


class GetFeeEstimateIn(BaseModel):
    grace_blocks: Optional[int]


class GetOutputDistributionIn(BaseModel):
    amounts: List[int]
    from_height: Optional[int]
    to_height: Optional[int]
    cumulative: Optional[bool]
    binary: Optional[bool]
    compress: Optional[bool]


DaemonJsonRPCIn = Union[
    OnGetBlockHashIn,
    GetBlockTemplateIn,
    SubmitBlockIn,
    GetBlockHeaderBaseIn,
    GetBlockHeaderByHashIn,
    GetBlockHeaderByHeightIn,
    GetBlockHeadersIn,
    GetBlockIn,
    SetBansIn,
    TxIn,
    GetOutputHistogramIn,
    GetCoinbaseTxSumIn,
    GetFeeEstimateIn,
    GetOutputDistributionIn,
]


# class GetBlocksBinIn(BaseModel):
#     block_ids: List[bytes]
#     # *first 10 blocks id goes sequential,
#     # next goes in pow(2,n) offset, like 2, 4, 8, 16, 32, 64 and so on,
#     # and the last one is always genesis block
#     start_height: int
#     prune: bool
#     no_miner_tx: Optional[bool]


class GetTransactionsIn(BaseModel):
    """
    - txs_hashes - List of transaction hashes to look up.
    - decode_as_json - If set true, the returned transaction information will be decoded rather than binary.
    - prune - Optional (false by default).
    """

    txs_hashes: List[str]
    decode_as_json: Optional[bool] = False
    prune: Optional[bool] = False
    split: Optional[bool]


class IsKeyImageSpentIn(BaseModel):
    key_images: List[str]


class SendRawTxIn(BaseModel):
    """
    - tx_as_hex - Full transaction information as hexidecimal string.
    - do_not_relay - Stop relaying transaction to other nodes (default is false).
    """

    tx_as_hex: str
    do_not_relay: Optional[bool] = False
    do_sanity_checks: Optional[bool] = True


class StartMiningIn(BaseModel):
    """
    - do_background_mining - States if the mining should run in background (true) or foreground (false).
    - ignore_battery - States if batery state (on laptop) should be ignored (true) or not (false).
    - miner_address - Account address to mine to.
    - threads_count - Number of mining thread to run.
    """

    miner_address: str
    threads_count: int
    do_background_mining: bool
    ignore_battery: bool


class SetLogHashRateIn(BaseModel):
    """
    - visible - States if hash rate logs should be visible (true) or hidden (false)
    """

    visible: bool


class SetLogLevelIn(BaseModel):
    """
    - level - daemon log level to set from 0 (less verbose) to 4 (most verbose)
    """

    level: int


class SetLogCategoriesIn(BaseModel):
    """
    - categories: list of categories
    """

    categories: str


class LimitIn(BaseModel):
    """
    - limit_down - Download limit in kBytes per second (-1 reset to default, 0 don't change the current limit)
    - limit_up - Upload limit in kBytes per second (-1 reset to default, 0 don't change the current limit)
    """

    limit_up: int
    limit_down: int


class OutPeersIn(BaseModel):
    """
    - out_peers - Max number of outgoing peers
    """

    set: Optional[bool] = True
    out_peers: int


class InPeersIn(BaseModel):
    """
    - in_peers - Max number of incoming peers
    """

    in_peers: int


class GetOutputOuts(BaseModel):
    amount: int
    index: int


class GetOutsIn(BaseModel):
    """
    - outputs array of GetOutputOuts, see :class:`pymoneroasync.models.daemon.inputs.GetOutputOuts`
    - get_txid - If true, a txid will included for each output in the response.
    """

    outputs: List[GetOutputOuts]
    get_txid: bool


class UpdateCommand(str, Enum):
    check = "check"
    download = "download"


class UpdateIn(BaseModel):
    """
    - command - command to use, either check or download
    - path - Optional, path where to download the update.
    """

    command: UpdateCommand
    path: Optional[str]


DaemonOtherRPCIn = Union[
    GetTransactionsIn,
    IsKeyImageSpentIn,
    SendRawTxIn,
    StartMiningIn,
    SetLogHashRateIn,
    SetLogLevelIn,
    SetLogCategoriesIn,
    LimitIn,
    OutPeersIn,
    InPeersIn,
    GetOutsIn,
    UpdateIn,
]
