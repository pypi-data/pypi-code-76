from azure.identity._credentials.managed_identity import ManagedIdentityCredential
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.datalake.store import lib
import pyodbc # Python interface for ODBC API         https://github.com/mkleehammer/pyodbc
import struct # Maps C struct to python bytes object  https://docs.python.org/3/library/struct.html
import pandas as pd
import os
from datetime import datetime
import logging


def unused():
    #azure_tenant_id=os.environ['AZURE_TENANT_ID']
    #print('TENANT_ID: ' + azure_tenant_id)
    #azure_client_id=os.environ['AZURE_CLIENT_ID']
    #print('AZURE_CLIENT_ID: ', azure_client_id)
    #azure_client_secret=os.environ['AZURE_CLIENT_SECRET']
    #print('AZURE_CLIENT_SECRET: ', azure_client_secret)



    #print('Getting token...')
    #token = lib.auth(tenant_id = azure_tenant_id, client_id = azure_client_id, client_secret = azure_client_secret)

    # Ref https://arunpant.com/technology/sql-user-context-rls-webapp/
    ################ BLACK MAGIC STARTS #########################
    #exptoken = b"";
    #for i in token:
    #    exptoken += bytes({i});
    #    exptoken += bytes(1);

    #tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;

    # Creating a connection
    #conn = pyodbc.connect(connstr, attrs_before = { 1256:tokenstruct });

    ############### BLACK MAGIC ENDS ############################
    #data = pd.read_sql('select top 10 * from files', conn)
    pass


def log_files(filetype, filename, url, status, message):
    try:
        load_dotenv(verbose=True, override=True)
    except:
        logging.info('Error in load_dotenv')

    server=os.environ['IMBALANCE_LOG_SERVER']
    #logging.info('SERVER: ' + server)
    database=os.environ['IMBALANCE_LOG_DATABASE']
    #logging.info('DATABASE: '+ database)
    username=os.environ['IMBALANCE_LOG_USERNAME']
    #logging.info('USERNAME: ' + username)
    password=os.environ['IMBALANCE_LOG_PASSWORD']
    #logging.info('PASSWORD: ' + password)

    now = datetime.now()
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()
    cursor.execute('insert into files(dt, filetype, filename, url, status, message) values(?, ?, ?, ?, ?, ?)', now, filetype, filename, url, status, message)
    connection.commit()


    # data = pd.read_sql('select top 10 * from files', connection)
    # print(data)