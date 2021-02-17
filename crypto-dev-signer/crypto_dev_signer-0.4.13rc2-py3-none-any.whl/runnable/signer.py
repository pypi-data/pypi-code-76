# standard imports
import os
import sys
import stat
import socket
import json
import logging 
import argparse

# third-party imports
import confini
from jsonrpc.exceptions import *

# local imports
from crypto_dev_signer.eth.signer import ReferenceSigner
from crypto_dev_signer.eth.transaction import EIP155Transaction
from crypto_dev_signer.keystore import ReferenceKeystore
from crypto_dev_signer.error import UnknownAccountError

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

config_dir = '.'

db = None
signer = None
chainId = 8995
socket_path = '/run/crypto-dev-signer/jsonrpc.ipc'

argparser = argparse.ArgumentParser()
argparser.add_argument('-c', type=str, default=config_dir, help='config file')
argparser.add_argument('--env-prefix', default=os.environ.get('CONFINI_ENV_PREFIX'), dest='env_prefix', type=str, help='environment prefix for variables to overwrite configuration')
argparser.add_argument('-i', type=int, help='default chain id for EIP155')
argparser.add_argument('-s', type=str, help='socket path')
argparser.add_argument('-v', action='store_true', help='be verbose')
argparser.add_argument('-vv', action='store_true', help='be more verbose')
args = argparser.parse_args()

if args.vv:
    logging.getLogger().setLevel(logging.DEBUG)
elif args.v:
    logging.getLogger().setLevel(logging.INFO)

config = confini.Config(args.c, args.env_prefix)
config.process()
config.censor('PASSWORD', 'DATABASE')
config.censor('SECRET', 'SIGNER')
logg.debug('config loaded from {}:\n{}'.format(config_dir, config))

if args.i:
    chainId = args.i
if args.s:
    socket_path = args.s
elif config.get('SIGNER_SOCKET_PATH'):
    socket_path = config.get('SIGNER_SOCKET_PATH')


# connect to database
dsn = 'postgresql://{}:{}@{}:{}/{}'.format(
        config.get('DATABASE_USER'),
        config.get('DATABASE_PASSWORD'),
        config.get('DATABASE_HOST'),
        config.get('DATABASE_PORT'),
        config.get('DATABASE_NAME'),    
    )

logg.info('using dsn {}'.format(dsn))
logg.info('using socket {}'.format(socket_path))


class MissingSecretError(BaseException):

    def __init__(self, message):
        super(MissingSecretError, self).__init__(message)


def personal_new_account(p):
    password = p
    if p.__class__.__name__ != 'str':
        if p.__class__.__name__ != 'list':
            e = JSONRPCInvalidParams()
            e.data = 'parameter must be list containing one string'
            raise ValueError(e)
        logg.error('foo {}'.format(p))
        if len(p) != 1:
            e = JSONRPCInvalidParams()
            e.data = 'parameter must be list containing one string'
            raise ValueError(e)
        if p[0].__class__.__name__ != 'str':
            e = JSONRPCInvalidParams()
            e.data = 'parameter must be list containing one string'
            raise ValueError(e)
        password = p[0]

    r = db.new(password)
             
    return r


def personal_sign_transaction(p):
    logg.debug('got {} to sign'.format(p[0]))
    #t = EIP155Transaction(p[0], p[0]['nonce'], 8995)
    t = EIP155Transaction(p[0], p[0]['nonce'], int(p[0]['chainId']))
    z = signer.signTransaction(t, p[1])
    raw_signed_tx = t.rlp_serialize()
    o = {
        'raw': '0x' + raw_signed_tx.hex(),
        'tx': t.serialize(),
        }
    logg.debug('signed {}'.format(o))
    return o


# TODO: temporary workaround for platform, since personal_signTransaction is missing from web3.py
def eth_signTransaction(tx):
    return personal_sign_transaction([tx, ''])


