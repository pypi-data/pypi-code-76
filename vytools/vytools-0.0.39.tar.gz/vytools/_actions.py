import logging, json
from pathlib import Path
from termcolor import cprint
from vytools.config import CONFIG, ITEMS

import vytools.utils
import vytools.stage
import vytools.compose
import vytools.episode
import vytools.definition
import vytools.object
import vytools.ui

def _label_repositories(items):
  repo_path_list = []
  repo_path_dict = {}
  for r,v in items.items():
    if r.startswith('repo:'):
      repo_path_list.append(v['path'])
      repo_path_dict[v['path']] = r
  repo_path_list.sort(key=len)
  repo_path_list.reverse()
  for i,v in items.items():
    ipaths = [v['path']]+[str(p) for p in Path(v['path']).parents]
    for r in repo_path_list:
      if r in ipaths:
        v['repo'] = repo_path_dict[r]
        break

def _scan(contextpaths=None):
  if contextpaths:
    print('\nScanning the following directories for vy items:'+'\n  '.join(['']+contextpaths)+'\n\n')
  items = {}
  success = True
  success &= vytools.definition.find_all(items, contextpaths=contextpaths)
  success &= vytools.object.find_all(items, contextpaths=contextpaths)
  success &= vytools.stage.find_all(items, contextpaths=contextpaths)
  success &= vytools.ui.find_all(items, contextpaths=contextpaths)
  success &= vytools.compose.find_all(items, contextpaths=contextpaths)
  success &= vytools.episode.find_all(items, contextpaths=contextpaths)

  # Assign repositories
  _label_repositories(items)

  # if success: # Check for missing dependencies
  for i,it in items.items():
    for dependency in it['depends_on']:
      if dependency not in items:
        logging.warning(' * Item {j} (depended on by {i}) is not in the list of found items'.format(i=i, j=dependency))
        success = False

  # if success: # Reverse dependency chain
  for i in items:
    items[i]['depended_on'] = []
  for i in items:
    for d in items[i]['depends_on']:
      if d in items:
        items[d]['depended_on'].append(i)

  if success:
    thinglist = [item for item in items]
    sorted_things = vytools.utils.sort(thinglist, items)
    for itemid in items: # Sort the depends_on of each thing
      items[itemid]['depends_on'] = [i for i in sorted_things if i in items[itemid]['depends_on']]

  return (success, items)

def build(original_list, items=None, build_args=None, build_level=0, jobpath=None):
  if items is None: items = ITEMS
  if build_args is None: build_args = {}
  built = []
  stages = []
  for type_name in original_list:
    if type_name.startswith('stage:') and type_name not in stages:
      stages.append(type_name)
    elif type_name.startswith('compose:') and type_name in items:
      build_arg_dict = build_args.copy()
      build_level = max(0,build_level) # Don't write for a compose if run at this level
      if False == vytools.compose.build(type_name, items=items, build_args=build_arg_dict, built=built, build_level=build_level, eppath=jobpath):
        return False
    elif type_name.startswith('episode:') and type_name in items:
      build_arg_dict = build_args.copy()
      build_level = max(0,build_level) # Don't write for a compose if run at this level
      if False == vytools.episode.build(type_name, built, build_args=build_arg_dict, items=items, build_level=build_level, eppath=jobpath):
        return False

  build_arg_dict = build_args.copy()
  if len(stages) > 0:
    if not vytools.utils.exists(stages, items):
      return False
    if not vytools.stage.build(stages, items, build_arg_dict, built, build_level, jobpath=jobpath):
      return False
  return built

def run(original_list, items=None, build_args=None, clean=False, data=None, data_mods=None, jobpath=None):
  if items is None: items=ITEMS
  if build_args is None: build_args = {}
  results = {}
  for type_name in original_list:
    if type_name.startswith('stage:'):
      build_arg_dict = build_args.copy()
      results[type_name] = vytools.stage.run(type_name, items=items, build_args=build_arg_dict, jobpath=jobpath)
    elif type_name.startswith('episode:'):
      build_arg_dict = build_args.copy()
      results[type_name] = vytools.episode.run(type_name, items=items, build_args=build_arg_dict, clean=clean, data=data, data_mods=data_mods, jobpath=jobpath)
  return results

def _recursive_list(name, spctop, items, field):
  def list_all_dependencies(name, spc, visited, items):
    if name not in items:
      print(spc+name+'[?]')
    elif name in visited:
      print(spc+name+'[*]')
    else:
      print(spc+name)
      visited.append(name)
      for d in items[name][field]:
        list_all_dependencies(d, spc+spctop, visited, items)
  visited = []
  list_all_dependencies(name, spctop, visited, items)

def info(original_list, items=None, list_dependencies=False, expand=False):
  if items is None: items=ITEMS
  CONFIG.info()
  dep_spaces = '   '
  for i in original_list:
    if i in items:
      cprint(i, attrs=['bold'])
      print(json.dumps(items[i], indent=6, sort_keys=True))
      if i.startswith('object:') and expand:
        item = items[i]
        obj = vytools.object.expand(item['data'], item['definition'], items)
        print(json.dumps(obj, indent=6, sort_keys=True))
      if list_dependencies:
        cprint(dep_spaces + 'dependencies', attrs=['bold'])
        _recursive_list(i, dep_spaces, items, 'depends_on')
        cprint(dep_spaces + 'dependents', attrs=['bold'])
        _recursive_list(i, dep_spaces, items, 'depended_on')

      repo_versions = vytools.utils.get_repo_versions([i],items)
      print('This item depends directly or indirectly on these repositories which are currently at these versions:')
      for x in repo_versions.values():
        cprint('  '+x,color='yellow' if x.endswith('+') else 'green')
      if i.startswith('stage:'):
        for image in vytools.stage.stages(i):
          print('Image {} was built with repositories|version'.format(image))
          for x in vytools.stage.get_built_stage_repos(image):
            cprint('  '+x,color='yellow' if x.endswith('+') else 'green')

    else:
      cprint('Unknown item {i}'.format(i=i), attrs=['bold'])

  if not original_list:
    repo_versions = vytools.utils.get_repo_versions(lst,items)
    for x in repo_versions.values():
      cprint(x,color='yellow' if x.endswith('+') else 'green')