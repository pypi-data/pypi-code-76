#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from .exceptions import InvalidOffsetException
from pinecone.utils import replica_kube_hostname, replica_name
from pinecone.protos import core_pb2
from pinecone.network.zmq.servlet import ZMQServlet
from pinecone.utils import open_or_create, get_hostname, wal
from pinecone.utils.constants import MAX_CLIENTS, SEND_TIMEOUT, ZMQ_LOG_PORT, MAX_MSGS_PENDING
from pinecone.network.zmq.spec import ServletSpec, SocketType, Socket

from typing import Iterable, Tuple, List
from loguru import logger

import concurrent.futures
from threading import Lock
import asyncio
import os
import functools
import mmap
import zmq


class WALServlet(ZMQServlet):
    """
    ZMQServlet for distributed stateful functions to provide
    - client ordering guarantees
    - replay recovery from disk
    - leader-follower replication
    """

    def __init__(self, servlet_spec: ServletSpec, num_replicas: int, path: str, volume_request: int = 15):
        super().__init__(servlet_spec)
        self.replica = servlet_spec.replica
        self.num_replicas = num_replicas
        self.wal_size_limit = volume_request * (10 ** 9) * 0.33  # translate to GB

        self.executor = concurrent.futures.ThreadPoolExecutor()

        self.log_in = self.init_socket(self.log_in_socket)
        self.log_outs = [self.init_socket(log_out_socket) for log_out_socket in self.log_out_sockets()]

        self.in_buffer = asyncio.Queue()
        self.in_msgs = asyncio.Queue(maxsize=MAX_MSGS_PENDING)

        os.makedirs(path, exist_ok=True)

        self.log_path = os.path.join(path, 'log')
        self.tmp_log_path = os.path.join(path, 'tmp_log')  # for compaction
        self.log_file = open_or_create(self.log_path)
        self.log_lock = Lock()

        self.log_compaction_started = False

        self.last = None
        self.size = self.load_size()

        offset_path = os.path.join(path, 'offsets')
        self.offset_file = open_or_create(offset_path, truncate=wal.OFFSET_BYTES*self.num_replicas)
        self.offsets = mmap.mmap(self.offset_file.fileno(), 0)
        self.offset_locks = [Lock() for _ in range(0, self.num_replicas)]

        client_offsets_path = os.path.join(path, 'client_offsets')
        self.client_offsets_file = open_or_create(client_offsets_path, truncate=wal.OFFSET_BYTES*MAX_CLIENTS)

        self.client_offsets = mmap.mmap(self.client_offsets_file.fileno(), 0)
        self.client_offsets_locks = [Lock() for _ in range(0, MAX_CLIENTS)]

    @property
    def log_in_socket(self):
        return Socket(True, SocketType.PULL, ZMQ_LOG_PORT, host=get_hostname())

    def log_out_sockets(self):
        return [
            Socket(False, SocketType.PUSH,
                   host=replica_name(self.spec.function_name, self.spec.shard, replica_id=replica_id) if self.spec.native
                   else replica_kube_hostname(self.spec.function_name, self.spec.shard, replica_id),
                   port=ZMQ_LOG_PORT)
            for replica_id in range(0, self.num_replicas)]

    def load_size(self):
        size = 0
        for pos, entry in self.sync_replay_log(0):
            size += 1
            self.last = entry
        return size

    def cleanup(self):
        self.offset_file.close()
        self.log_file.close()

    @property
    def leader(self):
        return self.replica == 0

    async def poll_log_socks(self):
        while True:
            msg = await self.recv_log_msg()
            await self.handle_log_msg(msg)

    async def poll_sock(self, sock: zmq.Socket):
        while True:
            msg = await self.recv_msg(sock)
            if self.use_wal(msg):
                await self.in_msgs.put(msg)
            else:
                await self.handle_msg(msg)

    def start_polling(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [*(loop.create_task(self.poll_sock(sock)) for sock in self.zmq_ins), loop.create_task(self.poll_log_socks())]

    def use_wal(self, msg: core_pb2.Request) -> bool:
        req_type = msg.WhichOneof('body')
        return req_type in ['index', 'delete']

    async def handle_msg_wal(self, msg: core_pb2.Request):
        new_offset = await self.put(msg)
        await self.handle_msg(msg)
        await self.set_client_offset(msg.client_id, msg.client_offset + 1)
        await self.ack(new_offset)

    async def handle_log_msg(self, msg: 'core_pb2.LogEntry'):
        if not self.leader:
            try:
                if await self.put(msg.entry, offset=msg.offset):
                    await self.handle_msg(msg.entry)
            except InvalidOffsetException:
                await self.send_log_msg(self.get_replay_request(), 0)
        else:
            await self.remote_ack(msg.offset, msg.ack.replica, msg.ack.replay)

    async def consume_msgs(self):
        while True:
            msg = await self.in_msgs.get()
            if self.is_next(msg.client_id, msg.client_offset):
                await self.handle_msg_wal(msg)
                while True:
                    try:
                        await self.in_msgs.put(self.in_buffer.get_nowait())
                    except asyncio.QueueEmpty:
                        break
            else:
                # logger.error(f"Invalid client_offset {msg.client_offset}")
                if msg.client_offset >= self.get_client_offset(msg.client_id):
                    await self.in_buffer.put(msg)
                # elif msg.client_offset == self.get_client_offset(msg.client_id) - 1:
                #     await self.send_msg(msg)

    async def recv_log_msg(self):
        msg = await self.log_in.recv()
        msg_pb = core_pb2.LogEntry()
        msg_pb.ParseFromString(msg)
        return msg_pb

    async def send_log_msg(self, msg: 'core_pb2.LogEntry', replica: int):
        assert replica != self.spec.replica
        while True:
            try:
                await asyncio.wait_for(self.log_outs[replica].send(msg.SerializeToString()), SEND_TIMEOUT)
                break
            except asyncio.TimeoutError:
                logger.error("SENDING TIMED OUT, RETRYING")

    async def run_sync(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, functools.partial(func, *args, **kwargs))

    def get_offset(self, replica: int):
        start = wal.OFFSET_BYTES * replica
        return int.from_bytes(self.offsets[start:start + wal.OFFSET_BYTES], wal.BYTEORDER)

    def offsets_list(self):
        return [self.get_offset(replica) for replica in range(0, self.num_replicas)]

    def write_offset(self, replica: int, offset: int):
        with self.offset_locks[replica]:
            self.offsets.seek(replica * wal.OFFSET_BYTES)
            self.offsets.write(offset.to_bytes(wal.OFFSET_BYTES, wal.BYTEORDER))
            self.offsets.flush()

    async def set_offset(self, replica: int, offset: int):
        await self.run_sync(self.write_offset, replica, offset)

    def get_client_offset(self, client_id: int):
        if client_id >= MAX_CLIENTS:
            return 0
        with self.client_offsets_locks[client_id]:
            start = client_id * wal.OFFSET_BYTES
            return int.from_bytes(self.client_offsets[start:start + wal.OFFSET_BYTES], wal.BYTEORDER)

    def is_next(self, client_id: int, client_offset: int):
        if self.leader:
            if client_offset == 0:
                self.sync_set_client_offset(client_id, 0)  # should make this async
            return client_offset == self.get_client_offset(client_id)
        else:
            return True

    def sync_set_client_offset(self, client_id: int, client_offset: int):
        if client_id >= MAX_CLIENTS:
            return
        with self.client_offsets_locks[client_id]:
            start = client_id * wal.OFFSET_BYTES
            self.client_offsets[start:start + wal.OFFSET_BYTES] = client_offset.to_bytes(wal.OFFSET_BYTES, wal.BYTEORDER)
            self.client_offsets.flush()

    async def set_client_offset(self, client_id: int, client_offset: int):
        if self.get_client_offset(client_id) > client_offset:
            return
        await self.run_sync(self.sync_set_client_offset, client_id, client_offset)

    def sync_put(self, entry: core_pb2.Request, offset: int):
        if (not offset) or (self.size + 1) == offset:
            with self.log_lock:
                wal.write_log_entry(self.log_file, entry)
                self.size += 1
                # we need to copy the message, because it might get changed later on
                self.last = core_pb2.Request()
                self.last.CopyFrom(entry)
                logfile_size = self.log_file.tell()
            return logfile_size, self.size

        elif offset <= self.size:
            return self.log_file.tell(), None
        else:
            raise InvalidOffsetException

    async def put(self, item: core_pb2.Request, offset: int = None):
        if not self.leader and offset is None:
            raise RuntimeError(f"{get_hostname()} Attempted to write directly to replica {self.replica} instead of leader")
        logfile_size, offset = await self.run_sync(self.sync_put, item, offset)
        if logfile_size > self.wal_size_limit and not self.log_compaction_started:
            loop = asyncio.get_event_loop()
            loop.create_task(self.start_compact_log())
        return offset

    def sync_replay_log(self, offset: int, end_offset: int = None) -> Iterable[Tuple[int, core_pb2.Request]]:
        """
        Replay log from offset 0 (inclusive) to end_offset (exclusive)
        :param offset:
        :param end_offset:
        :return:
        """
        with self.log_lock:
            self.log_file.seek(0)
            pos = 0
            while True:
                entry, msg_bytes = wal.read_entry(self.log_file)

                if msg_bytes == b'' or (end_offset and pos >= end_offset):
                    break
                if pos >= offset:
                    yield pos, entry
                pos += 1

    def get_leader_log_backlog(self, replica: int) -> Iterable[core_pb2.LogEntry]:
        return [core_pb2.LogEntry(entry=entry, offset=offset)
                for offset, entry in self.sync_replay_log(self.get_offset(replica))]

    def sync_ack(self, offset: int):
        self.write_offset(self.replica, offset)

    async def ack(self, offset: int):
        prev_offset = self.get_offset(self.replica)
        if prev_offset > offset:
            logger.warning('Acked offset less than current offset')
        # elif prev_offset + 1 > offset:
        #     logger.warning('Acked by more than one offset')

        await self.set_offset(self.replica, offset)

        if self.leader:
            for r in range(1, self.num_replicas):
                msg = core_pb2.LogEntry(entry=self.last, offset=offset)
                await self.send_log_msg(msg, r)
        else:
            ack = core_pb2.Ack(replica=self.replica)
            await self.send_log_msg(core_pb2.LogEntry(offset=offset, ack=ack), 0)

    async def remote_ack(self, start_offset: int, replica: int, replay=False):
        if replay:
            leader_offset = self.get_offset(self.replica)
            logs = await self.run_sync(lambda s: list(self.sync_replay_log(s, end_offset=leader_offset)), start_offset)
            if not leader_offset == len(logs) + start_offset:
                logger.error(f"INCORRECT LENGTH OF REPLAY LOG {len(logs)} OFFSETS: {self.offsets_list()}. Size {self.size} start offset: {start_offset} ledaer: {leader_offset}")
            for offset, msg in logs:
                await self.send_log_msg(core_pb2.LogEntry(entry=msg, offset=offset), replica)

    def get_replay_request(self):
        ack = core_pb2.Ack(replica=self.replica, replay=True)
        return core_pb2.LogEntry(offset=self.get_offset(self.replica), ack=ack)

    def load_sync(self, handler):
        logger.info(f'Recovering from local WAL: offset: {self.get_offset(self.replica)}')
        for offset, entry in self.sync_replay_log(self.get_offset(self.replica)):
            response = handler(entry)  # type: core_pb2.Request
            self.sync_ack(offset)
            if self.leader:
                yield response

    def swap_log_files(self, end_file_offset: int):
        tmp_log_file = open(self.tmp_log_path, "r+b")

        with self.log_lock:
            self.log_file.seek(end_file_offset)
            while True:
                entry, msg_bytes = wal.read_entry(self.log_file)
                if msg_bytes == b'':
                    break
                wal.write_log_entry(tmp_log_file, entry)
            tmp_log_file.close()
            self.log_file.close()
            os.remove(self.log_path)
            os.rename(self.tmp_log_path, self.log_path)
            self.log_file = open(self.log_path, "r+b")

    async def start_compact_log(self):
        with self.log_lock:
            self.log_compaction_started = True
            end_file_offset = self.log_file.tell()
            self.log_file.flush()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(concurrent.futures.ProcessPoolExecutor(), wal.compact_log,
                                   self.log_path, self.tmp_log_path, end_file_offset)

        await self.run_sync(self.swap_log_files, end_file_offset)
        self.log_compaction_started = False

    @property
    def all_socks(self):
        return [*super().all_socks, self.log_in, *self.log_outs]
