import os, json, logging
from termcolor import cprint
from pathlib import Path
_FOLDER = os.path.dirname(os.path.realpath(__file__))
_CONFIGFILE = os.path.join(_FOLDER,'vyconfig.json')
_FIELDS = ['contexts','items','secrets','jobs','menu']
SEARCHED_REPO_PATHS = {}
ITEMS = {}

def check_folder(field,values):
  success = True
  for v in values:
    if not os.path.isdir(v):
      logging.error('The path "{v}" is not a directory. Create this directory before setting it as your "{f}" directory'.format(v=v,f=field))
      success = False
  return success

class __CONFIG:
  def __init__(self):
    self._data = {}
    self._secrets = {}
    try:
      self._data = json.loads(Path(_CONFIGFILE).read_text().strip())
      self.__get_secrets()
    except:
      pass
  
  def __write(self):
    with open(_CONFIGFILE,'w') as w:
      w.write(json.dumps(self._data))

  def __get_secrets(self):
    if 'secrets' in self._data and self._data['secrets']:
      self._secrets = {}
      if type(self._data['secrets']) == str:
        self._data['secrets'] = [self._data['secrets']]
      for folder in self._data['secrets']:
        for root, dirs, files in os.walk(folder):
          for sname in files:
            self._secrets[sname] = os.path.join(folder, sname)

  def set(self,field,value):
    if field in _FIELDS:
      if field in ['secrets','contexts']:
        if check_folder(field, value):
          self._data[field] = [str(Path(v).resolve()) for v in value]
      elif field in ['jobs']:
        if check_folder(field, [value]):
          self._data[field] = str(Path(value).resolve())
          ign = os.path.join(self._data[field],'.vyignore')
          if not os.path.exists(ign):
            with open(ign,'w'): pass
      else:
        self._data[field] = value
      self.__write()
      if field == 'secrets':
        self.__get_secrets()

  def get(self,field):
    return self._data[field] if self._data and field in self._data else None

  def secrets_cmd(self, secret_list):
    cmd = []
    ok = True
    for secret in secret_list:
      if secret not in self._secrets:
        logging.error('No secret found for id={s}'.format(s=secret))
        secrets_path = self.get('secrets')
        if not secrets_path:
          logging.error('secrets path not specified, specify path with vytools --secrets , (e.g. "vytools --secrets path/to/folder/containing/secrets" info)')
        else:
          logging.error('This secret should be in '+secrets_path)
        ok = False
      else:
        cmd += ['--secret','id='+secret+',src='+self._secrets[secret]]
    return (ok, cmd)

  def info(self):
    cprint('VyTools Configuration & Summary:', attrs=['bold'])
    print('  Configuration saved at: '+_CONFIGFILE)
    print('  Contexts = {s}'.format(s=self.get('contexts')))
    print('  Secrets at {s}'.format(s=self.get('secrets')))
    jobpath = self.get('jobs')
    if jobpath:
      print('  Jobs at {s}'.format(s=jobpath))
    else:
      cprint('  Jobs path not specified, specify path with vytools --jobs , (e.g. "vytools --jobs path/to/folder/for/jobs" info)', attrs=['bold'])
    print('  Items found:')
    items = self.get('items')
    typs = {}
    if items:
      for i in items:
        typ = i.split(':')[0]
        if typ not in typs: typs[typ] = 0
        typs[typ] += 1
    for typ in typs:
      print('    - {n} {t} items'.format(t=typ,n=typs[typ]))

  def job_path(self):
    jp = self.get('jobs')
    if not jp:
      logging.error('No jobs path specified ("vytools info")')
      return None
    return jp

CONFIG = __CONFIG()

