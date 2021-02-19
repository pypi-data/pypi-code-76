from datetime import datetime
from enum import Enum, IntEnum
from ipaddress import IPv4Address, IPv6Address
from typing import List, Optional, Union

from pydantic import BaseModel


class StatusBase(str, Enum):
    OK = "OK"
    BUSY = "BUSY"
    NOT_MINING = "NOT MINING"
    PAYMENT_REQUIRED = "PAYMENT REQUIRED"
    FAILED = "Failed"


class ResponseBase(BaseModel):
    """
    Base RPC response.

    - status - General RPC error code. "OK" means everything looks good.
    - untrusted - States if the result is obtained using the bootstrap mode, and is therefore not trusted (true), or when the daemon is fully synced (false).
    """

    status: StatusBase
    untrusted: bool


class AccessResponseBase(ResponseBase):
    """
    Access base RPC response.
    """

    credits: int
    top_hash: str


class GetBlockCount(ResponseBase):
    """
    Number of blocks in longest chain seen by the node.
    """

    count: int


class OnGetBlockHash(BaseModel):
    """
    Block hash
    """

    __root__: str


class GetBlockTemplate(ResponseBase):
    """
    Get a block template on which mining a new block.

    - blocktemplate_blob - Blob on which to try to mine a new block.
    - blockhashing_blob - Blob on which to try to find a valid nonce.
    - difficulty - Difficulty of next block.
    - expected_reward - Coinbase reward expected to be received if block is successfully mined.
    - height - Height on which to mine.
    - prev_hash - Hash of the most recent block on which to mine the next block.
    - reserved_offset - Reserved offset.
    """

    difficulty: int
    wide_difficulty: str
    difficulty_top64: int
    height: int
    reserved_offset: int
    expected_reward: int
    prev_hash: str
    seed_height: int
    seed_hash: str
    next_seed_hash: str
    blocktemplate_blob: str
    blockhashing_blob: str


class BlockHeader(BaseModel):
    """
    Block header information for the most recent block.

    - block_header - A structure containing block header information.
    - block_size - The block size in bytes.
    - depth - The number of blocks succeeding this block on the blockchain. A larger number means an older block.
    - difficulty - The strength of the Monero network based on mining power.
    - hash - The hash of this block.
    - height - The number of blocks preceding this block on the blockchain.
    - major_version - The major version of the monero protocol at this block height.
    - minor_version - The minor version of the monero protocol at this block height.
    - nonce - a cryptographic random one-time number used in mining a Monero block.
    - num_txes - Number of transactions in the block, not counting the coinbase tx.
    - orphan_status - Usually false. If true, this block is not part of the longest chain.
    - prev_hash - The hash of the block immediately preceding this block in the chain.
    - reward - The amount of new atomic units generated in this block and rewarded to the miner. Note: 1 XMR = 1e12 atomic units.
    - timestamp - The unix time at which the block was recorded into the blockchain.
    """

    major_version: int
    minor_version: int
    timestamp: datetime
    prev_hash: str
    nonce: int
    orphan_status: bool
    height: int
    depth: int
    hash: str
    difficulty: int
    wide_difficulty: str
    difficulty_top64: int
    cumulative_difficulty: int
    wide_cumulative_difficulty: str
    cumulative_difficulty_top64: int
    reward: int
    block_size: int
    block_weight: Optional[int]
    num_txes: int
    pow_hash: str
    long_term_weight: Optional[int]
    miner_tx_hash: str


class GetBlockHeader(AccessResponseBase):
    """
    Block header information, can be retrieved using either a block's hash or height.

    - block_header - A structure containing block header information. See :meth:`pymoneroasync._abc.AsyncDaemon.get_last_block_header`.
    """

    block_header: BlockHeader


class GetBlockHeaders(AccessResponseBase):
    """
    Block headers information for a range of blocks.

    - headers - array of block_header.

    See :meth:`pymoneroasync._abc.AsyncDaemon.get_last_block_header`.
    """

    headers: List[BlockHeader]


