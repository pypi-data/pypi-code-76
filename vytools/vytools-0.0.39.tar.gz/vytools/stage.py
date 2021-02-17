import os, re, logging, json, subprocess, copy, time
import vytools.utils as utils
from vytools.config import CONFIG
from pathlib import Path
import cerberus

#todo NOT SURE THIS IS THE RIGHT REGEX
COPY_STAGE_A = re.compile(r'^copy[\s]+--from=[\'"]?([\w-]+)',re.I | re.M)
COPY_STAGE_B = re.compile(r'^from[\s]+([\w\-:\.\/]+)',re.I | re.M)
COPY_REPO = re.compile(r'^copy[\s]+[\'"]?([\w-]+)',re.I | re.M)

SCHEMA = utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['stage']},
  'build_context':{'type':'string', 'maxlength': 1024},
  'secrets':{'type':'list','schema': {'type': 'string', 'maxlength':64}},
  'args':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'key': {'type': 'string', 'maxlength': 64},
        'value': {'type': 'string', 'maxlength': 64}
      }
    }
  }
})

VALIDATE = cerberus.Validator(SCHEMA)

def get_repo_info(name):
  return {'type':'git','source':'bitbucket','account':'autonomoussolutions','name':name}

def line_before_escape(line):
  return re.split(r'([^\\]#)',line)[0]      # All characters before unescaped # (comments)

def remove_quotes(line):
  if line.startswith('"') and line.endswith('"'):
    return line.strip('"')
  elif line.startswith("'") and line.endswith("'"):
    return line.strip("'")
  else:
    return line

def dependencies(stage_text,stage_sources):
  dependency = []
  args = []
  started = False
  for linex in stage_text.splitlines(): # TODO would be nice to preserve backslash continuation lines as one line
    line = linex.strip()
    if line.startswith('#'): continue         # need this
    line = line_before_escape(line)           # All characters before unescaped # (comments)
    m = re.match(COPY_STAGE_A, line)
    if not m:
      m = re.match(COPY_STAGE_B, line)
      if m: started = True
    if m and 'stage:'+m.group(1) not in dependency:  # COPY/FROM STAGE
      sn = m.group(1)
      stage_sources[sn] = '?' if sn not in stage_sources else stage_sources[sn]
      if stage_sources[sn] != '':
        dependency.append('stage:'+m.group(1))  # add dependency
    if started: # For multistage builds only get args AFTER FROM (only these will work)
      m = re.match(r'^[\s]*arg[\s]+(.+)',line,re.I)
      if m:
        argline = line_before_escape(m.group(1)).split('=',1)
        argkey = argline[0].strip()
        argval = argline[1].strip() if len(argline) > 1 else ''
        if argkey not in [a['key'] for a in args]:
          args.append({'key':argkey, 'value':remove_quotes(argval)}) 
  return (dependency, args)

def parse(namein, pth, reponame, items):
  name = namein.lower() # Stages must be unique case insensitively
  with open(pth,'r') as r:
    stage_text = r.read()
  secrets = []
  build_context = '.'
  sources = {}
  for line in stage_text.splitlines():
    m = re.search(r'^#vy(.+)', line, re.I | re.M)
    if m:
      try:
        obj = json.loads(m.group(1))
        build_context = obj.get('context',build_context)
        sources.update(obj.get('source',{}))
      except Exception as exc:
        logging.error('Failed to read potential vy json comment ({c}) in "{p}"'.format(c=m.group(1), p=pth))
        return False
    m = re.search(r'--mount=type=secret(.+)',line,re.I | re.M)
    if m:
      m = re.search(r'id=([^\s]+)',m.group(1),re.I | re.M)
      if m and m.group(1) not in secrets:
        secrets.append(m.group(1))
  type_name = 'stage:'+name
  if os.path.isabs(build_context):
    logging.error('Stage build contexts should be relative paths "{p}"'.format(p=build_context))
    return False
  else:
    try:
      build_context = Path(os.path.join(os.path.dirname(pth),build_context)).resolve()
      # TODO make sure this is in the right repository
      #      If the build context of the stage goes up above the repo directory this will be wrong
    except Exception as exc:
      logging.error('Stage build context "{p}" for stage {n} may not be a directory'.format(p=build_context,n=name))
      return False
    (dependency,args) = dependencies(stage_text,sources)
    item = {'name':name,
      'thingtype':'stage',
      'path':pth,
      'repo':reponame,
      'args':args,
      'secrets':secrets,
      'build_context':str(build_context),
      'sources':sources,
      'depends_on':dependency
    }
    return utils._add_item(item, items, VALIDATE)

TAGSAFE = lambda v : re.sub(r'[^a-zA-Z0-9\-\_]','_',v)
ARGTAG = lambda k,a : TAGSAFE(k) + '.' + TAGSAFE(a[k])
def taglist(_stage_name_, items):
  stage = items[_stage_name_]
  my_dep_args = [sa['key'] for sa in stage['args']]
  for s in stage['depends_on']:
    my_dep_args += [a for a in taglist(s, items) if a not in my_dep_args]
  return my_dep_args

