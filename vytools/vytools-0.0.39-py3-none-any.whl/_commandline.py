#!/usr/bin/env python3
import argparse, sys, os, json, argcomplete, re
import vytools

import logging
logging.basicConfig(level=logging.INFO)

TLIST = '(definition, object, ui, stage, compose, episode)'

def add_all(parser):
  parser.add_argument('--all', action='store_true', 
                      help='If present, rebuild all dependent stages.'
                            'Otherwise only rebuild top level and missing stages')

def make_parser():
  parser = argparse.ArgumentParser(prog='vytools', description='tools for working with vy')
  parser.add_argument('--version','-v', action='store_true', 
    help='Print vytools version')
  parser.add_argument('--contexts', type=str, default='',
    help='Comma or semi-colon delimited list of paths to context folders')
  parser.add_argument('--secrets', type=str, required=False, 
    help='Comma or semi-colon delimited list of paths to secrets files')
  parser.add_argument('--jobs', type=str, required=False, 
    help='Path to jobs folder. All jobs will be written to this folder.')
  parser.add_argument('--arg','-a', metavar='KEY=VALUE', action = 'append',
                      help="Set a key-value pairs "
                            "(do not put spaces before or after the = sign). "
                            "If a value contains spaces, you should define "
                            "it with double quotes: "
                            'foo="this is a sentence". Note that '
                            "values are always treated as strings.")      
  parser.add_argument('--name','-n', action='append', choices=vytools.CONFIG.get('items'),
    help='Name of thing '+TLIST+' to find episodes for')

  subparsers = parser.add_subparsers(help='specify action', dest='action')

  build_sub_parser = subparsers.add_parser('build',
    help='Build docker images that are dependent on named items')
  add_all(build_sub_parser)

  info_sub_parser = subparsers.add_parser('info',
    help='Print things '+TLIST)
  info_sub_parser.add_argument('--dependencies','-d', action='store_true', 
    help='List dependencies of items')
  info_sub_parser.add_argument('--expand','-e', action='store_true', 
    help='Expand items')

  server_sub_parser = subparsers.add_parser('server',help='Run ui server')

  run_sub_parser = subparsers.add_parser('run',
    help='Run specified episodes')
  run_sub_parser.add_argument('--build', action='store_true', 
    help='If present, build dependent stages (also note --all flag).')
  add_all(run_sub_parser)
  run_sub_parser.add_argument('--clean', action='store_true', 
    help='Clean episode folders before running')
  run_sub_parser.add_argument('--data_mods', type=str, required=False, 
    help='Data mods')

  return parser

def parse_key_value(kv,typ):
  args = {}
  success = True
  if kv:
    for arg in kv:
      if '=' not in arg:
        success = False
        logging.error('A {s} ({a}) failed to be in the form KEY=VALUE'.format(s=typ,a=arg))
      else:
        (k,v) = arg.split('=',1)
        args[k] = v
  return (success, args)

def parse_build_args(ba):
  return parse_key_value(ba,'argument (--arg, -a)')

def parse_data_mods(args):
  if 'data_mods' in dir(args) and args.data_mods:
    try:
      return json.loads(args.data_mods)
    except Exception as exc:
      logging.error('Failed to parse input datamods:'+str(exc))
      return False
  else:
    return None

def main():
  parser = make_parser()
  argcomplete.autocomplete(parser)
  args = parser.parse_args()
  if args.version:
    print(vytools.__version__)
    return

  if args.secrets: vytools.CONFIG.set('secrets', re.split(';|,',args.secrets))
  if args.contexts: vytools.CONFIG.set('contexts', re.split(';|,',args.contexts))
  if args.jobs: vytools.CONFIG.set('jobs',args.jobs)
  if not vytools.CONFIG.get('contexts'):
    logging.error('The vy context(s) has not been initialized. Please provide a --contexts')
    return
  ignore_success = vytools.scan()

  lst = [n for n in args.name] if 'name' in dir(args) and args.name else []
  ba = None if 'arg' not in dir(args) else args.arg
  success, build_args = parse_build_args(ba)
  if not success: return
  build_level = 1 if 'all' in dir(args) and args.all else 0

  if args.action == 'build':
    return bool(vytools.build(lst, build_args=build_args, build_level=build_level))
  elif args.action == 'run':
    data_mods = parse_data_mods(args)
    if data_mods == False:
      return False
    if args.build:
      br = vytools.build(lst, build_args=build_args, build_level=build_level)
      if br == False: return False
    return bool(vytools.run(lst, build_args=build_args, clean=args.clean, data_mods=data_mods))
  elif args.action == 'info':
    vytools.info(lst, list_dependencies=args.dependencies, expand=args.expand)
  elif args.action == 'server':
    vytools.server()
  else:
    return False
