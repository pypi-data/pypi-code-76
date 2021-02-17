import os, re, logging, copy, subprocess, re
from termcolor import cprint
from vytools.config import CONFIG, SEARCHED_REPO_PATHS
from pathlib import Path, PurePath
from cerberus import Validator
INFOCOLOR = 'cyan'
SUCCESSCOLOR = 'green'
FAILCOLOR = 'red'

def print_info(*argv):
  cprint(' '.join(argv),INFOCOLOR)

def print_success(*argv):
  cprint(' '.join(argv),SUCCESSCOLOR)

def print_fail(*argv):
  cprint(' '.join(argv),FAILCOLOR)


BASE_DATA_TYPES = {'float32':0,'float64':0,'uint64':0,
  'int64':0,'uint32':0,'int32':0,'uint16':0,'int16':0,'uint8':0,
  'int8':0,'string':'','bool':False,'byte':0,'char':''}

BASE_SCHEMA = {
  'path': {'type':'string', 'maxlength': 1024},
  'name': {'type':'string', 'maxlength': 64},
  'depends_on':{'type':'list','schema': {'type': 'string', 'maxlength':64}},
  'sources':{'type':'dict'},
  'repo':{'type':'string', 'maxlength': 64}
}

REPO_SCHEMA = BASE_SCHEMA.copy()
REPO_SCHEMA.update({
  'source': {'type':'string', 'maxlength': 32},
  'account': {'type':'string', 'maxlength': 32},
  'reponame': {'type':'string', 'maxlength': 128},
  'url': {'type':'string', 'maxlength': 512},
  'type': {'type':'string', 'allowed': ['git','hg']},
})

def repo_version(typ, pth):
  try:
    if typ == 'hg':
      return subprocess.check_output(['hg','--cwd',pth,'id','-i']).decode('ascii').strip()  # unfortunately THIS CHANGES FILES IN THE .Hg folder
    elif typ == 'git':
      hash_ = subprocess.check_output(['git','-C',pth,'rev-parse','HEAD']).decode('ascii').strip()
      changes = subprocess.check_output(['git','-C',pth,'status','--porcelain']).decode('ascii').strip()
      hash_ += '+' if len(changes) > 0 else ''
      return hash_ #subprocess.check_output(['git','-C',pth,'rev-parse','HEAD']).decode('ascii').strip()
    else:
      return '-'
  except Exception as exc:
    logging.error('Failed to get hash of repo: '+str(exc))
    return '-'

def parse_repo(pth, items):
  if pth in SEARCHED_REPO_PATHS: return SEARCHED_REPO_PATHS[pth]
  SEARCHED_REPO_PATHS[pth] = False

  if os.path.exists(os.path.join(pth,'.git')): # Can be directory or file so use exists
    typ = 'git'
    options = ['origin','remote'] # to do more here
    cmdprefx = ['git','-C',pth,'config','--get']
  elif os.path.isdir(os.path.join(pth,'.hg')):
    typ = 'hg'
    options = ['default'] # to do more here
    cmdprefx = ['hg','--cwd',pth,'paths']
  else:
    return SEARCHED_REPO_PATHS[pth]

  s = {'type':typ,'path':pth,'depends_on':[],'version':'','thingtype':'repo'}
  url = None
  for o in options: 
    try:
      cmd = cmdprefx + ['remote.{o}.url'.format(o=o) if typ == 'git' else o]
      url = subprocess.check_output(cmd).decode('utf-8').strip()
      if len(url) > 0: break
    except Exception as exc:
      pass
  if not url:
    logging.error('Failed to parse repository at {p}'.format(p=pth))
    return SEARCHED_REPO_PATHS[pth]

  # e.g.
  # git@bitbucket.org:account/name.git
  # https://username@bitbucket.org/account/name.git
  # https://github.com/account/name.git
  # git@github.com:account/name.git
  s['url'] = url
  urlparts = url.split('@',1)[-1]
  urlparts = re.split('/|:',urlparts)
  if len(urlparts) < 3:
    logging.error('Failed to parse url "{u}" for repository at {p}'.format(u=url,p=pth))
    return SEARCHED_REPO_PATHS[pth]

  s['source'] = urlparts[0]
  s['account'] = urlparts[1]
  s['reponame'] = urlparts[2].replace('.git','').replace('.hg','')
  name_root = s['account']+'|'+s['reponame']
  name = name_root
  count = 0
  while 'repo:'+name in items:
    name = name_root+'|'+str(count)
    count += 1
  s['repo'] = 'repo:'+name
  s['name'] = name
  items['repo:'+name] = s
  SEARCHED_REPO_PATHS[pth] = True
  return SEARCHED_REPO_PATHS[pth]

