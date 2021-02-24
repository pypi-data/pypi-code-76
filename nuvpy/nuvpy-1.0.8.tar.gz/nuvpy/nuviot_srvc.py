import urllib3.request
import urllib.parse
import certifi
import os
import requests
from requests.exceptions import HTTPError

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email

from sendgrid.helpers.mail.attachment import Attachment
import base64
from sendgrid.helpers.mail.file_content import FileContent
from sendgrid.helpers.mail.file_type import FileType
from sendgrid.helpers.mail.file_name import FileName
from sendgrid.helpers.mail.disposition import Disposition
       
class NuvIoTResponse:
    def __init__(self, result):
        self.rows = result['model']
        self.nextParititonKey = result['nextPartitionKey']
        self.nextRowKey = result['nextRowKey']
        self.pageSize = result['pageSize']
        self.hasMoreRecords = result['hasMoreRecords']

class NuvIoTRequest:
    def __init__(self, path):
        self.path = path
        self.pageSize = 50
        self.nextRowKey = None
        self.nextPartitionKey = None
        self.startDate = None
        self.endDate = None
                                      
def get(ctx, path, content_type = "", pageSize=50):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token, 'x-pagesize' : str(pageSize)}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token, 'x-pagesize' : str(pageSize)}
       
    if(content_type != ""):
        headers['Accept'] = content_type
   
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    url = ctx.url + path
    r = http.request("GET", url, headers=headers, preload_content=False)
    
    responseJSON = ''
    for chunk in r.stream(32):
        responseJSON += chunk.decode("utf-8")

    r.release_conn()
    
    if r.status > 299:
        print('Failed http call, response code: ' + str(r.status))
        print('Url: ' + url)
        print('Headers: ' + str(headers))
        print(responseJSON)
        print('--------------------------------------------------------------------------------')
        print()
        raise Exception("Http non success code %d not complete request to %s" % (r.status, path))
   

    return responseJSON

def post_json(ctx, path, json):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token, 'Content-Type':'application/json'}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token, 'Content-Type':'application/json'}
    
    url = ctx.url + path

    encoded_data = json.encode('utf-8')
    
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('POST', url,
             headers=headers,
             preload_content=False,
             body=encoded_data)
    
    responseJSON = ''
    responseStatus = r.status
    for chunk in r.stream(32):
        responseJSON += chunk.decode("utf-8")
    
    r.release_conn()

    if responseStatus > 299:
        print('Failed http call, response code: ' + str(responseStatus))
        print('Url: ' + url)
        print('Headers: ' + str(headers))
        print(responseJSON)
        print('--------------------------------------------------------------------------------')
        print()
        raise Exception("Could not post JSON to %s" % path)

    return responseJSON  
  
def post_file(ctx, path, file_name):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token}

    url = ctx.url + path

    if(not os.path.isfile(file_name)):
        raise Exception("File %s does not exists" % file_name)    
    
    session = requests.Session()
    files = {'file': open(file_name, 'rb')}
    r = requests.post(url, headers = headers, files = files)
    if r.status_code > 299:
        print('Failed http call, response code: ' + str(r.status_code))
        print('Url: ' + url)
        print('Headers: ' + str(headers))
        print(r.text)
        print('--------------------------------------------------------------------------------')
        print()
        raise Exception("Error %d, could not upload %s to %s." % (r.status_code, file_name, path))  


def download_file(ctx, path, dest, accept = ""):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token}
       
    if(accept != ""):
        headers['Accept'] = accept
    
    url = ctx.url + path
    
    print("Downloading file: %s" % url)

    chunk_size = 65536
        
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request("GET", url, headers=headers, preload_content=False)
 
    if r.status > 299:
        print('Failed http %d url: %s' % (r.status, url))
        print('Headers: ' + str(headers))
        print('--------------------------------------------------------------------------------')
        print()
        r.release_conn()
        return False

    print('Headers: ' + str(r.headers))
    print('Headers: ' + str(r.headers["Content-Disposition"]))
    with open(dest, 'wb') as out:
        while True:
            data = r.read(65535)
            if not data:
                break
            
            out.write(data)
    r.release_conn()
    return True
 
   
def get_paged(ctx, rqst):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token, 'x-pagesize' : rqst.pageSize}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token, 'x-pagesize' : rqst.pageSize}    

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    url = ctx.url + rqst.path;
    r = http.request("GET", url, headers=headers, preload_content=False)
    responseJSON = ''
    for chunk in r.stream(32):
        responseJSON += chunk.decode("utf-8")

    r.release_conn()
    
    if r.status > 299:
        print('Failed http call, response code: ' + str(r.status))
        print('Url: ' + url)
        print('Headers: ' + str(headers))
        print(responseJSON)
        print('--------------------------------------------------------------------------------')
        print()
        return None
      

    return responseJSON