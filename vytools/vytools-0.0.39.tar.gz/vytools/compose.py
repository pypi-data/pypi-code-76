
import vytools.utils as utils
import vytools.stage
from vytools.composerun import run
from vytools.config import CONFIG, ITEMS
import yaml, re, json, os, shutil
import cerberus
import logging
from pathlib import Path

KEYSRULES = '[a-zA-Z0-9_]+'
SCHEMA = utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['compose']},
  'ui':{'type':'string', 'maxlength': 64, 'required': False},
  'subcompose':{'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'name': {'type': 'string', 'maxlength': 64},
        'calibration':{'type': 'dict', 'required':False}
      }
    }
  },
  'anchors':{'type': 'dict','keysrules': {'type': 'string', 'regex': KEYSRULES}}
})
VALIDATE = cerberus.Validator(SCHEMA)

def parse(name, pth, reponame, items=None):
  if items is None: items = vytools.ITEMS
  item = {
    'name':name,
    'thingtype':'compose',
    'repo':reponame,
    'depends_on':[],
    'path':pth
  }
  itemx = {'ui':None, 'subcompose':[], 'anchors':{}}

  with open(pth,'r') as r:
    content = yaml.safe_load(r.read())
    xvy = content.get('x-vy',{})
    itemx.update((k, xvy[k]) for k in itemx.keys() & xvy.keys())
    if itemx['ui'] is None: del itemx['ui']
    item.update(itemx)
  return utils._add_item(item, items, VALIDATE)

ANCHORTHINGTYPES = ['stage','definition']
ANCHORTYPES = ['definition','argument','artifact','stage','directory','file']

def find_all(items, contextpaths=None):
  success = utils.search_all(r'(.+)\.compose\.y[a]*ml', parse, items, contextpaths=contextpaths)
  if success: # process definitions
    for (type_name, item) in items.items():
      if type_name.startswith('compose:'):
        successi = True
        item['depends_on'] = []
        for e in item['anchors']:
          atype = [a for a in ANCHORTYPES if item['anchors'][e].startswith(a+':')]
          if len(atype) == 1 and atype[0] in ANCHORTHINGTYPES: 
            successi &= utils._check_add(item['anchors'][e], atype[0], item, items, type_name)
          elif len(atype) != 1:
            successi = False
            logging.error('Unknown anchor type "{t} {v}" in {n}'.format(t=e,v=item['anchors'][e],n=type_name))
        if 'ui' in item:
          successi &= utils._check_add(item['ui'], 'ui', item, items, type_name)
        for e in item['subcompose']:
          successi &= utils._check_add(e['name'], 'compose', item, items, type_name)
        success &= successi
        if not successi:
          logging.error('Failed to interpret/link compose {c}'.format(c=type_name))
  return success

def build(rootcompose, items=None, build_args=None, built=None, build_level=1, data=None, data_mods=None, eppath=None):
  if items is None: items = ITEMS
  if data is None:
    data = {}
  elif type(data) == str and data in items:
    data = items[data]['data']
  return assemble({'name':rootcompose,'parent_data':data,'data_mods':data_mods},
                        items=items, build_args=build_args, built=built, build_level=build_level, eppath=eppath)

