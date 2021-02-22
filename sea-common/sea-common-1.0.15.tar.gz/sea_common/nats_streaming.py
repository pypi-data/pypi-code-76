from typing import Optional
from asyncio import AbstractEventLoop
from nats.aio.client import Client as Nats
from stan.aio.client import Client as Stan


class NatsStreaming:
    nc: Optional[Nats] = None
    sc: Optional[Stan] = None

    async def connect(self, cluster_id: str, client_id: str, url: str, loop):
        # Use borrowed connection for NATS then mount NATS Streaming client on top.
        self.nc = Nats()
        await self.nc.connect(servers=[url], io_loop=loop)

        # Start session with NATS Streaming cluster.
        self.sc = Stan()
        await self.sc.connect(cluster_id, client_id, nats=self.nc)

        print('Connected to NATS Streaming server!')

    async def close(self):
        await self.sc.close()
        await self.nc.close()

    async def shutdown(self, loop: AbstractEventLoop):
        try:
            await nats.close()
            print('NATS connection closed')
        except:
            pass
        finally:
            loop.stop()


nats = NatsStreaming()