def stage_args(stage_name, items, build_arg_dict=None):
  if build_arg_dict is None: build_arg_dict = {}
  my_dep_args = taglist(stage_name, items)
  this_args = {}
  for key in my_dep_args:
    if key in build_arg_dict:
      this_args[key] = build_arg_dict[key]
    else:
      logging.error('Building {s} requires setting build argument "{b}"'.format(s=stage_name,b=key))
      return False
  return this_args

def stage_prefix(stage_name):
  return 'vy__' + stage_name.replace('stage:','',1).lower()

def stages(stage_item):
  cmd = ['docker','images','--filter=reference=' + stage_prefix(stage_item) + ':*','--format','{{.Repository}}:{{.Tag}}']
  return subprocess.check_output(cmd).decode('utf-8').strip().split()

def stage_tag(stage_name, items, build_arg_dict=None):
  this_args = stage_args(stage_name, items, build_arg_dict)
  if this_args == False: return (False,False)
  keys = list(this_args.keys())
  keys.sort()
  lst = [ARGTAG(key, this_args) for key in keys]
  tag = stage_prefix(stage_name) + (':' + '.'.join(lst) if len(lst) > 0 else ':latest')
  return (tag, this_args)

def get_built_stage_repos(tag):
  cmd = ['docker', 'inspect', '--format', '\'{{ index .Config.Labels "tools.vy.repos"}}\'', tag]
  try:
    vyreposi = subprocess.check_output(cmd).decode('utf-8').strip().strip("'")
    return [] if len(vyreposi) == 0 else vyreposi.split(',')
  except Exception as exc:
    print(cmd,exc)
  return []

def get_built_stage_versions(stage, items, build_args, checked):
  def _get_built_stage_versions(type_name, checked, top):
    if type_name not in items or not type_name.startswith('stage:'):
      return []
    item = items[type_name]
    tag, this_args = stage_tag(type_name, items, build_arg_dict=build_args)
    if tag and tag in checked:
      return checked[tag].copy()
    elif tag:
      stage_versions = []
      for d in item['depends_on']: 
        stage_versions += [sv for sv in _get_built_stage_versions(d, checked, False) if sv not in stage_versions]
      if not top:
        stage_versions += [sv for sv in get_built_stage_repos(tag) if sv not in stage_versions]
      elif top and item['repo'] in items:
        this_stage_repostr = utils.repo_version_string(items[item['repo']])
        if this_stage_repostr not in stage_versions:
          stage_versions.append(this_stage_repostr)
      checked[tag] = stage_versions.copy()
      return stage_versions

  return _get_built_stage_versions('stage:' + stage['name'], checked, True)

def __build__(stage, already_tagged, build_arg_dict, items, checked_versions, jobpath=None):
  if jobpath is None: jobpath = CONFIG.job_path()
  if not jobpath:
    return False, []
  stage_name = 'stage:'+stage['name']
  dfile_dir = os.path.join(jobpath,'__dockerfiles__')
  os.makedirs(dfile_dir, exist_ok=True)
  tag = already_tagged[stage_name]['tag']

  with open(stage['path'], 'r') as r:
    contents = r.read().replace('${VYNAME}',stage['name'])
  text = '# syntax=docker/dockerfile:experimental\n'
  for (k,v) in build_arg_dict.items():
    text += 'ARG {k}="{v}"\n'.format(k=k,v=v)
  for s in stage['depends_on']:
    st = already_tagged[s]
    text += 'FROM {t} as {s}\n'.format(t=st['tag'], s=st['name'])
  for line in contents.splitlines(): #TODO nice to preserve backslash continuation
    text += line+'\n'
    if re.search(r'^[\s]*FROM ',line,re.I):
      text += 'LABEL tools.vy.remove=true\nLABEL tools.vy.tag=-\n'

  stage_versions = get_built_stage_versions(stage, items, build_arg_dict, checked_versions)
  text += 'LABEL tools.vy.repos={}\n'.format(','.join(stage_versions))
  text += 'LABEL tools.vy.tag={}\n'.format(tag)
  text += '# ----------------------------------------\n\n\n'

  build_context = stage['build_context']
  df = os.path.join(dfile_dir, tag+'.dockerfile')
  with open(df,'w') as w: w.write(text)
  cmd = ['docker', 'build', '--force-rm', '-f', df, '-t', tag]  # don't tag because of cleanup , '-t', node['s['tag']']
  cmd += ['--progress=plain']
  for (k,v) in build_arg_dict.items():
    cmd += ['--build-arg',k+'='+v]

  ok,cmds = CONFIG.secrets_cmd(stage['secrets'])
  if not ok:
    logging.error('Failed to build '+tag)
    return False, stage_versions
  else:
    cmd += cmds
    cmd += [build_context]
    # utils.print_info(' '.join(cmd)+'\n\n'+text)
    logging.info('** Building image '+tag)
    proc = subprocess.run(cmd, env={'DOCKER_BUILDKIT':'1'})
    success = proc.returncode == 0
    if success:
      already_tagged[stage_name]['hash'] = subprocess.check_output(['docker','inspect','--format','{{.ID}}',tag]).decode('utf-8').strip()
      clean_up(['dangling=true','label=tools.vy.tag='+tag])
      # os.remove(df)
    else:
      logging.error('Failed to build '+tag)
  return success, stage_versions

