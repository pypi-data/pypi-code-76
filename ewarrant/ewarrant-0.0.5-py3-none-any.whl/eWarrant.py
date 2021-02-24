import boto3
import json
import os
from uuid import uuid4
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

class eWarrant:

    cbucket = 'ephod-tech.trading-advisor.auto-trade.tw.credentials'
    kbucket = 'ephod-tech.trading-advisor.auto-trade.tw.key'

    def __init__(self, key, credential, kbucket=kbucket, cbucket=cbucket):

        self.cbucket = cbucket
        self.kbucket = kbucket
        self.key = key 
        self.credential = credential

        print(self)
        s3 = boto3.client('s3') 
        s3.download_file(self.kbucket, self.key, self.key)
        s3.download_file(self.cbucket, self.credential, self.credential)

        encyption_key = open(self.key,'rb').read()
        f = Fernet(encyption_key)
        j = json.load(open(self.credential,'rb'))

        self._username = f.decrypt(str.encode(j['username'], 'utf-8')).decode('utf-8')
        self._password = f.decrypt(str.encode(j['password'], 'utf-8')).decode('utf-8')
        self._capassword = f.decrypt(str.encode(j['ca_password'], 'utf-8')).decode('utf-8')
    
    def username(self):
        return self._username 

    def password(self):
        return self._password 

    def ca_password(self):
        return self._capassword    
