import requests
from functools import partial
from typing import Optional, List, Tuple

from django.conf import settings

BASE_URL = "https://api.cloudflare.com/client/v4"
AUTH_HEADERS = {
    "X-Auth-Email": settings.CLOUDFLARE["AUTH_EMAIL"],
    "X-Auth-Key": settings.CLOUDFLARE["AUTH_KEY"],
}


def purge_remote_cache(urls: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Function to purge saved pages on remote cache.
    At the moment only Cloudflare is supported.
    """
    url = f"{BASE_URL}/zones/{settings.CLOUDFLARE['ZONE_ID']}/purge_cache"
    send_request = partial(requests.post, url=url, headers=AUTH_HEADERS, timeout=6.0)

    if urls:
        r = send_request(data={"files": urls})
    else:
        r = send_request(data={"purge_everything": True})

    if r.ok and r.data.get("success"):
        return True, "Cache flushed successfully"
    elif r.ok:
        return False, f"Something went wrong. Errors: {' '.join(r.data.get('errors'))}"
    else:
        return False, f"Something went wrong. Status code: {r.status_code}"