class GetBlock(AccessResponseBase):
    """
    Full block information

    - blob - Hexadecimal blob of block information.
    - block_header - A structure containing block header information. See :meth:`pymoneroasync._abc.AsyncDaemon.get_last_block_header`.
    - json - JSON formatted block details:
        - major_version - Same as in block header.
        - minor_version - Same as in block header.
        - timestamp - Same as in block header.
        - prev_id - Same as prev_hash in block header.
        - nonce - Same as in block header.
        - miner_tx - Miner transaction information
            - version - Transaction version number.
            - unlock_time - The block height when the coinbase transaction becomes spendable.
            - vin - List of transaction inputs:
                - gen - Miner txs are coinbase txs, or "gen".
                    - height - This block height, a.k.a. when the coinbase is generated.
            - vout - List of transaction outputs. Each output contains:
                - amount - The amount of the output, in atomic units.
                - target -
                    - key -
            - extra - Usually called the "transaction ID" but can be used to include any random 32 byte/64 character hex string.
            - signatures - Contain signatures of tx signers. Coinbased txs do not have signatures.
        - tx_hashes - List of hashes of non-coinbase transactions in the block. If there are no other transactions, this will be an empty list.
    """

    block_header: BlockHeader
    miner_tx_hash: str
    tx_hashes: Optional[List[str]]
    blob: str
    json_: str

    class Config:
        fields = {"json_": "json"}


class Connection(BaseModel):
    """
    Represents a connection

    - address - The peer's address, actually IPv4 & port
    - avg_download - Average bytes of data downloaded by node.
    - avg_upload - Average bytes of data uploaded by node.
    - connection_id - The connection ID
    - current_download - Current bytes downloaded by node.
    - current_upload - Current bytes uploaded by node.
    - height- The peer height
    - host - The peer host
    - incoming - Is the node getting information from your node?
    - ip - The node's IP address.
    - live_time -
    - local_ip - is it a local ip
    - localhost - is is localhost
    - peer_id - The node's ID on the network.
    - port - The port that the node is using to connect to the network.
    - recv_count -
    - recv_idle_time -
    - send_count -
    - send_idle_time -
    - state -
    - support_flags -
    """

    address: str
    address_type: int
    avg_download: int
    avg_upload: int
    connection_id: str
    current_download: int
    current_upload: int
    height: int
    host: str
    incoming: bool
    ip: str
    live_time: int
    local_ip: bool
    localhost: bool
    peer_id: str
    port: str
    pruning_seed: int
    recv_count: int
    recv_idle_time: int
    rpc_credits_per_hash: int
    rpc_port: int
    send_count: int
    send_idle_time: int
    state: str
    support_flags: int


class GetConnections(ResponseBase):
    """
    Retrieve information about incoming and outgoing connections to your node.

    connections - List of all connections and their info, see :class:`pymoneroasync.models.daemon.outputs.Connection`
    """

    connections: List[Connection]


