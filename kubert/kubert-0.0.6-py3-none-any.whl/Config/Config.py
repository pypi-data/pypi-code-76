import os

class Config(object):

  def __init__(self, *args, **kwargs):
    super(Config,self).__init__(*args,**kwargs)
    self.token = open('/run/secrets/kubernetes.io/serviceaccount/token', "r").read()
    self.namespace = open('/run/secrets/kubernetes.io/serviceaccount/namespace', "r").read()
    self.cert = '/run/secrets/kubernetes.io/serviceaccount/ca.crt'
    self.host = os.environ.get('KUBERNETES_SERVICE_HOST')
    self.proto = os.environ.get('KUBERNETES_PORT_443_TCP_PROTO')
    self.addr = os.environ.get('KUBERNETES_PORT_443_TCP_ADDR')
    self.port = os.environ.get('KUBERNETES_PORT')
    self.tcpPort = os.environ.get('KUBERNETES_PORT_443_TCP_PORT')
    self.httpsPort = os.environ.get('KUBERNETES_SERVICE_PORT_HTTPS')
    self.tcp = os.environ.get('KUBERNETES_PORT_443_TCP')
    self.servicePort = os.environ.get('KUBERNETES_SERVICE_PORT')