def eth_sign(p):
    logg.debug('got message {} to sign'.format(p[1]))
    message_type = type(p[1]).__name__
    if message_type != 'str':
        raise ValueError('invalid message format, must be {}, not {}'.format(message_type))
    z = signer.signEthereumMessage(p[0], p[1][2:])
    return str(z)


methods = {
        'personal_newAccount': personal_new_account,
        'personal_signTransaction': personal_sign_transaction,
        'eth_signTransaction': eth_signTransaction,
        'eth_sign': eth_sign,
    }


def jsonrpc_error(rpc_id, err):
    return {
            'json-rpc': '2.0',
            'id': rpc_id,
            'error': {
                'code': err.CODE,
                'message': err.MESSAGE,
                },
            }


def jsonrpc_ok(rpc_id, response):
    return {
            'json-rpc': '2.0',
            'id': rpc_id,
            'result': response,
            }


def is_valid_json(j):
    if j.get('id') == 'None':
        raise ValueError('id missing')
    return True


def process_input(j):
    rpc_id = j['id']
    m = j['method']
    p = j['params']
    return (rpc_id, methods[m](p))


def start_server_tcp(spec):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(spec)
    logg.debug('created tcp socket {}'.format(spec))
    start_server(s)


def start_server_unix(socket_path):
    socket_dir = os.path.dirname(socket_path)
    try:
        fi = os.stat(socket_dir)
        if not stat.S_ISDIR:
            RuntimeError('socket path {} is not a directory'.format(socket_dir))
    except FileNotFoundError:
        os.mkdir(socket_dir)

    try:
        os.unlink(socket_path)
    except FileNotFoundError:
        pass
    s = socket.socket(family = socket.AF_UNIX, type = socket.SOCK_STREAM)
    s.bind(socket_path)
    logg.debug('created unix ipc socket {}'.format(socket_path))
    start_server(s)


def start_server(s):
    s.listen(10)
    logg.debug('server started')
    while True:
        (csock, caddr) = s.accept()
        d = csock.recv(4096)
        j = None
        try:
            j = json.loads(d)
            is_valid_json(j)
            logg.debug('{}'.format(d.decode('utf-8')))
        except Exception as e:
            logg.error('input error {}'.format(e))
            csock.send(json.dumps(jsonrpc_error(None, JSONRPCParseError)).encode('utf-8'))
            csock.close()
            continue

        try:
            (rpc_id, r) = process_input(j)
            r = jsonrpc_ok(rpc_id, r)
            j = json.dumps(r).encode('utf-8')
            csock.send(j)
        except ValueError as e:
            # TODO: handle cases to give better error context to caller
            logg.error('process error {}'.format(e))
            csock.send(json.dumps(jsonrpc_error(j['id'], JSONRPCServerError)).encode('utf-8'))
        except UnknownAccountError as e:
            logg.error('process unknown account error {}'.format(e))
            csock.send(json.dumps(jsonrpc_error(j['id'], JSONRPCServerError)).encode('utf-8'))

        csock.close()
    s.close()

    os.unlink(socket_path)


def init():
    global db, signer
    secret_hex = config.get('SIGNER_SECRET')
    if secret_hex == None:
        raise MissingSecretError('please provide a valid hex value for the SIGNER_SECRET configuration variable')

    secret = bytes.fromhex(secret_hex)
    kw = {
            'symmetric_key': secret,
            }
    db = ReferenceKeystore(dsn, **kw)
    signer = ReferenceSigner(db)


def main():
    init()
    arg = None
    try:
        arg = json.loads(sys.argv[1])
    except:
        logg.info('no json rpc command detected, starting socket server')
        socket_spec = socket_path.split(':')
        if len(socket_spec) == 2:
            host = socket_spec[0]
            port = int(socket_spec[1])
            start_server_tcp((host, port))
        else:
            start_server_unix(socket_path)
        sys.exit(0)
   
    (rpc_id, response) = process_input(arg)
    r = jsonrpc_ok(rpc_id, response)
    sys.stdout.write(json.dumps(r))


if __name__ == '__main__':
    main()