def repo_version_string(repo, version=None):
  if version == None:
    version = repo_version(repo['type'], repo['path'])
  return repo['type'] + '|' + repo['source'] + '|' + repo['name'] + '|' + version

def get_repo_versions(lst, items, build_args=None):
  repo_versions = {}
  def get_version(name):
    if name in items:
      item = items[name]
      if len(item['repo']) > 0 and item['repo'] in items and item['repo'] not in repo_versions:
        repo_versions[item['repo']] = repo_version_string(items[item['repo']])
      for d in item['depends_on']: get_version(d)
  for l in lst: get_version(l)
  return repo_versions

def ui_search(rootpath, vydir, func, items):
  for root, dirs, files in os.walk(rootpath, topdown=True):
    for f in files:
      if f != 'vydirectory':
        pth = os.path.join(root,f)
        name = os.path.join('/vy', vydir, str(PurePath(pth).relative_to(rootpath)))
        func(name, pth, '', items)

def get_repository_paths(rep_str_lst, contextpaths=None):
  sp = contextpaths if contextpaths else CONFIG.get('contexts')
  items = {}
  newcp = []
  success = True
  search_all(None, None, items, contextpaths=sp, find_repos_only=True)
  repo_versions = get_repo_versions([i for i in items],items)
  print('Found repositories:')
  for item in repo_versions.values(): print('  ',item)
  for r in rep_str_lst:
    found = False
    for i,item in repo_versions.items():
      found = item.startswith(r)
      if found:
        newcp.append(items[i]['path'])
        break
    if not found:
      success = False
      logging.error('Failed to find repository matching {n} in the searched directories {p}'.format(n=r,p=','.join(sp)))
  SEARCHED_REPO_PATHS.clear()
  return (success, newcp)

def search_all(fname_regex, func, items, is_ui=False, contextpaths=None, find_repos_only=False):
  if contextpaths is None: contextpaths = CONFIG.get('contexts')
  success = False
  if contextpaths:
    success = True
    exclude = set(['.vy','.git','.hg'])
    for cp in contextpaths:
      for root, dirs, files in os.walk(cp, topdown=True):
        if '.vyignore' in files:
          dirs[:] = []
          continue
        isrepo = parse_repo(root, items)
        dirs[:] = [d for d in dirs if d not in exclude]
        if isrepo and find_repos_only:
          dirs[:] = []
          continue
        if is_ui and func:
          if 'vydirectory' in files:
            vydir = Path(os.path.join(root,'vydirectory')).read_text().strip()
            ui_search(root, vydir, func, items)
        elif fname_regex and func:
          for f in files:
            m = re.match(fname_regex,f,re.I)
            if m:
              success &= func(m.group(1), os.path.join(root, f), '', items)
  return success

def topological_sort(source):
    pending = [(name, set(deps)) for name, deps in source]        
    emitted = []
    while pending:
      next_pending = []
      next_emitted = []
      for entry in pending:
        name, deps = entry
        deps.difference_update(set((name,)), emitted)
        if deps:
          next_pending.append(entry)
        else:
          yield name
          emitted.append(name)
          next_emitted.append(name)
      if not next_emitted:
        raise ValueError("cyclic dependancy detected {n}".format(n=name))
      pending = next_pending
      emitted = next_emitted
    return emitted

def exists(lst, items, pad=''):
  success = True
  for l in lst:
    if l not in items:
      success = False
      logging.error('"{n}" was not found {p}'.format(n=l,p=pad))
    else:
      success &= exists(items[l]['depends_on'],items,'(depended on by {})'.format(l))
  return success

def sort(lst, items):
  return [x for x in topological_sort([(k,set(items[k]['depends_on'])) for k in lst])]

def _check_add(nme, typ, item, items, type_name):
  if nme.startswith(typ+':') and nme in items:
    item['depends_on'].append(nme)
    return True
  logging.error('Failed to find subitem "{n}" referenced by "{tn}".\n  - "{n}" is not of type {t} or does not exist'.format(n=nme, t=typ, tn=type_name))
  return False

def _add_item(item, items, validate):
  typ = item['thingtype']
  name = item['name']
  pth = item['path']
  tname = typ+':'+name
  if tname in items:
    pthp = items[tname]['path']
    logging.error('"{t}" at "{p}" was not loaded because a same name item was already loaded from {p2}' \
                  .format(t=tname, p=pth, p2=pthp))
    return False
  elif validate==True or validate.validate(item):
    items[tname] = item
    return True
  else:
    logging.error('"{n}" at "{p}" failed validation {s}'.format(n=tname, p=pth, s=validate.errors))
    return False
