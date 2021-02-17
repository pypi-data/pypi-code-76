# standard imports
import logging
import re
import socket
import uuid
import json

logg = logging.getLogger(__file__)


def jsonrpc_request(method, params):
    uu = uuid.uuid4()
    return {
        "jsonrpc": "2.0",
        "id": str(uu),
        "method": method,
        "params": params,
            }

class PlatformMiddleware:

    # id for the request is not available, meaning we cannot easily short-circuit
    # hack workaround
    id_seq = -1
    re_personal = re.compile('^personal_.*')
    ipcaddr = None


    def __init__(self, make_request, w3):
        self.w3 = w3 
        self.make_request = make_request
        if self.ipcaddr == None:
            raise AttributeError('ipcaddr not set')

    
    # TODO: understand what format input params come in
    # single entry input gives a tuple on params, wtf...
    # dict input comes as [{}] and fails if not passed on as an array
    @staticmethod
    def _translate_params(params):
        #if params.__class__.__name__ == 'tuple':
        #    r = []
        #    for p in params:
        #        r.append(p)
        #    return r

        if params.__class__.__name__ == 'list' and len(params) > 0:
            return params[0]

        return params


    # TODO: DRY
    def __call__(self, method, suspect_params):

        self.id_seq += 1
        logg.debug('in middleware method {} params {} ipcpath {}'.format(method, suspect_params, self.ipcaddr))

        if self.re_personal.match(method) != None:
            params = PlatformMiddleware._translate_params(suspect_params)
            # multiple providers is removed in web3.py 5.12.0
            # https://github.com/ethereum/web3.py/issues/1701
            # thus we need a workaround to use the same web3 instance
            s = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_STREAM, proto=0)
            ipc_provider_workaround = s.connect(self.ipcaddr)

            logg.info('redirecting method {}  params {} original params {}'.format(method, params, suspect_params))
            o = jsonrpc_request(method, params[0])
            j = json.dumps(o)
            logg.debug('send {}'.format(j))
            s.send(j.encode('utf-8'))
            r = s.recv(4096)
            s.close()
            logg.debug('got recv {}'.format(str(r)))
            jr = json.loads(r)
            jr['id'] = self.id_seq
            #return str(json.dumps(jr))
            return jr

        elif method == 'eth_signTransaction':
            params = PlatformMiddleware._translate_params(suspect_params)
            s = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_STREAM, proto=0)
            ipc_provider_workaround = s.connect(self.ipcaddr)
            logg.info('redirecting method {}  params {} original params {}'.format(method, params, suspect_params))
            o = jsonrpc_request(method, params[0])
            j = json.dumps(o)
            logg.debug('send {}'.format(j))
            s.send(j.encode('utf-8'))
            r = s.recv(4096)
            s.close()
            logg.debug('got recv {}'.format(str(r)))
            jr = json.loads(r)
            jr['id'] = self.id_seq
            #return str(json.dumps(jr))
            return jr

        elif method == 'eth_sign':
            params = PlatformMiddleware._translate_params(suspect_params)
            s = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_STREAM, proto=0)
            ipc_provider_workaround = s.connect(self.ipcaddr)
            logg.info('redirecting method {}  params {} original params {}'.format(method, params, suspect_params))
            o = jsonrpc_request(method, params)
            j = json.dumps(o)
            logg.debug('send {}'.format(j))
            s.send(j.encode('utf-8'))
            r = s.recv(4096)
            s.close()
            logg.debug('got recv {}'.format(str(r)))
            jr = json.loads(r)
            jr['id'] = self.id_seq
            return jr



        r = self.make_request(method, suspect_params)
        return r