class GetInfo(AccessResponseBase):
    """
    Retrieve general information about the state of your node and the network.

    - alt_blocks_count - Number of alternative blocks to main chain.
    - block_size_limit - Maximum allowed block size
    - block_size_median - Median block size of latest 100 blocks
    - bootstrap_daemon_address - bootstrap node to give immediate usability to wallets while syncing by proxying RPC to it. (Note: the replies may be untrustworthy).
    - busy_syncing - States if new blocks are being added (true) or not (false).
    - cumulative_difficulty - Cumulative difficulty of all blocks in the blockchain.
    - difficulty - Network difficulty (analogous to the strength of the network)
    - free_space - Available disk space on the node.
    - grey_peerlist_size - Grey Peerlist Size
    - height - Current length of longest chain known to daemon.
    - height_without_bootstrap - Current length of the local chain of the daemon.
    - incoming_connections_count - Number of peers connected to and pulling from your node.
    - mainnet - States if the node is on the mainnet (true) or not (false).
    - offline - States if the node is offline (true) or online (false).
    - outgoing_connections_count - Number of peers that you are connected to and getting information from.
    - rpc_connections_count - Number of RPC client connected to the daemon (Including this RPC request).
    - stagenet - States if the node is on the stagenet (true) or not (false).
    - start_time - Start time of the daemon, as UNIX time.
    - synchronized - States if the node is synchronized (true) or not (false).
    - target - Current target for next proof of work.
    - target_height - The height of the next block in the chain.
    - testnet - States if the node is on the testnet (true) or not (false).
    - top_block_hash - Hash of the highest block in the chain.
    - tx_count - Total number of non-coinbase transaction in the chain.
    - tx_pool_size - Number of transactions that have been broadcast but not included in a block.
    - was_bootstrap_ever_used - States if a bootstrap node has ever been used since the daemon started.
    - white_peerlist_size - White Peerlist Size
    """

    height: int
    target_height: int
    difficulty: int
    wide_difficulty: str
    difficulty_top64: int
    target: int
    tx_count: int
    tx_pool_size: int
    alt_blocks_count: int
    outgoing_connections_count: int
    incoming_connections_count: int
    rpc_connections_count: int
    white_peerlist_size: int
    grey_peerlist_size: int
    mainnet: bool
    testnet: bool
    stagenet: bool
    nettype: str
    top_block_hash: str
    cumulative_difficulty: int
    wide_cumulative_difficulty: str
    cumulative_difficulty_top64: int
    block_size_limit: int
    block_weight_limit: int
    block_size_median: int
    block_weight_median: int
    adjusted_time: int
    start_time: int
    free_space: int
    offline: bool
    bootstrap_daemon_address: str
    height_without_bootstrap: int
    was_bootstrap_ever_used: bool
    database_size: int
    update_available: bool
    busy_syncing: bool
    version: str
    synchronized: bool


class HardForkInfo(AccessResponseBase):
    """
    Look up information regarding hard fork voting and readiness.

    - earliest_height - Block height at which hard fork would be enabled if voted in.
    - enabled - Tells if hard fork is enforced.
    - state - Current hard fork state: 0 (There is likely a hard fork), 1 (An update is needed to fork properly), or 2 (Everything looks good).
    - status - General RPC error code. "OK" means everything looks good.
    - threshold - Minimum percent of votes to trigger hard fork. Default is 80.
    - version - The major block version for the fork.
    - votes - Number of votes towards hard fork.
    - voting - Hard fork voting status.
    - window - Number of blocks over which current votes are cast. Default is 10080 blocks.
    """

    version: int
    enabled: bool
    window: int
    votes: int
    threshold: int
    voting: int
    state: int
    earliest_height: int


class Ban(BaseModel):
    """
    - host - Host to ban (IP in A.B.C.D form - will support I2P address in the future).
    - ip - IP address to ban, in Int format.
    - seconds - Number of seconds to ban node.
    """

    host: Optional[str]
    ip: Optional[int]
    seconds: int


class GetBans(ResponseBase):
    """
    Get list of banned IPs.

    - bans - List of banned nodes
    """

    bans: Optional[List[Ban]]


class HistogramEntry(BaseModel):
    amount: int
    total_instances: int
    unlocked_instances: int
    recent_instances: int


class GetOutputHistogram(AccessResponseBase):
    """
    Get a histogram of output amounts. For all amounts (possibly filtered by parameters), gives the number of outputs on the chain for that amount. RingCT outputs counts as 0 amount.

    - histogram - list of histogram entries, see :class:`pymoneroasync.models.daemon.outputs.HistogramEntry`
    """

    histogram: List[HistogramEntry]


