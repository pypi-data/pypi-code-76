#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' A function for a quick access to a sidex server.

This module provides a helper function `sidex_request` to make
a query to a sidex server.
'''
import requests


def request(url,method,filename=None,token=None):
  '''
  Make a request to a sidex server.

  Args:
    url (str):
        The url, which defines a query to a sidex server.
    method (str):
        The name of the requested method. The available methods
        are `get`, `put`, and `delete`.
    filename (str, optional):
        A filename to be uploaded to a sidex server. This
        argument is only required in the 'put' method.
    token (str, optional):
        A token string passed to a sidex server. This argument will
        be ignored when the server is not protecte by token.

  Returns:
    requests.Response:
        A response from a sidex server.
  '''
  method = 'get'
  basename = os.path.basename(url)

  if method not in ('get','put','delete'):
    raise RuntimeError('invalid method.')
  if method == 'put' and filename is None:
    raise RuntimeError('upload file is not specified.')
  data = { 'method': method, 'token': token }

  if method == 'get':
    if os.path.exists(filename):
      raise RuntimeError('file "{}" already exists'.format(filename))
    return requests.post(url, data=data)
  elif method == 'put':
    with open(args.filename,'rb') as f:
      files = { 'payload': f.read(), }
    return requests.post(url, data=data, files=files)
  elif method == 'delete':
    return requests.post(url, data=data)
