#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' A command-line SIDEX client.

This file provides a command-line SIDEX client.
A detailed usage is available by typing the following command:

   python -m sidex.client -h
'''

import os, sys, re, logging, requests


if __name__ == '__main__':
  from argparse import ArgumentParser as ap
  parser = ap(prog='client', description='SIDEX minimal client')
  parser.add_argument('filename', type=str, nargs='?',
    help='filename to be uploaded (only requred in put mode)')
  parser.add_argument('target', type=str,
    help='address to SIDEX server')
  parser.add_argument(
    '-d', '--delete', dest='delete', action='store_true',
    help='delete file')
  parser.add_argument(
    '--token', dest='token', metavar='token', type=str,
    help='set token')

  args = parser.parse_args()
  ## Leading "http://" can be omitted.
  if not re.match('^https?://',args.target):
    args.target = 'http://' + args.target
  eprint = lambda s: print('error: '+s, file=sys.stderr)

  if args.delete is True and args.filename is not None:
    eprint('option conflicted.')
    exit(1)

  method = 'get'
  filename = os.path.basename(args.target)

  if args.delete is True:
    method = 'delete'
  if args.filename is not None:
    method = 'put'
    with open(args.filename,'rb') as f:
      files = { 'payload': f.read(), }
  else:
    files = None

  if method == 'get' and os.path.exists(filename):
    eprint('file "{}" already exists.'.format(filename))
    exit(1)

  try:
    data = { 'method': method, 'token': args.token }
    req = requests.post(args.target, data=data, files=files)
    if req.ok is False:
      eprint(req.text.strip())
      req.raise_for_status()

    if method == 'get':
      with open(filename, 'wb') as f:
        f.write(req.content)
    else:
      print(req.text.strip())
  except Exception as e:
    eprint(str(e))
    exit(1)
