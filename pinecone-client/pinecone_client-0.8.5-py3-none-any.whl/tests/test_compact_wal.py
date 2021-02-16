from pinecone.network.zmq.wal import WALServlet
from pinecone.network.zmq.spec import ServletSpec
from pinecone.protos import core_pb2
from pinecone.utils import load_numpy, dump_numpy
import numpy as np

import asyncio
import pytest
import os

DATA = np.array([[2.0, 3.0, 4.0], [5.1, 2.3, 0.2]])

DIR = '/tmp/compact_wal'

@pytest.mark.asyncio
async def test_compact_wal():
    os.environ['HOSTNAME'] = 'waltest'
    servlet_spec = ServletSpec(handle_msg=None, in_sockets=[], out_sockets=dict())
    if os.path.exists(DIR + '/log'):
        os.remove(DIR + '/log')
    wal = WALServlet(servlet_spec, 1, DIR)

    for i in range(0, 100):
        await wal.put(core_pb2.Request(
            index=core_pb2.IndexRequest(ids=[str(i), str(i) + 'b'], data=dump_numpy(DATA))))
    for i in range(0, 100):
        await wal.put(core_pb2.Request(
            index=core_pb2.IndexRequest(ids=[str(i)], data=dump_numpy(DATA[[0], :]))))

    await wal.start_compact_log()

    for pos, entry in wal.sync_replay_log(0):
        if pos < 100:
            assert len(entry.index.ids) == 1
            assert entry.index.ids[0] == str(99 - pos)
            assert load_numpy(entry.index.data).all() == DATA[[1], :].all()
        else:
            assert len(entry.index.ids) == 1
            assert entry.index.ids[0] == str(199 - pos) + 'b'
            assert load_numpy(entry.index.data).all() == DATA[[0], :].all()

    for i in range(100, 110):
        await wal.put(core_pb2.Request(
            delete=core_pb2.DeleteRequest(ids=[str(i)])))
    await wal.start_compact_log()


if __name__ == '__main__':
    asyncio.run(test_compact_wal())
