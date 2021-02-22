from dataclasses import dataclass
from typing import Optional, Union

from eiprice.httpclient.core.methods import Method


@dataclass
class DownloadSpec:
    url: str
    method: Method
    headers: Optional[dict] = None
    params: Optional[dict] = None
    json: Optional[dict] = None
    data: Optional[Union[dict, str]] = None
    proxies: Optional[dict] = None
    cookies: Optional[dict] = None
    time_between_requests: Union[int, float] = None
    verify: Optional[bool] = True
    timeout: Optional[int] = 60