class GetCoinbaseTxSum(AccessResponseBase):
    """
    Get the coinbase amount and the fees amount for n last blocks starting at particular height
    """

    emission_amount: int
    wide_emission_amount: str
    emission_amount_top64: int
    fee_amount: int
    wide_fee_amount: str
    fee_amount_top64: int


class GetVersion(ResponseBase):
    """
    Give the node current version
    """

    version: int
    release: bool


class GetFeeEstimate(AccessResponseBase):
    """
    Gives an estimation on fees per byte.

    - fee - Amount of fees estimated per byte in atomic units
    - quantization_mask - Final fee should be rounded up to an even multiple of this value
    """

    fee: int
    quantization_mask: int


class Chain(BaseModel):
    """
    - block_hash - the block hash of the first diverging block of this alternative chain.
    - difficulty - the cumulative difficulty of all blocks in the alternative chain.
    - height - the block height of the first diverging block of this alternative chain.
    - length - the length in blocks of this alternative chain, after divergence.
    """

    block_hash: str
    height: int
    length: int
    difficulty: int
    wide_difficulty: str
    difficulty_top64: int
    block_hashes: List[str]
    main_chain_parent_block: str


class GetAlternateChains(ResponseBase):
    """
    Display alternative chains seen by the node.

    - chains: array of chains, see :class:`pymoneroasync.models.daemon.outputs.Chain`
    """

    chains: Optional[List[Chain]]


class Peer(BaseModel):
    """
    - info - structure of connection info, as defined in get_connections, see :class:`pymoneroasync.models.daemon.outputs.Connection`
    """

    info: Connection


class Span(BaseModel):
    """
    - connection_id - Id of connection
    - nblocks - number of blocks in that span
    - rate - connection rate
    - remote_address - peer address the node is downloading (or has downloaded) than span from
    - size - total number of bytes in that span's blocks (including txes)
    - speed - connection speed
    - start_block_height - block height of the first block in that span
    """

    start_block_height: int
    nblocks: int
    connection_id: str
    rate: int
    speed: int
    size: int
    remote_address: str


class SyncInfo(AccessResponseBase):
    """
    Get synchronisation informations.

    - height -
    - peers - array of peer structure, see :class:`pymoneroasync.models.daemon.outputs.Peer`
    - spans - array of span structure, see :class:`pymoneroasync.models.daemon.outputs.Span`
    - target_height - target height the node is syncing from (will be undefined if node is fully synced)
    """

    height: int
    target_height: int
    next_needed_pruning_seed: int
    peers: List[Peer]
    spans: Optional[List[Span]]
    overview: str


class BacklogEntry(BaseModel):
    """
    - blob_size - (in binary form)
    - fee - (in binary form)
    - time_in_pool - (in binary form)
    """

    weight: int
    fee: int
    time_in_pool: int


class GetTxPoolBacklog(AccessResponseBase):
    """
    Get all transaction pool backlog.

    backlog: array of structures tx_backlog_entry, see :class:`pymoneroasync.models.daemon.outputs.BacklogEntry`
    """

    backlog: Optional[List[BacklogEntry]]


class OutputDistributionData(BaseModel):
    pass


class Distribution(BaseModel):
    amount: int
    base: int
    binary: bool
    compress: bool
    distribution: List[int]


class GetOutputDistribution(AccessResponseBase):
    """
    Get output distribution.

    """

    distributions: Optional[List[Distribution]]


class GetHeight(ResponseBase):
    """
    Get the node's current height.

    - height - Current length of longest chain known to daemon.
    """

    height: int
    hash: str


# class TxOutputIndices(BaseModel):
#     indices: List[int]
#
#
# class BlockOutputIndices(BaseModel):
#     indices: List[TxOutputIndices]
#
#
# class GetBlocksBin(AccessResponseBase):
#     """
#     Get all blocks info. Binary request.
#     """
#
#     blocks: List[GetBlock]
#     start_height: int
#     current_height: int
#     output_indices: List[BlockOutputIndices]