def assemble(assembly, items=None, build_args=None, built=None, build_level=1, eppath=None):
  if items is None: items = ITEMS
  if build_args is None: build_args = {}
  if built is None: built = []
  type_name = assembly['name']
  stage_versions = []
  item = items[type_name]
  name = item['name']
  label = assembly.get('label', type_name.replace('compose:',''))

  cmd = []
  for sa in item['subcompose']:
    build__args = build_args.copy()
    subcompose = sa.copy()
    subcompose['label'] = label + '.'+subcompose['name'].replace('compose:','')
    subcompose['parent_data'] = {}
    subcmds = assemble(subcompose, items=items, build_args=build__args, built=built, build_level=build_level, eppath=eppath)
    if subcmds == False:
      return False
    else:
      cmd += subcmds['command']
      stage_versions += [sv for sv in subcmds['stage_versions'] if sv not in stage_versions]

  anchors = item.get('anchors',{}).copy()
  build__args = build_args.copy()
  ordered = []
  for atype in ANCHORTYPES:
    ordered += [k for k,v in anchors.items() if v.startswith(atype+':')]

  replace_obj = {}
  for tag in ordered: # SORTED TO ENSURE THIS ORDER DEFINITION, ARGUMENT, STAGE, ARTIFACT
    val = anchors[tag]
    if val.startswith('definition:'): # TODO FIX
      replace_obj[tag] = vytools.object.expand(assembly.get('parent_data',{}),
          val, items, data_mods=assembly.get('data_mods',None))
    elif val.startswith('argument:'):
      replace_obj[tag] = val.replace('argument:','',1)
      if tag not in build__args: build__args[tag] = replace_obj[tag]
    elif val.startswith('stage:'):
      tagged = vytools.stage.build([val], items, build__args, built, build_level, jobpath=eppath)
      if tagged == False: return False
      for k,v in tagged.items():
        stage_versions += [sv for sv in v['stage_versions'] if sv not in stage_versions]
      replace_obj[tag] = tagged[val]['tag']
    elif val.startswith('directory:') or val.startswith('file:') or val.startswith('artifact:'):
      splitname = val.split(':',1)
      arttyp = splitname[0]
      artname = splitname[-1]
      if len(splitname) == 2 and len(artname) > 0:
        replace_obj[tag] = artname
        if build_level == -1 and '..' not in artname and eppath and os.path.exists(eppath):
          artifactpath = os.path.join(eppath, artname)
          if arttyp in ['artifact','file']:
            with open(artifactpath,'w') as w: w.write('')
            os.chmod(artifactpath, 0o666)
          elif arttyp == 'directory':
            os.makedirs(artifactpath,exist_ok=True)

  if build_level == -1:
    compose_file_name = label + '.yaml'
    if _replace_and_write_values(compose_file_name, eppath, item['path'], replace_obj):
      cmd = cmd + ['-f',compose_file_name]
    else:
      return False

  return {'command':cmd,'stage_versions':stage_versions}

def _prefx(key,char,replkeys):
  return [r for r in replkeys if key.startswith(r+char)]

def stripkey(key):
  if key.startswith('$'):
    key = key[1:]
    if key.startswith('{'):
      key = ''.join(key[1:].split('}',1))
  return key

def _replkeysf(k, key, obj, repl, eppath):
  replkeys = [str(i) for i in len(repl)] if type(repl) == list else \
    (repl.keys() if type(repl) == dict else [])
  if key in replkeys:
    obj[k] = repl[key]
  else:
    for x in ['.','>']:
      prefx = _prefx(key,x,replkeys)
      if len(prefx) == 1:
        repl_ = repl[prefx[0]]
        key_ = stripkey(key.replace(prefx[0]+x,'',1))
        if x == '.':
          _replkeysf(k, key_, obj, repl_, eppath)
        elif x == '>' and eppath and os.path.exists(eppath):
          with open(os.path.join(eppath, key_),'w') as w:
            if key.endswith('.json'):
              w.write(json.dumps(repl_))
            elif key.endswith('.yaml'):
              w.write(yaml.safe_dump(repl_))
          obj[k] = key_

def _recursiv_replace(obj, repl, eppath):
  if type(obj) == dict:
    ks = obj.keys()
  elif type(obj) == list:
    ks = range(len(obj))
  else:
    return
  for k in ks:
    key = obj[k]
    if type(key) == str and key.startswith('$'):
      key = stripkey(key)
      _replkeysf(k, key, obj, repl, eppath)
    elif type(key) in [list,dict]:
      _recursiv_replace(obj[k], repl, eppath)
      
def _replace_and_write_values(compose_file_name, eppath, compose_pth, replace_obj):
  if '..' not in compose_file_name and eppath and os.path.exists(eppath):
    cfile = os.path.join(eppath, compose_file_name)
    if not bool(replace_obj):
      shutil.copyfile(compose_pth, cfile)
      return True
    composition = {}
    with open(compose_pth,'r') as r:
      composition = yaml.safe_load(r.read())
    if 'x-vy' in composition: del composition['x-vy']
    _recursiv_replace(composition, replace_obj, eppath)
    with open(cfile,'w') as w:
      w.write(yaml.safe_dump(composition))
    return True
  return False

def artifact_paths(compose_name, items, eppath):
  artifacts = {}
  def get_artifacts(i,artifacts):
    if i in items:
      for tag,val in items[i].get('anchors',{}).items():
        pth = os.path.join(eppath,val.replace('artifact:','',1))
        if val.startswith('artifact:') and '..' not in val and os.path.exists(pth):
          artifacts[tag] = pth
      for sa in items[i]['subcompose']: get_artifacts(sa['name'],artifacts)
  if eppath and os.path.exists(eppath):
    get_artifacts(compose_name,artifacts)
  return artifacts
