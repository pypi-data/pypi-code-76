import boto3
import json
import os
from uuid import uuid4
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

if 'cbucket' not in os.environ:
    os.environ['cbucket'] = 'ephod-tech.trading-advisor.auto-trade.tw.credentials'

if 'kbucket' not in os.environ:
    os.environ['kbucket'] = 'ephod-tech.trading-advisor.auto-trade.tw.key'

def setup(key, credential):

    if key is not None and credential is not None:
        s3 = boto3.client('s3')
        os.environ['key'] = key
        os.environ['credential'] = credential
        s3.download_file(os.environ['kbucket'], os.environ['key'], os.environ['key'])
        s3.download_file(os.environ['cbucket'], os.environ['credential'], os.environ['credential'])

        encyption_key = open(os.environ['key'],'rb').read()
        f = Fernet(encyption_key)
        j = json.load(open(os.environ['credential'],'rb'))

        os.environ['u'] = f.decrypt(str.encode(j['username'], 'utf-8')).decode('utf-8')
        os.environ['p'] = f.decrypt(str.encode(j['password'], 'utf-8')).decode('utf-8')

    return False

def password():
    return os.environ['p']

def username():
    return os.environ['u']
