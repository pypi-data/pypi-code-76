from typing import Type

from mypy.types import NoneType
from mypy_extensions import TypedDict

from pymoneroasync.models.daemon.inputs import (
    GetBlockHeaderBaseIn,
    GetBlockHeaderByHashIn,
    GetBlockHeaderByHeightIn,
    GetBlockHeadersIn,
    GetBlockIn,
    GetBlockTemplateIn,
    GetCoinbaseTxSumIn,
    GetFeeEstimateIn,
    GetOutputDistributionIn,
    GetOutputHistogramIn,
    GetOutsIn,
    GetTransactionsIn,
    InPeersIn,
    IsKeyImageSpentIn,
    LimitIn,
    OnGetBlockHashIn,
    OutPeersIn,
    SendRawTxIn,
    SetBansIn,
    SetLogCategoriesIn,
    SetLogHashRateIn,
    SetLogLevelIn,
    StartMiningIn,
    SubmitBlockIn,
    TxIn,
    UpdateIn,
)
from pymoneroasync.models.daemon.outputs import (
    AccessResponseBase,
    GetAltBlockHashes,
    GetAlternateChains,
    GetBans,
    GetBlock,
    GetBlockCount,
    GetBlockHeader,
    GetBlockHeaders,
    GetBlockTemplate,
    GetCoinbaseTxSum,
    GetConnections,
    GetFeeEstimate,
    GetHeight,
    GetInfo,
    GetOutputDistribution,
    GetOutputHistogram,
    GetOuts,
    GetPeerList,
    GetTransactions,
    GetTransationPool,
    GetTransationPoolStats,
    GetTxPoolBacklog,
    GetVersion,
    HardForkInfo,
    InPeers,
    IsKeyImageSpent,
    Limit,
    MiningStatus,
    OnGetBlockHash,
    OutPeers,
    ResponseBase,
    SendRawTx,
    SetLogCategories,
    SyncInfo,
    Update,
)

# https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#json-rpc-methods


class DaemonJsonRPCInDict(TypedDict):
    get_block_count: Type[NoneType]
    on_get_block_hash: Type[OnGetBlockHashIn]
    get_block_template: Type[GetBlockTemplateIn]
    submit_block: Type[SubmitBlockIn]
    get_last_block_header: Type[GetBlockHeaderBaseIn]
    get_block_header_by_hash: Type[GetBlockHeaderByHashIn]
    get_block_header_by_height: Type[GetBlockHeaderByHeightIn]
    get_block_headers_range: Type[GetBlockHeadersIn]
    get_block: Type[GetBlockIn]
    get_connections: Type[NoneType]
    get_info: Type[NoneType]
    hard_fork_info: Type[NoneType]
    set_bans: Type[SetBansIn]
    get_bans: Type[NoneType]
    flush_txpool: Type[TxIn]
    get_output_histogram: Type[GetOutputHistogramIn]
    get_coinbase_tx_sum: Type[GetCoinbaseTxSumIn]
    get_version: Type[NoneType]
    get_fee_estimate: Type[GetFeeEstimateIn]
    get_alternate_chains: Type[NoneType]
    relay_tx: Type[TxIn]
    sync_info: Type[NoneType]
    get_txpool_backlog: Type[NoneType]
    get_output_distribution: Type[GetOutputDistributionIn]


DAEMON_JSON_RPC_METHODS_INPUTS = DaemonJsonRPCInDict(
    get_block_count=NoneType,
    on_get_block_hash=OnGetBlockHashIn,
    get_block_template=GetBlockTemplateIn,
    submit_block=SubmitBlockIn,
    get_last_block_header=GetBlockHeaderBaseIn,
    get_block_header_by_hash=GetBlockHeaderByHashIn,
    get_block_header_by_height=GetBlockHeaderByHeightIn,
    get_block_headers_range=GetBlockHeadersIn,
    get_block=GetBlockIn,
    get_connections=NoneType,
    get_info=NoneType,
    hard_fork_info=NoneType,
    set_bans=SetBansIn,
    get_bans=NoneType,
    flush_txpool=TxIn,
    get_output_histogram=GetOutputHistogramIn,
    get_coinbase_tx_sum=GetCoinbaseTxSumIn,
    get_version=NoneType,
    get_fee_estimate=GetFeeEstimateIn,
    get_alternate_chains=NoneType,
    relay_tx=TxIn,
    sync_info=NoneType,
    get_txpool_backlog=NoneType,
    get_output_distribution=GetOutputDistributionIn,
)


