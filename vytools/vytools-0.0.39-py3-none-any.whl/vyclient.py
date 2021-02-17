import json, os, time, getpass, shutil, sys, threading
from vytools.meteorclient import MeteorClient
from multiprocessing import Queue

class VyClient(MeteorClient):
  def __init__(self, socket, vyroot, username=None, password=None):
    self.socket = socket
    self.username = username
    self.password = password
    self.log_cache = Queue()
    self.token = None
    self.user = None
    self.url = socket.replace('ws://','http://').replace('wss://','https://').rstrip('websocket')
    print('  * The VYPATH is: '+vyroot,flush=True)
    print('  * The VYSERVER is: '+self.url,flush=True)
    print('  * The WEBSOCKET is: '+self.socket,flush=True)
    if not os.path.isabs(vyroot):
      raise Exception('The vy directory may not be relative. Specify an absolute path for vy. (need not already exist!)')

    os.makedirs(vyroot, exist_ok=True)
    dockerignore = os.path.join(vyroot,'.dockerignore')
    if not os.path.isfile(dockerignore):
      with open(dockerignore,'w') as fle:
        fle.write('**/.hg\n**/.git\n.vy\n')

    MeteorClient.__init__(self, self.socket, auto_reconnect=True, auto_reconnect_timeout=1)
    self.on('changed', self.__changed)
    self.on('connected', self.__connected)
    self.on('logged_in', self.__logged_in)
    self.on('subscribed', self.__subscribed)
    self.on('socket_closed', self.__closed)
    self.on('closed', self.__closed)
    self.on('reconnected', self.__connected)
    self.connect()

  def __closed(self, code, reason):
    print('*VYCLIENT CONNECTION CLOSED',code, reason)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.logout() # logout
    self.close() # close

  def __changed(self, collection, _id, fields, cleared):
    if collection == 'users':
      if self.user is not None and _id == self.user['_id']:
        for f in fields:
          self.user[f] = fields[f]

  def __logtoclient(self):
    logstring = []
    lastlevel = None
    def logit(msg,lvl):
      if logstring and self.connected:
        self.call("ClientLog", ['\n'.join(msg), lvl])
        return []
      return logstring

    while True:
      while not self.log_cache.empty():
        data = self.log_cache.get()
        if lastlevel != data['level']:
          logstring = logit(logstring, lastlevel)
          lastlevel = data['level']
        logstring += [data['msg']]
      logstring = logit(logstring, lastlevel)
      time.sleep(0.1)

  def __register_user(self,err,x):
    if err is None:
      self.user = x
      # self.subscribe("stream-vystream", ["userstream__"+self.user['_id'],True])
      threading.Thread(target=self.__logtoclient, daemon=True).start()
    else:
      print('Error registering user',err)

  def __login_callback(self, err, token):
    if err is None and self.token is None:
      self.token = token['token']
    elif err is not None:
      self.log('Login error '+str(err),'danger')
      self.token = None

  def __logged_in(self, data):
    if self.user is not None: # for some reason if a callback throws an exception I get sent back here, so exiting early
      return
    self.call("getuser", [], callback=self.__register_user)
    self.log('vyengine connected','info')

  def __subscribed(self, subscription):
    self.log('  * engine subscribed to : '+subscription,'info')

  def __connected(self):
    self.log('(Re)connecting...', None)
    if self.token is not None:
      password = 'ignor'.encode('utf-8')
      self.login(self.user, password, token=self.token, callback=self.__login_callback)
    else:
      username = self.username if self.username is not None else input("vytools Username:")
      password = self.password if self.password is not None else getpass.getpass("vytools Password:")
      self.log('Attempting login...','info')
      self.login(username, password.encode('utf-8'), callback=self.__login_callback)

  def log(self, msg, level):
    if self.connected:
      self.log_cache.put({"msg":msg,"level":level})
    else:
      print(msg)
