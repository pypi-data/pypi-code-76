import logging
import os
import sys

from aiohttp import web
from .bindings import version
from .ledger import build_get_txn_request
from .pool import Pool, open_pool

LOGGER = logging.getLogger(__name__)
GENESIS_PATH: str = None
POOL: Pool = None
ROUTES = web.RouteTableDef()


@ROUTES.get("/genesis")
async def genesis(request):
    if not POOL:
        return web.Response(status=503)
    genesis = await POOL.get_transactions()
    LOGGER.info("got txns")
    return web.json_response(genesis)


@ROUTES.get("/txn")
async def txn(request):
    if not POOL:
        return web.Response(status=503)
    req = build_get_txn_request(None, None, 15)
    resp = await POOL.submit_request(req)
    return web.json_response(resp)


async def boot(app):
    global POOL
    POOL = await open_pool(transactions_path=GENESIS_PATH)


if __name__ == "__main__":
    LOGGER.info("indy-vdr version: %s", version())

    GENESIS_PATH = len(sys.argv) > 1 and sys.argv[1] or "genesis.txn"

    APP = web.Application()
    APP.add_routes(ROUTES)
    APP.on_startup.append(boot)
    LOGGER.info("Running webserver...")
    PORT = int(os.getenv("PORT", "8000"))
    web.run_app(APP, host="0.0.0.0", port=PORT)
