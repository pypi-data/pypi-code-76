import boto3
import json
import os
from uuid import uuid4
import datetime 
import time
import eWarrant
import shioaji as sj

# submit job for a batch job (uuid)
# key * credential uuid
# special role
# bunch of parameters

class eTestificatus:

    queue = 'ephod_shioaji_handles'

    def __init__(self, key, credential, certificate, queue=queue):
        self.key = key 
        self.credential = credential 
        self.certificate = certificate
        self.queue = queue 

        self.ew = eWarrant.eWarrant(key=self.key, credential=self.credential)
        self.username = self.ew.username()
        self.password = self.ew.password()
        self.ca_passwd = self.ew.username()
        self.shioaji = sj.Shioaji()
        self.shioaji.login(
            person_id=self.username, 
            passwd=self.password, 
            contracts_cb=lambda security_type: print(f'{repr(security_type)} fetch done.')
        )

    def place_order(self, stock_symbol, price, quantity, action, price_type, order_type):

        time_token = datetime.datetime.now().strptime('%Y%m%d%H%M%S')
        batch = boto3.client('batch')
        response = batch.submit_job(
            jobName=f'order_{stock_symbol}_{time_token}',
            jobQueue=self.queue,
            jobDefinition=self.certificate,
            containerOverrides={
                'environment': [
                    {
                        'name': 'username',
                        'value': self.username
                    },
                    {
                        'name': 'password',
                        'value': self.password
                    },
                    {
                        'name': 'ca_password',
                        'value': self.ca_password,
                    },
                    {
                        'name': 'stock_symbol',
                        'value': stock_symbol
                    },
                    {
                        'name': 'price',
                        'value': price
                    },
                    {
                        'name': 'quantity',
                        'value': quantity
                    },
                    {
                        'name': 'action',
                        'value': action
                    }, 
                    {
                        'name': 'price_type',
                        'value': price_type                        
                    },
                    {
                        'name': 'order_type',
                        'value': order_type
                    }
                ]
            }
        )
        
        print(response)