def sorted_vy_images(filters):
  cmd = ['docker','images']
  for f in filters:
    cmd += ['--filter',f]
  cmd += ['--format','{{.CreatedAt}}\t{{.ID}}\t{{.Repository}}\t{{.Tag}}']
  imlist = subprocess.check_output(cmd).decode('ascii').strip()
  if len(imlist) > 0:
    images = []
    for im in imlist.split('\n'):
      imageid = im.split('\t')
      images.append({'created':imageid[0], 'id':imageid[1], 'repo':imageid[2], 'tag':imageid[3]})
    return sorted(images, key=lambda k: k['created'], reverse=True) # Most recent first
  return []

def clean_up(filters):
  subprocess.run(['docker','builder','prune','-f']) # Todo, why do I need this? Why is their a build cache when everything builds successfully?
  untagged = [im['id'] for im in sorted_vy_images(filters)]
  untagged.reverse()
  if len(untagged) > 0:
    while True:
      try:
        logging.info('Attempting to remove dangling images:'+str(untagged))
        subprocess.check_output(['docker','rmi']+untagged)
        break
      except Exception as exc:
        logging.warning(str(exc))
        time.sleep(5)

def find_all(items, contextpaths=None):
  # r'[.]*dockerfile[.]*'
  return utils.search_all(r'(.+)\.stage\.dockerfile', parse, items, contextpaths=contextpaths)

def build(stages, items, build_arg_dict, already_built, build_level, jobpath=None):
  # build_level = 1 # Rebuild all - unless you've already
  # build_level = 0 # Rebuild top level - unless you've already sometime 
  # build_level = -1 # Don't build anything
  if not utils.exists(stages, items):
    logging.error('  Failed to build {}'.format(stages))
    return False

  existing_images = [im['repo']+':'+im['tag'] for im in sorted_vy_images(['label=tools.vy.tag'])]
  checked_versions = {}
  already_tagged = {}
  def __multistage__(stage_name):
    stage = items[stage_name]
    for s in stage['depends_on']:
      if __multistage__(s) == False: return False
    if stage_name not in already_tagged:
      tag,this_args = stage_tag(stage_name, items, build_arg_dict)
      if not tag: return False
      already_tagged[stage_name] = {'tag':tag,'name':stage['name'],'skipped':False,'stage_versions':[]}
      oktobuild = ((build_level == 0 and stage_name in stages) or
                  (build_level == 1) or (tag not in existing_images)) and tag not in already_built
      if oktobuild:
        utils.print_info(' * Building: {s} --as-- {i}'.format(s=stage_name,i=tag))
        success, stage_versions = __build__(stage, already_tagged, this_args, items, checked_versions, jobpath) # Build this stage
        if not success:
          utils.print_fail(' * Failed {s} --as-- {i}'.format(s=stage_name,i=tag))
          return False
        if stage_versions:
          already_tagged[stage_name]['stage_versions'] = stage_versions
        already_built.append(tag)
        utils.print_success(' * Finished: {s} --as-- {i}'.format(s=stage_name,i=tag))
        print('\n\n')
      elif tag not in already_built:
        already_tagged[stage_name]['stage_versions'] = get_built_stage_versions(stage, items, this_args, checked_versions)
      else:
        already_tagged[stage_name]['skipped'] = True
        # # I think this is cumbersome/notuseful printing
        # if tag not in already_built:
        #   utils.print_info('* Skipping: {s} as {i}'.format(s=stage_name,i=tag))
        # else: 
        #   utils.print_info('* Already built: {s} as {i}'.format(s=stage_name,i=tag))
    return True

  for top_name in stages:
    if False == __multistage__(top_name):
      return False

  if build_level != -1:
    print('')
    for tag in already_tagged:
      if not already_tagged[tag]['skipped']:
        utils.print_success(' * Built {n} --as-- {t}'.format(n=tag,t=already_tagged[tag]['tag']))
      # else: # I think this is cumbersome/notuseful printing
        # utils.print_info(' * Skipped {n} as {t}'.format(n=tag,t=already_tagged[tag]['tag']))
  return already_tagged #sum([int(v['hash'],16) for v in already_tagged.values()])

def run(type_name, items=None, build_args=None, jobpath=None):
  if items is None: items = ITEMS
  if build_args is None: build_args = {}
  already_built = []
  built = build([type_name], items, build_args, already_built, -1, jobpath=jobpath)
  if built and type_name in built:
    if jobpath is None: jobpath = CONFIG.job_path()
    if not jobpath:
      return False
    tag = built[type_name]['tag']
    datadir = os.path.join(jobpath,'__data__')
    os.makedirs(datadir,exist_ok=True)
    utils.print_info('** Running {t} with "{p}" mounted to "/__vydata__" in the container'.format(t=tag,p=datadir))
    proc = subprocess.run(['docker', 'run', '--rm', '-it', '-v', jobpath+':/__vydata__', tag])