class TxEntry(BaseModel):
    """
    - as_hex - Full transaction information as a hex string.
    - as_json - List of transaction info:
        - version - Transaction version
        - unlock_time - If not 0, this tells when a transaction output is spendable.
        - vin - List of inputs into transaction:
            - key - The public key of the previous output spent in this transaction.
                - amount - The amount of the input, in atomic units.
                - key_offsets - A list of integer offets to the input.
                - k_image - The key image for the given input
        - vout - List of outputs from transaction:
            - amount - Amount of transaction output, in atomic units.
            - target - Output destination information:
                - key - The stealth public key of the receiver. Whoever owns the private key associated with this key controls this transaction output.
        - extra - Usually called the "payment ID" but can be used to include any random 32 bytes.
        - signatures - List of signatures used in ring signature to hide the true origin of the transaction.
    - block_height - block height including the transaction
    - block_timestamp - Unix time at chich the block has been added to the blockchain
    - double_spend_seen - States if the transaction is a double-spend (true) or not (false)
    - in_pool - States if the transaction is in pool (true) or included in a block (false)
    - output_indices - transaction indexes
    - tx_hash - string; transaction hash
    """

    tx_hash: str
    as_hex: str
    pruned_as_hex: str
    prunable_as_hex: str
    prunable_hash: str
    as_json: str
    in_pool: bool
    double_spend_seen: bool
    block_height: int
    block_timestamp: datetime
    received_timestamp: Optional[datetime]
    output_indices: List[int]
    relayed: Optional[bool]


class GetTransactions(AccessResponseBase):
    """
    Look up one or more transactions by hash.


    - missed_tx - (Optional - returned if not empty) Transaction hashes that could not be found.
    - txs - array of structure entry as follows:
    - txs_as_hex - Full transaction information as a hex string (old compatibility parameter)
    - txs_as_json - (Optional - returned if set in inputs. Old compatibility parameter) List of transaction as in as_json above:
    """

    txs_as_hex: Optional[List[str]]
    txs_as_json: Optional[List[str]]
    txs: Optional[List[TxEntry]]
    missed_tx: Optional[List[str]]


class GetAltBlockHashes(AccessResponseBase):
    """
    Get the known blocks hashes which are not on the main chain.

    - blks_hashes - list of alternative blocks hashes to main chain
    """

    blks_hashes: Optional[List[str]]


class SpentStatusEnum(IntEnum):
    UNSPENT = 0
    SPENT_IN_BLOCKCHAIN = 1
    SPENT_IN_POOL = 2


class IsKeyImageSpent(AccessResponseBase):
    """
    Check if outputs have been spent using the key image associated with the output.

    - spent_status - List of statuses for each image checked.
        - 0 = unspent,
        - 1 = spent in blockchain,
        - 2 = spent in transaction pool
    """

    spent_status: Optional[List[SpentStatusEnum]]


class SendRawTx(AccessResponseBase):
    """
    Broadcast a raw transaction to the network.

    - double_spend - Transaction is a double spend (true) or not (false).
    - fee_too_low - Fee is too low (true) or OK (false).
    - invalid_input - Input is invalid (true) or valid (false).
    - invalid_output - Output is invalid (true) or valid (false).
    - low_mixin - Mixin count is too low (true) or OK (false).
    - not_rct - Transaction is a standard ring transaction (true) or a ring confidential transaction (false).
    - not_relayed - Transaction was not relayed (true) or relayed (false).
    - overspend - Transaction uses more money than available (true) or not (false).
    - reason - Additional information. Currently empty or "Not relayed" if transaction was accepted but not relayed.
    - status - General RPC error code. "OK" means everything looks good. Any other value means that something went wrong.
    - too_big - Transaction size is too big (true) or OK (false).
    - untrusted - States if the result is obtained using the bootstrap mode, and is therefore not trusted (true), or when the daemon is fully synced (false).
    """

    reason: str
    not_relayed: bool
    low_mixin: bool
    double_spend: bool
    invalid_input: bool
    invalid_output: bool
    too_big: bool
    overspend: bool
    fee_too_low: bool
    too_few_outputs: bool
    sanity_check_failed: bool


