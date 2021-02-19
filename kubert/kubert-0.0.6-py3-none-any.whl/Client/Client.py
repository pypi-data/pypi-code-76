import logging
import re
import urllib3
import os
import json, yaml
import inspect
from sys import version
from unicodedata import category
from idna.core import valid_label_length
from urllib3.exceptions import HTTPError
from kubert import Config
from types import SimpleNamespace
from pprint import pp

class Client(object):

  def __init__(self, config, poolSize=os.cpu_count()):
    super(Client, self).__init__()
    if config is None:
      config = Config()
    self.config = config
    
    self._HTTPPool = urllib3.connectionpool.connection_from_url(
      'https://' + self.config.host + ':' + self.config.tcpPort, 
      maxsize=poolSize,
      ca_certs = self.config.cert
    )

    self.headers = {
      'Authorization': 'Bearer ' + self.config.token,
      "User-Agent": "nginx/kubert 0.1"
    }

    self._dicoverResources()

  def request(self, *args, **kwargs):
    kwargs['headers'] = {}
    kwargs['headers'].update(self.headers)
    return self._HTTPPool.request(*args, **kwargs)

  def _dicoverResources(self):
    self._apiResources = {}  
    self._apiResources['core'] = {}
    self._apiResources['core']['v1'] = json.loads(self.request("GET", "/api/v1").data)['resources']

    for s in json.loads(self.request("GET", "/apis/apiregistration.k8s.io/v1/apiservices").data)['items']:
      if 'group' not in s['spec']:
        continue
      endpoint = "/apis/" + s['spec']['group'] + "/" + s['spec']['version']
      r = json.loads(self.request("GET", endpoint).data)
      if s['spec']['group'] not in self._apiResources:
        self._apiResources[s['spec']['group']] = {} 
      self._apiResources[s['spec']['group']][s['spec']['version']] = r['resources']
    
    self.resources = {}

    for s in self._apiResources:
      for v in self._apiResources[s]:
        for r in self._apiResources[s][v]:
          if s == 'core':
            endpoint = "/api/%s" % (v)
          else:
            endpoint = "/apis/%s/%s" % (s,v)
          if r['kind'] not in self.resources:
            self.resources[r['kind']] = {}
          if v not in self.resources[r['kind']]:
            self.resources[r['kind']][v] = []
          categories = []
          if "categories" in r:
            categories.extend(r['categories'])

          self.resources[r['kind']][v].append({
            'categories': categories,
            'name': r['name'],
            'singularName': r['singularName'],
            'namespaced': r['namespaced'],
            'verbs': r['verbs'],
            'group': s
          })

  def _encodeResource(self,o,encoder=None):
    #If Object is dict do nothing
    if isinstance(o,dict):
      return o
    #TODO Implement SimpleNamespace Decoder
    if encoder is not None:
      return encoder.encode(o)
    #Frist try json
    try:
      return json.loads(o)
    except Exception:
    # Now try yaml
      try:
        return yaml.safe_load(o)
      except Exception:
        raise TypeError("Could not encode object type of '%s'" % (o.__class__))
  
  def _isValidateResource(self,resource):
    valid = True
    msgs = []
    if 'apiVersion' not in resource:
        valid = False
        msgs.append("apiVersion not defined")
    if 'kind' not in resource:
      valid = False
      msgs.append("kind not defined")
    if 'name' not in resource['metadata']:
      valid = False
      msgs.append("name not defined")
    
    return valid, msgs

  def resourceExist(self, resource, version="v1"):
    if resource not in self.resources:
      return False
    elif version not in self.resources[resource]:
      return False
    else:
      return True

  def getEndpoints(self, resource, verb, name=None, namespace=None, version="v1"):
    if not self.resourceExist(resource,version):
      print("Couldn't find resource", self._apiResources)
      return None
    resources = self.resources[resource][version]
    endpoints = []
    for r in resources:
      endpoint = ""
      if verb in r['verbs']:
        if r['group'] == 'core':
          endpoint += "/api/"
        else:
          endpoint += "/apis/"+r['group']+"/"
        endpoint += version+"/"
        if namespace is not None:
          endpoint += "namespaces/" + namespace + "/" + r['name']
        else:
          endpoint += r['name']
        if name is not None:
          endpoint += "/" + name 
        endpoints.append(endpoint)
    return endpoints

  def getEndpointsB(self,resource, verb=None, name=None, namespace=None, version="v1", group=None):
    resourceMatch = self.resources[resource][version]
    endpoints = []
    for r in resourceMatch:
      if verb not in r['verbs']:
        continue
      if r['group'] == 'core':
        endpoint = "/api/%s/" % (version)
      else:
        endpoint = "/apis/%s/%s/" % (r['group'],version)
      if r['namespaced'] and namespace is not None:
        endpoint += "namespaces/%s/" % (namespace) 
      endpoint += "%s" % (r['name'])
      if name is not None:
        endpoint += "/%s" % (name)
      if 'all' in r['categories'] and r['group'] == group:
        return endpoint
      endpoints.append(endpoint)
    if len(endpoints) == 1:
      return endpoints[0]
    elif len(endpoints) <= 0:
      return None
    return endpoints

  def _generateBody(self, *args, **kwargs):
    resource = args[0]
    if 'body' in kwargs:
      raise ValueError("'body' should not assigned, use resource argument")
    encoder = None
    if "encoder" in kwargs:
      encoder = kwargs['encoder']
      del kwargs['encoder']
    o = self._encodeResource(resource,encoder)
    isValid, errs = self._isValidateResource(o)
    if not isValid:
      raise ValueError("Not a valid Kubernetes resource: \n"+ "-"*10 + "\n"+"\n".join(errs))
    return o

  def create(self, *args, **kwargs):
    o = self._generateBody(*args, **kwargs)
    return self._send("POST", o, *args, **kwargs )

  def update(self, *args, **kwargs):
    o = self._generateBody(*args, **kwargs)
    return self._send("PUT", o, *args, name=o['metadata']['name'], **kwargs )

  def _send(self, method, resource, *args, namespace=None, name=None, version="v1", **kwargs):
    if 'url' in kwargs:
      endpoint = kwargs['url']
    else:
      endpointInfo = resource['apiVersion'].split('/')
      version = endpointInfo.pop()
      if len(endpointInfo) > 0:
        group = endpointInfo.pop(0)
      else:
        group = 'core'
    
    endpoint = self.getEndpointsB(
      resource['kind'], 
      inspect.stack()[1].function, 
      name=name, 
      namespace=namespace, 
      version=version,
      group=group
    )
    if endpoint is None:
      raise ValueError("Could not %s object. Invalid Kubernetes Object!" % (inspect.stack()[1].function))
    kwargs['body'] = json.dumps(resource)
    r: urllib3.HTTPResponse = self.request(method, endpoint, *args[1:], **kwargs)
    if not 200 <= r.status <= 299:
      raise HTTPError("%d: %s: %s " % (r.status, r.reason, r._request_url), r.data)
    return json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))

  def list(self, resource, namespace=None, version="v1"):
    listEndpoints = self.getEndpointsB(resource, 'list', namespace=namespace, version=version)
    results =[]
    for e in listEndpoints:
      if not  (e.endswith('/status') or e.endswith('/log')):
        r = self.request("GET", e)
        if not 200 <= r.status <= 299:
          raise HTTPError("%d: %s: %s " % (r.status, r.reason, r._request_url), r.data)
        results.append(json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d)))
    if len(results) == 1:
      return results[0]
    return results

  def get(self, resource, name, namespace=None, version="v1"):
    itemEndpoints = self.getEndpointsB(resource, 'get', name=name, namespace=namespace, version=version)
    results =[]
    for e in itemEndpoints:
      if not (e.endswith('/status/'+name) or e.endswith('/log/'+name)):
       r = self.request("GET", e)
      if not 200 <= r.status <= 299:
        raise HTTPError("%d: %s: %s " % (r.status, r.reason, r._request_url), r.data)
      results.append(json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d)))
    if len(results) == 1:
      return results[0]
    return results

  def watch(self, resource, name=None, namespace=None, version="v1"):
    watchEndpoints = self.getEndpointsB(resource, 'watch', name=name, namespace=namespace, version=version)
    watchers = []
    for e in watchEndpoints:
      r = self.request('GET', e+"?watch=1",  preload_content=False)
      if not 200 <= r.status <= 299:
        raise HTTPError("%d: %s: %s " % (r.status, r.reason, r._request_url), r.data)
      watchers.append(r)
    return watchers


    
      



    
      
  