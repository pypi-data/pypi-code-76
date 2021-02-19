import json
from typing import Optional

from sansio_jsonrpc.types import JsonRpcParams


def request(params: Optional[JsonRpcParams]) -> bytes:
    if params:
        bytes_to_send = json.dumps(params).encode()
    else:
        bytes_to_send = b""
    return bytes_to_send


def parse(content: bytes) -> Optional[JsonRpcParams]:
    if content != b"":
        parsed_bytes: JsonRpcParams = json.loads(content.decode())
        return parsed_bytes
    else:
        return None