class MiningStatus(ResponseBase):
    """
    Get the mining status of the daemon.

    - active - States if mining is enabled (true) or disabled (false).
    - address - Account address daemon is mining to. Empty if not mining.
    - is_background_mining_enabled - States if the mining is running in background (true) or foreground (false).
    - speed - Mining power in hashes per seconds.
    - status - General RPC error code. "OK" means everything looks good. Any other value means that something went wrong.
    - threads_count - Number of running mining threads.
    """

    active: bool
    speed: int
    threads_count: int
    address: str
    pow_algorithm: str
    is_background_mining_enabled: bool
    bg_idle_threshold: int
    bg_min_idle_seconds: int
    bg_ignore_battery: bool
    bg_target: int
    block_target: int
    block_reward: int
    difficulty: int
    wide_difficulty: str
    difficulty_top64: int


class PeerListEntry(BaseModel):
    """
    - host - IP address
    - id - Peer id
    - ip - IP address in integer format
    - last_seen - unix time at which the peer has been seen for the last time
    - port - TCP port the peer is using to connect to monero network.
    """

    id: int
    host: Union[IPv4Address, IPv6Address]
    ip: int
    port: int
    rpc_port: Optional[int]
    rpc_credits_per_hash: Optional[int]
    last_seen: datetime
    pruning_seed: Optional[int]


class GetPeerList(ResponseBase):
    """
    Get the known peers list.

    - gray_list - array of offline peer structure, see :class:`pymoneroasync.models.daemon.outputs.PeerListEntry`
    - white_list - array of online peer structure, see :class:`pymoneroasync.models.daemon.outputs.PeerListEntry`
    """

    white_list: Optional[List[PeerListEntry]]
    gray_list: Optional[List[PeerListEntry]]


class SetLogCategories(ResponseBase):
    categories: str


class SpentKeyImageInfo(BaseModel):
    id_hash: str
    txs_hashes: List[str]


class TxInfo(BaseModel):
    """
    - blob_size - The size of the full transaction blob.
    - double_spend_seen - States if this transaction has been seen as double spend.
    - do_not_relay - States if this transaction should not be relayed
    - fee - The amount of the mining fee included in the transaction, in atomic units.
    - id_hash - The transaction ID hash.
    - kept_by_block - States if the tx was included in a block at least once (true) or not (false).
    - last_failed_height -If the transaction validation has previously failed, this tells at what height that occured.
    - last_failed_id_hash - Like the previous, this tells the previous transaction ID hash.
    - last_relayed_time - Last unix time at which the transaction has been relayed.
    - max_used_block_height - Tells the height of the most recent block with an output used in this transaction.
    - max_used_block_hash - Tells the hash of the most recent block with an output used in this transaction.
    - receive_time - The Unix time that the transaction was first seen on the network by the node.
    - relayed - States if this transaction has been relayed
    - tx_blob - Hexadecimal blob represnting the transaction.
    - tx_json - JSON structure of all information in the transaction:
        - version - Transaction version
        - unlock_time - If not 0, this tells when a transaction output is spendable.
        - vin - List of inputs into transaction:
            - key - The public key of the previous output spent in this transaction.
                - amount - The amount of the input, in atomic units.
                - key_offsets - A list of integer offets to the input.
                - k_image - The key image for the given input
        - vout - List of outputs from transaction:
            - amount - Amount of transaction output, in atomic units.
            - target - Output destination information:
                - key - The stealth public key of the receiver. Whoever owns the private key associated with this key controls this transaction output.
        - extra - Usually called the "transaction ID" but can be used to include any random 32 bytes.
        - rct_signatures - Ring signatures:
            - type
            - txnFee
            - ecdhInfo - array of Diffie Helman Elipctic curves structures as follows:
                - mask - String
                - amount - String
            - outPk
        - rctsig_prunable
            - rangeSigs - array of structures as follows:
                - asig
                - Ci
            - MGs - array of structures as follows:
                - ss - array of arrays of two strings.
                - cc - String
    """

    id_hash: str
    tx_json: str
    blob_size: int
    weight: int
    fee: int
    max_used_block_id_hash: str
    max_used_block_height: int
    kept_by_block: bool
    last_failed_height: int
    last_failed_id_hash: str
    receive_time: int
    relayed: bool
    last_relayed_time: int
    do_not_relay: bool
    double_spend_seen: bool
    tx_blob: str


