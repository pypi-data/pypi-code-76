#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' A command-line SIDEX server.

This file provides a command-line SIDEX server.
A detailed usage is available by typing the following command:

   python -m sidex.server -h
'''
from . setup import setup


if __name__ == '__main__':
  from argparse import ArgumentParser as ap
  import logging
  parser = ap(prog='server', description='sidex server process')
  parser.add_argument('target', type=str,
    help='target directory')
  parser.add_argument(
    '--host', dest='host', metavar='host', type=str, default='0.0.0.0',
    help='set server hostname')
  parser.add_argument(
    '--port', dest='port', metavar='port', type=int, default=8080,
    help='set server port number')
  parser.add_argument(
    '--get-token', dest='get_token', metavar='token', type=str,
    help='limit get function by setting token')
  parser.add_argument(
    '--put-token', dest='put_token', metavar='token', type=str,
    help='enable put function by setting token')
  parser.add_argument(
    '--delete-token', dest='delete_token', metavar='token', type=str,
    help='enable delete function by setting token.')
  parser.add_argument(
    '--subdir', dest='subdir', metavar='subdir', type=str,
    help='set subdirectory')
  parser.add_argument(
    '--debug', dest='debug', action='store_true',
    help='enable debug messages')

  args = parser.parse_args()

  log_level = 'DEBUG' if args.debug else 'INFO'
  log_handler = logging.StreamHandler()
  log_handler.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'))

  server = setup(
    args.target, subdir=args.subdir,
    get_token=args.get_token, put_token=args.put_token,
    delete_token=args.delete_token,
    log_handler=log_handler, log_level=log_level)
  server.run(host=args.host, port=args.port, threaded=True, debug=args.debug)
