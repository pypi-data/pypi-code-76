from dotenv import load_dotenv
import pyodbc # Python interface for ODBC API         https://github.com/mkleehammer/pyodbc
import os
from datetime import datetime
import logging

def __get_connection():
    try:
        load_dotenv(verbose=True, override=True)
    except:
        logging.info('Error in load_dotenv')

    server=os.environ['IMBALANCE_LOG_SERVER']
    database=os.environ['IMBALANCE_LOG_DATABASE']
    username=os.environ['IMBALANCE_LOG_USERNAME']
    password=os.environ['IMBALANCE_LOG_PASSWORD']
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return connection

def log_files(filetype, filename, url, status, message):
    now = datetime.now()
    connection = __get_connection()
    cursor = connection.cursor()
    cursor.execute('insert into files(dt, filetype, filename, url, status, message) values(?, ?, ?, ?, ?, ?)', now, filetype, filename, url, status, message)
    connection.commit()

def log(severity, message):
    now = datetime.now()
    connection = __get_connection()
    cursor = connection.cursor()
    cursor.execute('insert into logs(dt, severity, message) values(?, ?, ?)', now, severity, message)
    connection.commit()

