import os, json, sys, threading
from pathlib import Path
from vytools.config import CONFIG, ITEMS
import vytools.utils as utils
import vytools.object
import vytools.episode
import vytools.utils as utils
import logging
import asyncio

from sanic import Sanic, response
from sanic_cors import CORS, cross_origin

BASEPATH = os.path.dirname(os.path.realpath(__file__))

def parse(name, pth, reponame, items):
  item = {
    'name':name,
    'repo':reponame,
    'thingtype':'ui',
    'depends_on':[],
    'path':pth
  }
  return utils._add_item(item, items, True)

def find_all(items, contextpaths=None):
  success = utils.search_all(None, parse, items, is_ui=True, contextpaths=contextpaths)
  return success

def get_ui(req, items):
  ui_name = req.get('name','')
  ui = items.get(ui_name,None)
  loaded = {'html':'Could not find '+ui_name}
  if ui:
    loaded['name'] = ui_name
    loaded['html'] = Path(ui['path']).read_text()
  return loaded

def get_episode(req, items):
  episode_name = req.get('name','')
  episode = items.get(episode_name,{})
  loaded = {}
  if episode:
    loaded = get_compose({'name':episode.get('compose','')},items)
    loaded['name'] = episode_name
    obj = items.get(episode.get('data',''),None)
    if obj:
      loaded['calibration'] = vytools.object.expand(obj['data'],obj['definition'],items)
      loaded['definition'] = obj['definition']
  return loaded

def get_compose(req,items):
  compose_name = req.get('name','')
  compose = items.get(compose_name,{})
  loaded = {}
  if compose:
    loaded['name'] = compose_name
    loaded['html'] = 'Could not find '+compose.get('ui','')
    ui = items.get(compose.get('ui',''),None)
    if ui: loaded['html'] = Path(ui['path']).read_text()
  return loaded

def build_run(req, action, jobpath, items, app_queue):
  kwargs = req['kwargs'] if 'kwargs' in req else None
  if 'jobpath' in kwargs: del kwargs['jobpath']
  if jobpath: kwargs['jobpath'] = jobpath
  # kwargs['items'] = items # TODO Add this if you every make items a keyword
  if action == 'build':
    vytools.build(req['list'],items,**kwargs)
  elif action == 'run':
    vytools.run(req['list'],items,**kwargs)
  try:
    app_queue.put_nowait([])
  except Exception as exc:
    logging.error('Failed to message ui about finished run !!!!!!!!!!!!!!!!!!')

def mimetype(pth):
  extensions_map = {
      '': 'application/octet-stream',
      '.manifest': 'text/cache-manifest',
      '.html': 'text/html',
      '.png': 'image/png',
      '.ico': 'image/ico',
      '.jpg': 'image/jpg',
      '.svg':	'image/svg+xml',
      '.css':	'text/css',
      '.js':'application/x-javascript',
      '.wasm': 'application/wasm',
      '.json': 'application/json',
      '.xml': 'application/xml',
  }
  return extensions_map.get('.'+pth.rsplit('.',1)[-1],'text/html')

def server(items=None, port=17171, ui_subscribers=None, menu=None, toplevel=None, jobpath=None):
  if items is None: items = ITEMS
  if ui_subscribers is None: ui_subscribers = {}
  THREAD = None

  app = Sanic(__name__)
  CORS(app, resources={
    r"/vybase/*": {"origins": "*"},
    r"/vy/*": {"origins": "*"}
  }, automatic_options=True)

  @app.listener('after_server_start')
  def create_task_queue(app, loop):
      app.queue = asyncio.Queue(loop=loop, maxsize=100)

  app.static('/', os.path.join(BASEPATH, 'vybase', 'main.html'))
  app.static('/favicon.ico', os.path.join(BASEPATH, 'vybase', 'favicon.ico'))
  app.static('/vybase', os.path.join(BASEPATH, 'vybase'))

  @app.route('/vy/<tag:path>', methods=['GET', 'OPTIONS'])
  async def _app_things(request, tag):
    pth = items.get('ui:/vy/'+tag,{}).get('path',None)
    if pth:
      return await response.file(pth,headers={'Content-Type':mimetype(pth)})
    else:
      return response.empty()

  @app.post('/__init__')
  async def _app_init(request):
    rslt = {
      'items':items,
      'server_subscribers':[k for k in ui_subscribers.keys()],
      'menu':CONFIG.get('menu') if menu is None else menu
    }
    if toplevel is not None and toplevel in items: rslt['toplevel'] = toplevel
    return response.json(rslt)

  @app.post('/custom/<tag>')
  async def _app_custom(request, tag):
    if tag in ui_subscribers:
      return response.json(ui_subscribers[tag](request.json) if tag in ui_subscribers else {})
    return response.json({})

  @app.post('/__<tag>__')
  async def _app_builtin(request, tag):
    nonlocal THREAD
    if tag == 'compose':
      return response.json(get_compose(request.json, items))
    elif tag == 'ui':
      return response.json(get_ui(request.json, items))
    elif tag == 'episode':
      return response.json(get_episode(request.json, items))
    elif tag == 'item':
      pth = items.get(request.json.get('name',None),{}).get('path',None)
      if pth: return await response.file(pth)
    elif tag in ['build','run']:
      starting = False
      if THREAD is None or not THREAD.is_alive():
        await app.queue.put([{'level':'info','message':'Started job, no more jobs will be accepted until this one finishes'}])
        THREAD = threading.Thread(target=build_run, args=(request.json, tag, jobpath, items, app.queue,), daemon=True)
        THREAD.start()
        starting = bool(THREAD)
      return response.json({'starting':starting})
    elif tag == 'menu':
      if menu is None: CONFIG.set('menu',request.json)
    elif tag == 'artifact':
      episode_name = request.json.get('name','')
      if episode_name.startswith('episode:'):
        artifact_name = request.json.get('artifact','_')
        apaths = vytools.episode.artifact_paths(episode_name, items, jobpath=jobpath)
        if artifact_name in apaths:
          return await response.file(apaths[artifact_name])
        else:
          logging.error('Could not find artifact {n} in {l}'.format(n=artifact_name,l=','.join(apaths)))
    return response.json({})

  @app.websocket('/server_status')
  async def _app_server_status(request, ws):
    while True:
      msg = await app.queue.get()
      await ws.send(json.dumps(msg))
  
  try:
    app.run(host="0.0.0.0", port=port)
    logging.info('Serving vytools on http://localhost:{p}'.format(p=port))
  except KeyboardInterrupt:
    # TODO shutdown running jobs?
    vytools.composerun.stop()
    print("Received exit, exiting.")
  