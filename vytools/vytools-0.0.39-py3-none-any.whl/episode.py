
import vytools.utils
import vytools.compose
import vytools.definition
import vytools.object
import vytools.composerun
from termcolor import cprint
from pathlib import Path
from vytools.config import CONFIG, ITEMS
import re, json, shutil, os, yaml, subprocess, sys, io
import signal
import cerberus
import logging

SCHEMA = vytools.utils.BASE_SCHEMA.copy()

INHERIT_ITEMS = {
  'tags':{'type':'list', 'required': False, 'schema': {'type': 'string', 'maxlength':64}},
  'expectation':{'type':'boolean', 'required': False},
}


SCHEMA.update(INHERIT_ITEMS)
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['episode']},
  'compose':{'type':'string', 'maxlength': 64},
  'data':{'type': 'string', 'maxlength': 64},
  'data_mods':{'type': 'dict', 'required': False},
  'passed':{'type':'boolean', 'required': False},
  'arguments':{'type': 'dict', 'required': False, 'keysrules': {'type': 'string', 'regex': vytools.compose.KEYSRULES}},
  'repos':{'type':'list', 'required': False, 'schema':{'type':'string','maxlength':1024}},
  'stage_repos':{'type':'list', 'required': False, 'schema':{'type':'string','maxlength':1024}}
})
VALIDATE = cerberus.Validator(SCHEMA)

def parse(name, pth, reponame, items):
  item = {
    'name':name,
    'repo':reponame,
    'thingtype':'episode',
    'path':pth
  }
  type_name = 'episode:' + name
  item['depends_on'] = []
  try:
    content = json.load(io.open(pth, 'r', encoding='utf-8-sig'))
    for sc in SCHEMA:
      if sc in content and sc not in ['repos']:
        item[sc] = content[sc]
    vytools.utils._check_add(item['compose'], 'compose', item, items, type_name)
    vytools.utils._check_add(item['data'], 'object', item, items, type_name)
    return vytools.utils._add_item(item, items, VALIDATE)
  except Exception as exc:
    logging.error('Failed to parse episode "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

def find_all(items, contextpaths=None):
  return vytools.utils.search_all(r'(.+)\.episode\.json', parse, items, contextpaths=contextpaths)

def get_build_args(episode, build_arg_dict=None):
  if build_arg_dict is None: build_arg_dict = {}
  build_args = episode.get('arguments',{})
  build_args.update(build_arg_dict)
  return build_args

def build(type_name, built, items=None, build_args=None, build_level=0, data=None, data_mods=None, eppath=None):
  if items is None: items = ITEMS
  item = items[type_name]
  build__args = get_build_args(item, build_args)
  rootcompose = item['compose']
  objdata = item['data']
  if data is None:
    data = items[objdata]['data'] if objdata in items else {}
  return vytools.compose.build(rootcompose, items=items, build_args=build__args, built=built, 
                        build_level=build_level, data=data, data_mods=data_mods, eppath=eppath)

def get_episode_id(episode):
  return None if '..' in episode['name'] else episode['name'].lower()

def artifact_paths(episode_name, items=None, jobpath=None):
  if items is None: items = ITEMS
  if episode_name not in items: return {}
  episode = items[episode_name]
  epid = get_episode_id(episode)
  eppath = vytools.composerun.runpath(epid,jobpath=jobpath)
  return vytools.compose.artifact_paths(episode['compose'], items, eppath=eppath)

def run(type_name, items=None, build_args=None, clean=False, data=None, data_mods=None, jobpath=None):
  if items is None: items = ITEMS
  if type_name not in items: return False
  episode = items[type_name]
  epid = get_episode_id(episode)
  eppath = vytools.composerun.runpath(epid,jobpath=jobpath)
  if epid is None or eppath is None: return False
  build__args = get_build_args(episode, build_args)
  if data is None: data = episode['data']
  compose_name = episode['compose']
  results = vytools.composerun.run(epid, compose_name, 
    items=items, build_args=build__args, clean=clean, 
    data=data, data_mods=data_mods, jobpath=jobpath,
    dont_track=episode['repo'])

  if results and eppath and os.path.exists(eppath):
    # artifacts = vytools.compose.artifact_paths(compose_name, items, eppath=eppath)
    for x in INHERIT_ITEMS:
      if x in episode: results[x] = episode[x]
    with open(os.path.join(eppath, episode['name']+'.episode_.json'),'w') as w2:
      w2.write(json.dumps(results))
  return results

