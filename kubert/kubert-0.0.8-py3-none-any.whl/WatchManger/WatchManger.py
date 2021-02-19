import json
import logging
from pprint import pp
import sys, traceback
from types import SimpleNamespace
from threading import Thread
from kubert import Client
from urllib3 import request, response

objectOperations = {
  "Update": "MODIFIED",
  "Add": "ADDED",
  "Delete": "DELETED",
  "Create": "ADDED"
}

class WatchManager(object):

  def __init__(self, client: Client) -> None:
      super().__init__()
      self._client = client
      self._watchers = {}
      self.logger = logging.getLogger(__name__)
      self.logger.setLevel(logging.DEBUG)
      self.logger.addHandler(logging.StreamHandler(sys.stdout))


  def addWatcher(self, watcherName, resource, 
    resourceName=None, 
    namespace=None, 
    version="v1", 
    addedCB=None, 
    modifiedCB=None, 
    deletedCB=None,
    exitedCB=None
    ):
    watchers = self._client.watch(resource, name=resourceName, namespace=namespace, version=version)
    for i,v in enumerate(watchers):
      threadName = "%s-%d" % (watcherName,i)
      self._watchers[threadName] = objectWatcher(threadName, v, self.logger,
        added=addedCB, 
        modified=modifiedCB, 
        deleted=deletedCB,
        exited=exitedCB
      )
      self._watchers[threadName].start()
    return True

  def registerCallbacks(self, watcherName, added=None, modified=None, deleted=None, exited=None):
    self._watchers[watcherName].registerCallbacks(added=added, modified=modified, deleted=deleted,exited=exited)
    return True

class objectWatcher(Thread):
  def __init__(self, watcherName, watcher, logger, **kwargs) -> None:
      super().__init__()
      self._watcher = watcher
      self._logger = logger
      self.name = watcherName
      self._callbacks = {
        'added': [],
        'modified': [],
        'deleted': [],
        'exited': [],
      }
      self._kwargs = kwargs
      self.registerCallbacks(**kwargs)

  def watchProcessor(self, resp: response):
    prev = ""
    try:
      for seg in resp.stream():
        seg = prev + seg.decode('utf8')
        lines = seg.split("\n")
        if not seg.endswith("\n"):
            prev = lines[-1]
            lines = lines[:-1]
        else:
            prev = ""
        for line in lines:
          if line:
              yield line
    except:
      print("There was an exception")
      if resp.status == 200:
        self._logger.error("There has been an error getting data. Check you configurations and try again: UNKNOWN ERROR!")
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        print("Recieved Response: %d->%s" % (resp.status, resp.data ))
        yield None
        yield resp.data
      else:
        self._logger.error("There has been an error getting data. Check you configurations and try again: UNKNOWN ERROR!")
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        print("Recieved Response: %d->%s" % (resp.status, resp.data ))
        yield None

  def run(self):
    for e in self.watchProcessor(self._watcher):
      o = None
      primitive = json.loads(e)
      if 'type' not in primitive:
        for m in primitive['metadata']['managedFields']:
          if m['fieldsType'] == 'FieldsV1':
            type = objectOperations[m['operation']]
        wrapped = {
          "type": type,
          "object": primitive
        }
        o = json.loads(json.dumps(wrapped), object_hook=lambda d: SimpleNamespace(**d))
      else:
        o =json.loads(e, object_hook=lambda d: SimpleNamespace(**d))
      self._logger.debug("type: %s -> %s:%s" % (o.type, o.object.metadata.selfLink, o.object.metadata.resourceVersion))
      if len(self._callbacks[o.type.lower()]) > 0:
        for cb in self._callbacks[o.type.lower()]:
          cb(self, o)
      else:
       self._logger.debug("No Callbacks found for %s" % (o.type.lower()))

    for cb in self._callbacks['exited']:
          cb(self)
        

  def registerCallbacks(self, added=None, modified=None, deleted=None, exited=None):
    if added is not None:
      self._callbacks['added'].append(added)
    if modified is not None:
      self._callbacks['modified'].append(modified)
    if deleted is not None:
      self._callbacks['deleted'].append(deleted)
    if exited is not None:
      self._callbacks['exited'].append(exited)
    return True