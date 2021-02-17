#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' A command-line SIDEX client for dump.

This file provides a command-line SIDEX client.
A detailed usage is available by typing the following command:

   python -m sidex.dump -h
'''

import os, sys, re, logging, requests
import io, gzip, bz2, lzma, tarfile


if __name__ == '__main__':
  from argparse import ArgumentParser as ap
  parser = ap(prog='dump', description='SIDEX dump client')
  parser.add_argument('target', type=str,
    help='address to SIDEX server')
  parser.add_argument('filename', type=str, nargs='+',
    help='requested filename')
  parser.add_argument(
    '-f', '--overwrite', dest='overwrite', action='store_true',
    help='overwrite files even if exists')
  parser.add_argument(
    '--tar', dest='tarball', type=str, action='store',
    help='grab files as a tarball archive')
  parser.add_argument(
    '--token', dest='token', metavar='token', type=str,
    help='set token')

  args = parser.parse_args()
  ## Leading "http://" can be omitted.
  if not re.match('^https?://',args.target):
    args.target = 'http://' + args.target
  eprint = lambda s: print('error: '+s, file=sys.stderr)

  method = 'dump'
  filename = os.path.basename(args.target)

  if not args.overwrite:
    if any([os.path.exists(f) for f in args.filename]):
      eprint('file "{}" already exists.'.format(f))
      exit(1)

  try:
    data = {
      'method': 'dump',
      'token': args.token,
      'filename': args.filename,
    }
    with requests.post(args.target, data=data, stream=True) as req:
      if req.ok is False:
        eprint(req.text.strip())
        req.raise_for_status()

      if args.tarball:
        dummy,ext = os.path.splitext(args.tarball)
        print(ext)
        if ext == '.gz':
          with gzip.open(args.tarball, 'wb') as arv:
            for chunk in req.iter_content(65535): arv.write(chunk)
        elif ext == '.bz2':
          with bz2.open(args.tarball, 'wb') as arv:
            for chunk in req.iter_content(65535): arv.write(chunk)
        elif ext == '.xz':
          with lzma.open(args.tarball, 'wb') as arv:
            for chunk in req.iter_content(65535): arv.write(chunk)
        else:
          with open(args.tarball, 'wb') as arv:
            for chunk in req.iter_content(65535): arv.write(chunk)
      else:
        buf = io.BytesIO(req.content)
        with tarfile.open(fileobj=buf, mode='r:') as arv:
          arv.extractall()
  except Exception as e:
    eprint(str(e))
    exit(1)
