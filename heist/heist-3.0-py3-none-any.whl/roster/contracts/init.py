# Import python libs
from typing import Any, Dict, Mapping


def sig_read(hub) -> Dict[str, Any]:
    ...


async def post_read(hub, ctx):
    ret = ctx.ret
    for data in ret.values():
        assert isinstance(data, Mapping)
    return ret
