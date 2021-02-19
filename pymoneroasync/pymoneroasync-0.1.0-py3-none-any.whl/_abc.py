import abc
import json
from abc import ABC
from typing import Any, List, Literal, Mapping, Optional, Tuple
from urllib.parse import urljoin, urlunsplit

from sansio_jsonrpc import (
    JsonRpcException,
    JsonRpcParseError,
    JsonRpcPeer,
    JsonRpcResponse,
)
from sansio_jsonrpc.types import JsonRpcParams

from pymoneroasync import sansio
from pymoneroasync.const import (
    DAEMON_JSON_RPC_METHODS_OUTPUTS,
    DAEMON_OTHER_RPC_METHODS_OUTPUTS,
)
from pymoneroasync.models.daemon.inputs import (
    DaemonJsonRPCIn,
    DaemonOtherRPCIn,
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


class BaseAsync(abc.ABC):

    _sansio_client: JsonRpcPeer
    url: str

    @abc.abstractmethod
    async def _post(
        self, url: str, body: bytes
    ) -> Tuple[int, Mapping[str, str], bytes]:
        pass

    async def _make_jsonrpc_request(
        self, rpc_method: str, params: Optional[JsonRpcParams] = None
    ) -> List[JsonRpcResponse]:
        request_id, bytes_to_send = self._sansio_client.request(
            method=rpc_method,
            params=params,
        )
        url = urljoin(self.url, "json_rpc")
        status_code, headers, content = await self._post(url, bytes_to_send)
        try:
            # parse returns a tuple of all messages, but since we sent only one
            # we return only one as well, the first and only
            messages = []
            for message in self._sansio_client.parse(content):
                assert isinstance(message, JsonRpcResponse)
                if message.success:
                    messages.append(message)
                elif message.error:
                    raise JsonRpcException.exc_from_error(message.error)

            return messages
        except JsonRpcParseError as pe:
            print("Exception while parsing response", pe)
            raise pe

    async def _make_other_rpc_request(
        self, path: str = "", params: Optional[JsonRpcParams] = None
    ) -> Optional[JsonRpcParams]:
        url = urljoin(self.url, path)
        bytes_to_send = sansio.request(params)
        status_code, headers, content = await self._post(url, bytes_to_send)
        try:
            message = sansio.parse(content)
            return message
        except Exception as e:
            raise e

    async def _make_jsonrpc(
        self,
        rpc_method: Literal[
            "get_block_count",
            "on_get_block_hash",
            "get_block_template",
            "submit_block",
            "get_last_block_header",
            "get_block_header_by_hash",
            "get_block_header_by_height",
            "get_block_headers_range",
            "get_block",
            "get_connections",
            "get_info",
            "hard_fork_info",
            "set_bans",
            "get_bans",
            "flush_txpool",
            "get_output_histogram",
            "get_coinbase_tx_sum",
            "get_version",
            "get_fee_estimate",
            "get_alternate_chains",
            "relay_tx",
            "sync_info",
            "get_txpool_backlog",
            "get_output_distribution",
        ],
        params: Optional[DaemonJsonRPCIn],
    ) -> Any:
        if params is not None:
            params_parsed = json.loads(params.json())
        else:
            params_parsed = None
        res = await self._make_jsonrpc_request(
            rpc_method=rpc_method, params=params_parsed
        )

        if isinstance(res[0].result, dict):
            res_obj = DAEMON_JSON_RPC_METHODS_OUTPUTS[rpc_method](**res[0].result)
            a = sorted(res[0].result.keys())
            b = sorted([k for k, v in res_obj.__fields__.items() if v.required])
            assert len(a) >= len(b)
        else:
            res_obj = DAEMON_JSON_RPC_METHODS_OUTPUTS[rpc_method](
                __root__=res[0].result
            )

        return res_obj

    async def _make_other_rpc(
        self,
        path: Literal[
            "get_height",
            "get_transactions",
            "get_alt_blocks_hashes",
            "is_key_image_spent",
            "send_raw_transaction",
            "start_mining",
            "stop_mining",
            "mining_status",
            "save_bc",
            "get_peer_list",
            "set_log_hash_rate",
            "set_log_level",
            "set_log_categories",
            "get_transaction_pool",
            "get_transaction_pool_stats",
            "stop_daemon",
            "set_limit",
            "get_limit",
            "out_peers",
            "in_peers",
            "get_outs",
            "update",
        ],
        params: Optional[DaemonOtherRPCIn],
    ) -> Any:
        if params is not None:
            params_parsed = json.loads(params.json())
        else:
            params_parsed = None
        res = await self._make_other_rpc_request(path=path, params=params_parsed)

        if isinstance(res, dict):
            res_obj = DAEMON_OTHER_RPC_METHODS_OUTPUTS[path](**res)
            a = sorted(res.keys())
            b = sorted([k for k, v in res_obj.__fields__.items() if v.required])
            assert len(a) >= len(b)
        else:
            res_obj = DAEMON_OTHER_RPC_METHODS_OUTPUTS[path](__root__=res)

        return res_obj


class AsyncDaemon(BaseAsync, ABC):
    def __init__(
        self,
        scheme: str = "http",
        host: str = "127.0.0.1",
        port: int = 18081,
        username: str = "",
        password: str = "",
    ):
        self.url = urlunsplit((scheme, f"{host}:{port}", "", "", ""))
        self.username = username
        self.password = password
        self._sansio_client = JsonRpcPeer()

    async def get_block_count(self) -> GetBlockCount:
        """
        Look up how many blocks are in the longest chain known to the node.
        """
        r: GetBlockCount = await self._make_jsonrpc("get_block_count", None)
        return r

    async def on_get_block_hash(self, params: OnGetBlockHashIn) -> OnGetBlockHash:
        """
        Look up a block's hash by its height.
        """
        r: OnGetBlockHash = await self._make_jsonrpc("on_get_block_hash", params)
        return r

    async def get_block_template(self, params: GetBlockTemplateIn) -> GetBlockTemplate:
        """
        Get a block template on which mining a new block.
        """
        r: GetBlockTemplate = await self._make_jsonrpc("get_block_template", params)
        return r

    async def submit_block(self, params: SubmitBlockIn) -> ResponseBase:
        """
        Submit a mined block to the network.
        """
        r: ResponseBase = await self._make_jsonrpc("submit_block", params)
        return r

    async def get_last_block_header(
        self, params: GetBlockHeaderBaseIn
    ) -> GetBlockHeader:
        """
        Block header information for the most recent block.
        """
        r: GetBlockHeader = await self._make_jsonrpc("get_last_block_header", params)
        return r

    async def get_block_header_by_hash(
        self, params: GetBlockHeaderByHashIn
    ) -> GetBlockHeader:
        """
        Block header information retrieved using a block's hash.
        """
        r: GetBlockHeader = await self._make_jsonrpc("get_block_header_by_hash", params)
        return r

    async def get_block_header_by_height(
        self, params: GetBlockHeaderByHeightIn
    ) -> GetBlockHeader:
        """
        Block header information retrieved using a block's height.
        """
        r: GetBlockHeader = await self._make_jsonrpc(
            "get_block_header_by_height", params
        )
        return r

    async def get_block_headers_range(
        self, params: GetBlockHeadersIn
    ) -> GetBlockHeaders:
        """
        Block headers information for a range of blocks.
        """
        r: GetBlockHeaders = await self._make_jsonrpc("get_block_headers_range", params)
        return r

    async def get_block(self, params: GetBlockIn) -> GetBlock:
        """
        Full block information
        """
        r: GetBlock = await self._make_jsonrpc("get_block", params)
        return r

    async def get_connections(self) -> GetConnections:
        """
        Retrieve information about incoming and outgoing connections to your node.
        """
        r: GetConnections = await self._make_jsonrpc("get_connections", None)
        return r

    async def get_info(self) -> GetInfo:
        """
        Retrieve general information about the state of your node and the network.
        """
        r: GetInfo = await self._make_jsonrpc("get_info", None)
        return r

    async def hard_fork_info(self) -> HardForkInfo:
        """
        Look up information regarding hard fork voting and readiness.
        """
        r: HardForkInfo = await self._make_jsonrpc("hard_fork_info", None)
        return r

    async def set_bans(self, params: SetBansIn) -> ResponseBase:
        """
        Ban another node by IP.
        """
        r: ResponseBase = await self._make_jsonrpc("set_bans", params)
        return r

    async def get_bans(self) -> GetBans:
        """
        Get list of banned IPs.
        """
        r: GetBans = await self._make_jsonrpc("get_bans", None)
        return r

    async def flush_txpool(self, params: TxIn) -> ResponseBase:
        """
        Flush tx ids from transaction pool.
        """
        r: ResponseBase = await self._make_jsonrpc("flush_txpool", params)
        return r

    async def get_output_histogram(
        self, params: GetOutputHistogramIn
    ) -> GetOutputHistogram:
        """
        Get a histogram of output amounts. For all amounts
        (possibly filtered by parameters), gives the number of outputs on the chain
        for that amount. RingCT outputs counts as 0 amount.
        """
        r: GetOutputHistogram = await self._make_jsonrpc("get_output_histogram", params)
        return r

    async def get_coinbase_tx_sum(self, params: GetCoinbaseTxSumIn) -> GetCoinbaseTxSum:
        """
        Get the coinbase amount and the fees amount for n last blocks starting at
        particular height
        """
        r: GetCoinbaseTxSum = await self._make_jsonrpc("get_coinbase_tx_sum", params)
        return r

    async def get_version(self) -> GetVersion:
        """
        Give the node current version.
        """
        r: GetVersion = await self._make_jsonrpc("get_version", None)
        return r

    async def get_fee_estimate(self, params: GetFeeEstimateIn) -> GetFeeEstimate:
        """
        Gives an estimation on fees per byte.
        """
        r: GetFeeEstimate = await self._make_jsonrpc("get_fee_estimate", params)
        return r

    async def get_alternate_chains(self) -> GetAlternateChains:
        """
        Display alternative chains seen by the node.
        """
        r: GetAlternateChains = await self._make_jsonrpc("get_alternate_chains", None)
        return r

    async def relay_tx(self, params: TxIn) -> AccessResponseBase:
        """
        Relay a list of transaction IDs.
        """
        r: AccessResponseBase = await self._make_jsonrpc("relay_tx", params)
        return r

    async def sync_info(self) -> SyncInfo:
        """
        Get synchronisation informations.
        """
        r: SyncInfo = await self._make_jsonrpc("sync_info", None)
        return r

    async def get_txpool_backlog(self) -> GetTxPoolBacklog:
        """
        Get all transaction pool backlog
        """
        r: GetTxPoolBacklog = await self._make_jsonrpc("get_txpool_backlog", None)
        return r

    async def get_output_distribution(
        self, params: GetOutputDistributionIn
    ) -> GetOutputDistribution:
        """
        Get output distribution.
        """
        r: GetOutputDistribution = await self._make_jsonrpc(
            "get_output_distribution", params
        )
        return r

    async def get_height(self) -> GetHeight:
        """
        Get the node's current height.
        """
        r: GetHeight = await self._make_other_rpc("get_height", None)
        return r

    # async def get_blocks_bin(self, params: GetBlocksBinIn) -> GetBlocksBin:
    #     """
    #     Get all blocks info. Binary request.
    #     """
    #     r = await self._make_other_rpc("get_blocks.bin", params)
    #     return cast(GetBlocksBin, r)

    async def get_transactions(self, params: GetTransactionsIn) -> GetTransactions:
        """
        Look up one or more transactions by hash.
        """
        r: GetTransactions = await self._make_other_rpc("get_transactions", params)
        return r

    async def get_alt_blocks_hashes(self) -> GetAltBlockHashes:
        """
        Get the known blocks hashes which are not on the main chain.
        """
        r: GetAltBlockHashes = await self._make_other_rpc("get_alt_blocks_hashes", None)
        return r

    async def is_key_image_spent(self, params: IsKeyImageSpentIn) -> IsKeyImageSpent:
        """
        Check if outputs have been spent using the key image associated with the output.
        """
        r: IsKeyImageSpent = await self._make_other_rpc("is_key_image_spent", params)
        return r

    async def send_raw_transaction(self, params: SendRawTxIn) -> SendRawTx:
        """
        Broadcast a raw transaction to the network.
        """
        r: SendRawTx = await self._make_other_rpc("send_raw_transaction", params)
        return r

    async def start_mining(self, params: StartMiningIn) -> ResponseBase:
        """
        Start mining on the daemon.
        """
        r: ResponseBase = await self._make_other_rpc("start_mining", params)
        return r

    async def stop_mining(self) -> ResponseBase:
        """
        Stop mining on the daemon.
        """
        r: ResponseBase = await self._make_other_rpc("stop_mining", None)
        return r

    async def mining_status(self) -> MiningStatus:
        """
        Get the mining status of the daemon.
        """
        r: MiningStatus = await self._make_other_rpc("mining_status", None)
        return r

    async def save_bc(self) -> ResponseBase:
        """
        Save the blockchain. The blockchain does not need saving and is always saved
        when modified, however it does a sync to flush the filesystem cache onto the
        disk for safety purposes against Operating System or Harware crashes.
        """
        r: ResponseBase = await self._make_other_rpc("save_bc", None)
        return r

    async def get_peer_list(self) -> GetPeerList:
        """
        Get the known peers list.
        """
        r: GetPeerList = await self._make_other_rpc("get_peer_list", None)
        return r

    async def set_log_hash_rate(self, params: SetLogHashRateIn) -> ResponseBase:
        """
        Set the log hash rate display mode.
        """
        r: ResponseBase = await self._make_other_rpc("set_log_hash_rate", params)
        return r

    async def set_log_level(self, params: SetLogLevelIn) -> ResponseBase:
        """
        Set the daemon log level. By default, log level is set to 0.
        """
        r: ResponseBase = await self._make_other_rpc("set_log_level", params)
        return r

    async def set_log_categories(self, params: SetLogCategoriesIn) -> SetLogCategories:
        """
        Set the daemon log categories. Categories are represented as a comma separated
        list of <Category>:<Level>

        For an extensive list of <Category>:<Level> see:

        - :const:`pymoneroasync.const.DAEMON_LOG_CATEGORIES`
        - :const:`pymoneroasync.const.DAEMON_LOG_LEVELS`

        For the defaults of <Category>:<Level> see:

        - :const:`pymoneroasync.const.DAEMON_DEFAULT_LOG`
        - :const:`pymoneroasync.const.DAEMON_DEFAULT_LOG_RPC`
        """
        r: SetLogCategories = await self._make_other_rpc("set_log_categories", params)
        return r

    async def get_transaction_pool(self) -> GetTransationPool:
        """
        Show information about valid transactions seen by the node but not yet mined
        into a block, as well as spent key image information for the txpool in
        the node's memory.
        """
        r: GetTransationPool = await self._make_other_rpc("get_transaction_pool", None)
        return r

    async def get_transaction_pool_stats(self) -> GetTransationPoolStats:
        """
        Get the transaction pool statistics.
        """
        r: GetTransationPoolStats = await self._make_other_rpc(
            "get_transaction_pool_stats", None
        )
        return r

    async def stop_daemon(self) -> ResponseBase:
        """
        Send a command to the daemon to safely disconnect and shut down.
        """
        r: ResponseBase = await self._make_other_rpc("stop_daemon", None)
        return r

    async def set_limit(self, params: LimitIn) -> Limit:
        """
        Set daemon bandwidth limits.
        """
        r: Limit = await self._make_other_rpc("set_limit", params)
        return r

    async def get_limit(self) -> Limit:
        """
        Get daemon bandwidth limits.
        """
        r: Limit = await self._make_other_rpc("get_limit", None)
        return r

    async def out_peers(self, params: OutPeersIn) -> OutPeers:
        """
        Limit number of Outgoing peers.
        """
        r: OutPeers = await self._make_other_rpc("out_peers", params)
        return r

    async def in_peers(self, params: InPeersIn) -> InPeers:
        """
        Limit number of Incoming peers.
        """
        r: InPeers = await self._make_other_rpc("in_peers", params)
        return r

    async def get_outs(self, params: GetOutsIn) -> GetOuts:
        """
        Get outputs.
        """
        r: GetOuts = await self._make_other_rpc("get_outs", params)
        return r

    async def update(self, params: UpdateIn) -> Update:
        """
        Update daemon.
        """
        r: Update = await self._make_other_rpc("update", params)
        return r