class DaemonJsonRPCOutDict(TypedDict):
    get_block_count: Type[GetBlockCount]
    on_get_block_hash: Type[OnGetBlockHash]
    get_block_template: Type[GetBlockTemplate]
    submit_block: Type[ResponseBase]
    get_last_block_header: Type[GetBlockHeader]
    get_block_header_by_hash: Type[GetBlockHeader]
    get_block_header_by_height: Type[GetBlockHeader]
    get_block_headers_range: Type[GetBlockHeaders]
    get_block: Type[GetBlock]
    get_connections: Type[GetConnections]
    get_info: Type[GetInfo]
    hard_fork_info: Type[HardForkInfo]
    set_bans: Type[ResponseBase]
    get_bans: Type[GetBans]
    flush_txpool: Type[ResponseBase]
    get_output_histogram: Type[GetOutputHistogram]
    get_coinbase_tx_sum: Type[GetCoinbaseTxSum]
    get_version: Type[GetVersion]
    get_fee_estimate: Type[GetFeeEstimate]
    get_alternate_chains: Type[GetAlternateChains]
    relay_tx: Type[AccessResponseBase]
    sync_info: Type[SyncInfo]
    get_txpool_backlog: Type[GetTxPoolBacklog]
    get_output_distribution: Type[GetOutputDistribution]


DAEMON_JSON_RPC_METHODS_OUTPUTS = DaemonJsonRPCOutDict(
    get_block_count=GetBlockCount,
    on_get_block_hash=OnGetBlockHash,
    get_block_template=GetBlockTemplate,
    submit_block=ResponseBase,
    get_last_block_header=GetBlockHeader,
    get_block_header_by_hash=GetBlockHeader,
    get_block_header_by_height=GetBlockHeader,
    get_block_headers_range=GetBlockHeaders,
    get_block=GetBlock,
    get_connections=GetConnections,
    get_info=GetInfo,
    hard_fork_info=HardForkInfo,
    set_bans=ResponseBase,
    get_bans=GetBans,
    flush_txpool=ResponseBase,
    get_output_histogram=GetOutputHistogram,
    get_coinbase_tx_sum=GetCoinbaseTxSum,
    get_version=GetVersion,
    get_fee_estimate=GetFeeEstimate,
    get_alternate_chains=GetAlternateChains,
    relay_tx=AccessResponseBase,
    sync_info=SyncInfo,
    get_txpool_backlog=GetTxPoolBacklog,
    get_output_distribution=GetOutputDistribution,
)


# https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#other-daemon-rpc-calls


class DaemonOtherRPCInDict(TypedDict):
    get_height: Type[NoneType]
    # get_blocks_bin: Type[GetBlocksBinIn]
    get_transactions: Type[GetTransactionsIn]
    get_alt_blocks_hashes: Type[NoneType]
    is_key_image_spent: Type[IsKeyImageSpentIn]
    send_raw_transaction: Type[SendRawTxIn]
    start_mining: Type[StartMiningIn]
    stop_mining: Type[NoneType]
    mining_status: Type[NoneType]
    save_bc: Type[NoneType]
    get_peer_list: Type[NoneType]
    set_log_hash_rate: Type[SetLogHashRateIn]
    set_log_level: Type[SetLogLevelIn]
    set_log_categories: Type[SetLogCategoriesIn]
    get_transaction_pool: Type[NoneType]
    get_transaction_pool_stats: Type[NoneType]
    stop_daemon: Type[NoneType]
    set_limit: Type[LimitIn]
    get_limit: Type[NoneType]
    out_peers: Type[OutPeersIn]
    in_peers: Type[InPeersIn]
    get_outs: Type[GetOutsIn]
    update: Type[UpdateIn]


DAEMON_OTHER_RPC_METHODS_INPUTS = DaemonOtherRPCInDict(
    get_height=NoneType,
    # get_blocks_bin=GetBlocksBinIn,
    get_transactions=GetTransactionsIn,
    get_alt_blocks_hashes=NoneType,
    is_key_image_spent=IsKeyImageSpentIn,
    send_raw_transaction=SendRawTxIn,
    start_mining=StartMiningIn,
    stop_mining=NoneType,
    mining_status=NoneType,
    save_bc=NoneType,
    get_peer_list=NoneType,
    set_log_hash_rate=SetLogHashRateIn,
    set_log_level=SetLogLevelIn,
    set_log_categories=SetLogCategoriesIn,
    get_transaction_pool=NoneType,
    get_transaction_pool_stats=NoneType,
    stop_daemon=NoneType,
    set_limit=LimitIn,
    get_limit=NoneType,
    out_peers=OutPeersIn,
    in_peers=InPeersIn,
    get_outs=GetOutsIn,
    update=UpdateIn,
)