class GetTransationPool(AccessResponseBase):
    """
    Show information about valid transactions seen by the node but not yet mined
    into a block, as well as spent key image information for the txpool in
    the node's memory.

    - spent_key_images - List of spent output key images
    - txs_hashes - tx hashes of the txes (usually one) spending that key image.
    """

    transactions: Optional[List[TxInfo]]
    spent_key_images: Optional[List[SpentKeyImageInfo]]


class TxPoolHisto(BaseModel):
    """
    - txs - number of transactions
    - bytes - size in bytes.
    """

    txs: int
    bytes: int


class TxPoolStats(BaseModel):
    """
    - bytes_max - Max transaction size in pool
    - bytes_med - Median transaction size in pool
    - bytes_min - Min transaction size in pool
    - bytes_total - total size of all transactions in pool
    - histo - structure txpool_histo see :class:`pymoneroasync.models.daemon.TxPoolHisto`
    - histo_98pc the time 98% of txes are "younger" than
    - num_10m number of transactions in pool for more than 10 minutes
    - num_double_spends number of double spend transactions
    - num_failing number of failing transactions
    - num_not_relayed number of non-relayed transactions
    - oldest unix time of the oldest transaction in the pool
    - txs_total total number of transactions.
    """

    bytes_total: int
    bytes_min: int
    bytes_max: int
    bytes_med: int
    fee_total: int
    oldest: int
    txs_total: int
    num_failing: int
    num_10m: int
    num_not_relayed: int
    histo_98pc: int
    histo: Optional[List[TxPoolHisto]]
    num_double_spends: int


class GetTransationPoolStats(AccessResponseBase):
    """ "
    Get the transaction pool statistics.

    - pool_stats, see :class:`pymoneroasync.models.daemon.outputs.TxPoolStats`
    """

    pool_stats: TxPoolStats


class Limit(ResponseBase):
    """
    Daemon bandwidth limits.

    - limit_down - Download limit in kBytes per second
    - limit_up - Upload limit in kBytes per second
    """

    limit_up: int
    limit_down: int


class OutPeers(ResponseBase):
    """
    Limit number of Outgoing peers.

    - out_peers - Max number of outgoing peers
    """

    out_peers: int


class InPeers(ResponseBase):
    """
    Limit number of Incoming peers.

    - in_peers - Max number of incoming peers
    """

    in_peers: int


class OutKey(BaseModel):
    """
    - height - block height of the output
    - key - the public key of the output
    - mask -
    - txid - transaction id
    - unlocked - States if output is locked (false) or not (true)
    """

    key: str
    mask: str
    unlocked: bool
    height: int
    txid: str


class GetOuts(AccessResponseBase):
    """
    Get outputs.

    - outs -  array of structure OutKey, see :class:`pymoneroasync.models.daemon.outputs.OutKey`
    """

    outs: Optional[List[OutKey]]


class Update(ResponseBase):
    """
    Update daemon.

    - auto_uri -
    - hash -
    - path - path to download the update
    - update - States if an update is available to download (true) or not (false)
    - user_uri -
    - version - Version available for download.
    """

    update: bool
    version: str
    user_uri: str
    auto_uri: str
    hash: str
    path: str
