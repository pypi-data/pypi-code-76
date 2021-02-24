# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_limiter']

package_data = \
{'': ['*']}

install_requires = \
['aioredis', 'fastapi']

setup_kwargs = {
    'name': 'fastapi-limiter',
    'version': '0.1.2',
    'description': 'A request rate limiter for fastapi',
    'long_description': '# fastapi-limiter\n\n[![pypi](https://img.shields.io/pypi/v/fastapi-limiter.svg?style=flat)](https://pypi.python.org/pypi/fastapi-limiter)\n[![license](https://img.shields.io/github/license/long2ice/fastapi-limiter)](https://github.com/long2ice/fastapi-limiter/blob/master/LICENCE)\n[![workflows](https://github.com/long2ice/fastapi-limiter/workflows/pypi/badge.svg)](https://github.com/long2ice/fastapi-limiter/actions?query=workflow:pypi)\n[![workflows](https://github.com/long2ice/fastapi-limiter/workflows/ci/badge.svg)](https://github.com/long2ice/fastapi-limiter/actions?query=workflow:ci)\n\n## Introduction\n\nFastAPI-Limiter is a rate limiting tool for [fastapi](https://github.com/tiangolo/fastapi) routes.\n\n## Requirements\n\n- [redis](https://redis.io/)\n\n## Install\n\nJust install from pypi\n\n```shell script\n> pip install fastapi-limiter\n```\n\n## Quick Start\n\nFastAPI-Limiter is simple to use, which just provide a dependency `RateLimiter`, the following example allow `2` times request per `5` seconds in route `/`.\n\n```py\nimport aioredis\nimport uvicorn\nfrom fastapi import Depends, FastAPI\n\nfrom fastapi_limiter import FastAPILimiter\nfrom fastapi_limiter.depends import RateLimiter\n\napp = FastAPI()\n\n\n@app.on_event("startup")\nasync def startup():\n    redis = await aioredis.create_redis_pool("redis://localhost")\n    FastAPILimiter.init(redis)\n\n\n@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])\nasync def index():\n    return {"msg": "Hello World"}\n\n\nif __name__ == "__main__":\n    uvicorn.run("main:app", debug=True, reload=True)\n```\n\n## Usage\n\nThere are some config in `FastAPILimiter.init`.\n\n### redis\n\nThe `redis` instance of `aioredis`.\n\n### prefix\n\nPrefix of redis key.\n\n### identifier\n\nIdentifier of route limit, default is `ip`, you can override it such as `userid` and so on.\n\n```py\nasync def default_identifier(request: Request):\n    forwarded = request.headers.get("X-Forwarded-For")\n    if forwarded:\n        return forwarded.split(",")[0]\n    return request.client.host\n```\n\n### callback\n\nCallback when access is forbidden, default is raise `HTTPException` with `429` status code.\n\n```py\nasync def default_callback(request: Request, expire: int):\n    """\n    default callback when too many requests\n    :param request:\n    :param expire: The remaining seconds\n    :return:\n    """\n    raise HTTPException(\n        HTTP_429_TOO_MANY_REQUESTS, "Too Many Requests", headers={"Retry-After": str(expire)}\n    )\n```\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/long2ice/fastapi-limiter/blob/master/LICENCE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/fastapi-limiter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
