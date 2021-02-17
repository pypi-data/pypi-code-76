#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Simple Data Exchange Server

This module provides a minimal framework to launch a file server
running on the middleware `Flask`. You are allowed to fetch, put,
and delete files over HTTP.

You can launch a server on the command line as follows:

    python -m sidex.server --host localhost --port 8000 TARGET_DIR

A file in the TARGET_DIR can be fetched by `wget`:

    wget --post-data="method=get" http://localhost:8000/FILENAME

or by using `sidex.client`:

    python -m sidex.client http://localhost:8080/FILENAME

The `POST` method is required since the `method` data is mandatory.
The `get` method can be protected by setting a token.

The `put` and `delete` methods are disabled by default. They can be
enabled by setting tokens. Note that the token is just a passphrase
and not ciphered at all. The transaction is never protected. Do not
use the SIDEX in case that the network is untrastrul.

The SIDEX provides a way to customize the functions. The default
behaviors of any methods can be overridden.
'''

from . setup import setup
from . request import request