class DaemonOtherRPCOutDict(TypedDict):
    get_height: Type[GetHeight]
    # get_blocks_bin: Type[GetBlocksBin]
    get_transactions: Type[GetTransactions]
    get_alt_blocks_hashes: Type[GetAltBlockHashes]
    is_key_image_spent: Type[IsKeyImageSpent]
    send_raw_transaction: Type[SendRawTx]
    start_mining: Type[ResponseBase]
    stop_mining: Type[ResponseBase]
    mining_status: Type[MiningStatus]
    save_bc: Type[ResponseBase]
    get_peer_list: Type[GetPeerList]
    set_log_hash_rate: Type[ResponseBase]
    set_log_level: Type[ResponseBase]
    set_log_categories: Type[SetLogCategories]
    get_transaction_pool: Type[GetTransationPool]
    get_transaction_pool_stats: Type[GetTransationPoolStats]
    stop_daemon: Type[ResponseBase]
    set_limit: Type[Limit]
    get_limit: Type[Limit]
    out_peers: Type[OutPeers]
    in_peers: Type[InPeers]
    get_outs: Type[GetOuts]
    update: Type[Update]


DAEMON_OTHER_RPC_METHODS_OUTPUTS = DaemonOtherRPCOutDict(
    get_height=GetHeight,
    # get_blocks_bin=GetBlocksBin,
    get_transactions=GetTransactions,
    get_alt_blocks_hashes=GetAltBlockHashes,
    is_key_image_spent=IsKeyImageSpent,
    send_raw_transaction=SendRawTx,
    start_mining=ResponseBase,
    stop_mining=ResponseBase,
    mining_status=MiningStatus,
    save_bc=ResponseBase,
    get_peer_list=GetPeerList,
    set_log_hash_rate=ResponseBase,
    set_log_level=ResponseBase,
    set_log_categories=SetLogCategories,
    get_transaction_pool=GetTransationPool,
    get_transaction_pool_stats=GetTransationPoolStats,
    stop_daemon=ResponseBase,
    set_limit=Limit,
    get_limit=Limit,
    out_peers=OutPeers,
    in_peers=InPeers,
    get_outs=GetOuts,
    update=Update,
)

#: Default mainnet p2p port
MAINNET_P2P_PORT = 18080
#: Default mainnet rpc port
MAINNET_RPC_PORT = 18081
#: Default mainnet zmq port
MAINNET_ZMQ_PORT = 18082

#: Default stagenet p2p port
STAGENET_P2P_PORT = 38080
#: Default stagenet rpc port
STAGENET_RPC_PORT = 38081
#: Default stagenet zmq port
STAGENET_ZMQ_PORT = 38082

#: Default testnet p2p port
TESTNET_P2P_PORT = 28080
#: Default testnet rpc port
TESTNET_RPC_PORT = 28081
#: Default testnet zmq port
TESTNET_ZMQ_PORT = 28082

W_TESTNET_RPC_PORT = 29081

#: Log categories
DAEMON_LOG_CATEGORIES = [
    "*",
    "default",
    "net",
    "net.http",
    "net.p2p",
    "logging",
    "net.throttle",
    "blockchain.db",
    "blockchain.db.lmdb",
    "bcutil",
    "checkpoints",
    "net.dns",
    "net.dl",
    "i18n",
    "perf",
    "stacktrace",
    "updates",
    "account",
    "cn",
    "difficulty",
    "hardfork",
    "miner",
    "blockchain",
    "txpool",
    "cn.block_queue",
    "net.cn",
    "daemon",
    "debugtools.deserialize",
    "debugtools.objectsizes",
    "device.ledger",
    "wallet.gen_multisig",
    "multisig",
    "bulletproofs",
    "ringct",
    "daemon.rpc",
    "wallet.simplewallet",
    "WalletAPI",
    "wallet.ringdb",
    "wallet.wallet2",
    "wallet.rpc",
    "tests.core",
]

#: Log level
DAEMON_LOG_LEVELS = ["FATAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE"]

#: Default daemon log level
DAEMON_DEFAULT_LOG = "*:WARNING,net:FATAL,net.p2p:FATAL,net.cn:FATAL,global:INFO,verify:FATAL,stacktrace:INFO,logging:INFO,msgwriter:INFO"  # noqa: E501
#: Default daemon rcp log
DAEMON_DEFAULT_LOG_RPC = "*:WARNING,net:FATAL,net.p2p:FATAL,net.cn:FATAL,global:INFO,verify:FATAL,stacktrace:INFO,logging:INFO,msgwriter:INFO,daemon.rpc:DEBUG"  # noqa: E501
