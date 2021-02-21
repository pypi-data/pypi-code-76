import requests
from slacker import Slacker
import datetime as dt
from google.cloud import storage
import pymysql
from selenium.common.exceptions import NoSuchElementException
import linecache
import sys
import inspect
import pathlib
import json
import time
import os


class airtableToolbox:
    def __init__(self, base, apiKey):
        self.base = base
        self.apiKey = apiKey
        self.airtableURL = 'https://api.airtable.com/v0/{}'.format(base)
        self.airtableHeaders = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(apiKey)}

    def create_dictionary(self, url, baseName, reverse=False, *args):
        _dict = {}
        _dict_reverse = {}
        atURL = url

        while True:
            print(atURL)
            r = requests.get(atURL, headers=self.airtableHeaders).json()
            if len(r) != 0:
                for rec in r['records']:
                    try:
                        _items = []
                        _name = str(rec['fields'][baseName]).strip()
                        for a in args:
                            try:
                                _items.append(str(rec['fields'][a]).strip())
                            except:
                                _items.append('N/A')

                        if reverse:
                            _items.insert(0, _name)
                            _dict_reverse[rec['id']] = _items
                        else:
                            _items.insert(0, rec['id'])
                            _dict[_name] = _items

                    except KeyError:
                        pass

                try:
                    offset = r['offset']
                    if '?' in url:
                        atURL = '{}&offset={}'.format(url, offset)
                    else:
                        atURL = '{}?offset={}'.format(url, offset)
                except KeyError:
                    break
                except Exception:
                    break
            else:
                if reverse:
                    _dict_reverse = {}
                else:
                    _dict = {}
                break
        if reverse:
            return _dict_reverse
        else:
            return _dict

    def clean_list_string(self, str):
        str = str.replace('[', '').replace("'", '').replace(']', '')
        return str

    def api_request(self, url, payload, method=None):
        r = requests.request(method, url, data=payload, headers=self.airtableHeaders)
        return r

    def push_data(self, url, payload, patch=True):
        try:
            if patch:
                r = requests.patch(url, payload, headers=self.airtableHeaders)
            else:
                r = requests.post(url, payload, headers=self.airtableHeaders)
            statCode = r.status_code
        except requests.exceptions.HTTPError as e:
            return e
        return statCode

    def table_duplicate_check(self, url, baseName):
        _list = []
        _dup_list = []
        atURL = url

        while True:
            print(atURL)
            r = requests.get(atURL, headers=self.airtableHeaders).json()
            if len(r) != 0:
                for rec in r['records']:
                    try:
                        _item = str(rec['fields'][baseName]).strip()
                        if _item not in _list:
                            _list.append(_item)
                        else:
                            _dup_list.append(_item)
                    except KeyError:
                        pass

                try:
                    offset = r['offset']
                    if '?' in url:
                        atURL = '{}&offset={}'.format(url, offset)
                    else:
                        atURL = '{}?offset={}'.format(url, offset)
                except KeyError:
                    break
                except Exception:
                    break
        if len(_dup_list) == 0:
            return 'No duplicates found on\n----table: {}\n----column: {}'.format(url, baseName)
        else:
            return 'The following duplicates found on\n----table: {}\n----column: {}'.format(url, _dup_list)

    def create_list(self, url, _column):
        airtableURL = url
        _list = []

        while True:
            print(airtableURL)
            r = requests.get(airtableURL, headers=self.airtableHeaders).json()
            if len(r) != 0:
                for rec in r['records']:
                    try:
                        _list.append(rec['fields'][_column])
                    except KeyError:
                        pass

                try:
                    offset = r['offset']
                    if '?' in url:
                        airtableURL = '{}&offset={}'.format(url, offset)
                    else:
                        airtableURL = '{}?offset={}'.format(url, offset)
                except KeyError:
                    break
                except Exception:
                    break
        return _list

    def get_json(self, url):
        airtableURL = url
        _list_json = []

        while True:
            print(airtableURL)
            r = requests.get(airtableURL, headers=self.airtableHeaders).json()
            for rec in r['records']:
                _list_json.append(rec)

            try:
                offset = r['offset']
                if '?' in url:
                    airtableURL = '{}&offset={}'.format(url, offset)
                else:
                    airtableURL = '{}?offset={}'.format(url, offset)
            except KeyError:
                break
            except Exception:
                break
        return _list_json

    def create_url(self, url_base):
        return '{}/{}'.format(self.airtableURL, url_base)

    def get_ids(self, table, column_name):
        if '?' in table:
            url = "{base_url}/{table}&sort[0][field]={column_name}&sort[0][direction]=desc&fields[]={column_name}".\
                format(base_url=self.airtableURL, table=table, column_name=column_name)
        else:
            url = "{base_url}/{table}?sort[0][field]={column_name}&sort[0][direction]=desc&fields[]={column_name}".\
                format(base_url=self.airtableURL, table=table, column_name=column_name)
        atURL = url
        _dict = {}

        while True:
            print(atURL)
            r = requests.get(atURL, headers=self.airtableHeaders).json()
            for row in r['records']:
                _id = row['id']
                poName = row['fields']['PO Name']
                _dict[_id] = poName

            try:
                offset = r['offset']
                if '?' in url:
                    atURL = '{}&offset={}'.format(url, offset)
                else:
                    atURL = '{}?offset={}'.format(url, offset)
            except KeyError:
                break
            except Exception:
                break

        _list_po = _dict
        _dict = {}
        for po in _list_po:
            _list = []
            key = _list_po.get(po)
            value = po
            if key in _dict:
                # get _dict _list, append value to _list
                _list_new = _dict.get(key)
                _list_new.append(value)
                _dict[key] = _list_new
                _list_new = []
            else:
                # add key to _dict and create new list
                _list_new = []
                _list_new.append(value)
                _dict[key] = _list_new
                _list_new = []
        return _dict

    def delete_ids(self, _table, _list_id):
        """
        Please note that the script can only handle a max of 10 IDs
        """
        _list_id = ['records[]={}'.format(_id) for _id in _list_id]
        if len(_list_id) > 10:
            raise Exception('Function NathanJamesToolbox.airtableToolbox.delete_ids can only handle a max of 10 IDs.')

        url = '{}/{}?{}'.format(self.airtableURL, _table, '&'.join(_list_id))
        r = requests.request('DELETE', url, headers=self.airtableHeaders)
        return r


class slackToolbox:
    def __init__(self, _key, _channel):
        self._key = _key
        self._channel = _channel

    def send_message(self, funcName=None, errorDesc=None):
        try:
            _inspect = inspect.stack()[1][0]
            elems = str(_inspect).split(',')
            print(elems)

            caller = elems[1]
            caller = str(caller[6:-1]).strip()

            _line = str(elems[2]).strip()

            if funcName is None:
                caller_func = str(elems[3])
                caller_func = caller_func.replace('code', '').strip()
                caller_func = caller_func[:-1]
            else:
                caller_func = funcName

            if caller.rfind('/', 0, caller.rfind('/')) <= 0:
                pass
            else:
                index_ = caller.rfind('/', 0, caller.rfind('/'))
                caller = caller[index_:]
        except Exception:
            caller = '__process__'
            _line = '__line__'
            caller_func = 'n/a'

        _message = 'Python File: {}\n' \
                   'Function Name: {}\n' \
                   'Error Description: \n' \
                   '-- Error on {}\n-- {}\n{}'.format(caller, caller_func, _line, errorDesc, '=' * 100)

        # print(_message)
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)

    def send_booking_confirmation(self, funcName, description):
        _message = 'Python File: {}\n' \
                   'Function Name: {}\n' \
                   'Description: {}'.format(__file__, funcName, description)
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)

    def send_warning(self, pyfile=__file__, funcName=None, description=None):
        _message = 'Python File:\n\t\t{}\n' \
                   'Function Name:\n\t\t{}\n' \
                   'Description:\n\t\t{}\n{}'.format(pyfile, funcName, description, '=' * 100)
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)

    def send_warning_steps(self, pyfile=__file__, funcName=None, warning=None, steps=None):
        _message = 'Script File Name:\n\t\t{} > {}\n' \
                   'Error Message:\n\t\t{}\n' \
                   'Next Steps:\n\t\t{}\n{}'.format(pyfile, funcName, warning, steps, '=' * 100)
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)


class pdfFillerToolbox:
    def __init__(self, baseURL, downloadPath):
        self.baseURL = baseURL
        self.downloadPath = downloadPath
        # self.postHeaders = {'content-type': 'application/json',
        #                     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjgwNThiOTFhYTE5MDViZGJhNmNmZ'
        #                                      'TIwZTI0ZmFiYjBlNTc5MDNlYjE4MWM4N2UzNGEzYjVhOTc4ZGJkM2E4YTg2YjUwM2EwNTkwNzk3ZWZkIn0.'
        #                                      'eyJhdWQiOiIwIiwianRpIjoiODA1OGI5MWFhMTkwNWJkYmE2Y2ZlMjBlMjRmYWJiMGU1NzkwM2ViMTgxYzg'
        #                                      '3ZTM0YTNiNWE5NzhkYmQzYThhODZiNTAzYTA1OTA3OTdlZmQiLCJpYXQiOjE1NzM1MzY0NDMsIm5iZiI6MT'
        #                                      'U3MzUzNjQ0MywiZXhwIjoxNjA1MTU4ODQzLCJzdWIiOiIyMDYxMjU0MjUiLCJzY29wZXMiOltdfQ.ffahz4f'
        #                                      '-INxOYoKqoBMcfLQDmTRRE8s9pTY_PWLiU7A5BnmlZI0fz6ch6bfnENlB00BXO7XLaVRZiMmSp2HmHP_X0u'
        #                                      'bl76horv8eGrnYwB21Sldr9M4YL0as-fg6fa65Za9jS2iXfkQyhnMXKmoC4_bbEbGT3wtFGl9sFhaJJ_'
        #                                      'tAbkS9lOkBCxwKFiR61girhocWYEAAlnJDqwYUk3E-L4k3QfVBZphLb9FVEWm_woWzixrmHBeVI6h1ymjHd'
        #                                      'MndV5ctDMU5CCBvISodcr9aMaDzIukHWxHqDNb1DTtYqtO7yPXkjvlfuvPABeD4xHyH5KPOxFqt0tSOaJmU'
        #                                      'J5xGh0vh_SV_FwtLDVizg4ALrnWGu5BNoVWnmo7sy9YKgU3LEm0mzr--j6mW4TC_Aw8y6eXE5uAc1p5wiZP'
        #                                      '1OnfGYG3a8ZEaY-F7ZopR_KXJyf-oHWoZh9--8BHZgffiGz1_cuVcq8leMhf5R3etLlwrPDbt-kYcVkXFFb'
        #                                      'npM2fxQqYxPPUhas2U9q9A9q3x8KXSRdm7efurFVIe_gWCrqL1_DQ52FzphyRzANxqzoCvM4EsAU-t1B0Dd'
        #                                      'VZ6ybtQ3h3aneZaNnFdG3zv3Zm7BQqAY_IGhM7Wlq2GkM9nbz2A-Sc6K6cwIskXdvqF2acXNyXWXGXlSD3L'
        #                                      'YI-FicJ0RoM8DtU'}
        self.postHeaders = {'content-type': 'application/json',
                            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjA2NWZhNWRiNjE4Mjc2ZDllMTIwM'
                                    'jAxMDU4NWVkNmIwYThlMjJjNTY0YzhmODhkNzk4OWI4NjNmNTZhZTE2ZjcxZWQ2YWM1NTQ3NDI3NTlmIn'
                                    '0.eyJhdWQiOiIwIiwianRpIjoiMDY1ZmE1ZGI2MTgyNzZkOWUxMjAyMDEwNTg1ZWQ2YjBhOGUyMmM1NjR'
                                    'jOGY4OGQ3OTg5Yjg2M2Y1NmFlMTZmNzFlZDZhYzU1NDc0Mjc1OWYiLCJpYXQiOjE2MDU1Mzc4MTYsIm5i'
                                    'ZiI6MTYwNTUzNzgxNiwiZXhwIjoxNjM3MDczODE2LCJzdWIiOiIyMDYxMjU0MjUiLCJzY29wZXMiOltdf'
                                    'Q.YzEozJovS5cvfmjY7rAowRC70yQS77znPlSQGrwcKwYtoxSd0tKmqG4rHxL32UKrV5BX_pAaGKA5y0h'
                                    'OPAl5CyrYB43IZLM_BHCUHAFszcSCV0LQpyFmNMAnHYkP-KGDzyAANpybxjX1JdMUkhWG54wIkPV4bnit'
                                    'GG11GzpvuKAaW8ODPobWSNxyq_1UjPns4E1l_1Eqj3RuBhem183hgU35PbTfPKOyjWt5EIxW4B1aXVYuX'
                                    'wxS3iaYyTeVnfuqEqZs5rxLUA9JAjYXgG9rDWi8ycgCGI_bze0kQY4vqiheVNdV6fXXh9AoQYwiMZ4JAq'
                                    'gKP3jZE5PZWyAHgjOMcHSGId3a6DP46G5yQoNoVf1umuCsQcLcm4147FjdVZY7cXmhaR1cLE4V604tvUk'
                                    'tP6eSJPgNizjessZ1HsFSca34llFgVx2dJQ8px07zBGLZumgH6HY6f1IHCgJ08o0JmagtHueHuKVLVhz5'
                                    'QWB9D_8v5t--x7G9_42LTCnClvSeXjYdb3fOSpT0kF4wNzfPNMwQv3s-2mg23GhumxfW0IsOjDhhCLu0X'
                                    'fFW0770HbYNQ5-Kj6k2LTjSD3rll33bn1DrKJArZfr_2nckqZGpswCC_y_zNnl40XIwb0IBxMZGTmz6WB'
                                    'GUMiS0-R0PHghEi9KA7_0E6cT0sVkTbGoibP0'}
        self.downloadHeaders = {'content-type': 'application/json',
                                'Authorization': 'Bearer fXVIj4MZeHAahieugwzygN9dKkRXEklAwH98AfD8'}

    def postJSON(self, templateID, pl):
        data = requests.post('{}{}'.format(self.baseURL, templateID), pl, headers=self.postHeaders).json()
        return data

    def pdf_download(self, docID, docName):

        url = 'https://api.pdffiller.com/v1/document/' + str(docID) + '/download/'
        r = requests.get(url, headers=self.downloadHeaders)
        fName = '{}\\{}.pdf'.format(self.downloadPath, docName)
        # fName = os.path.join(self.downloadPath, '{}.pdf'.format(docName))
        with open(fName, 'wb') as f:
            f.write(r.content)
        print('Documnet downloaded from PDFfiller. Local path =', fName)

    def checkAvail_Format(self, _json, _data, _type):
        try:
            _data = _json['fields'][_data]
            if type(_data) is list:
                _data = _data[0]
        except KeyError:
            return ''

        if _type == 'date':
            try:
                _data = dt.datetime.strptime(_data, '%Y-%m-%d')
                _data = dt.datetime.strftime(_data, '%m/%d/%Y')
            except KeyError:
                _data = ''
        elif _type == 'str':
            try:
                _data = _data
            except KeyError:
                _data = ''
            except TypeError:
                _data = ''
        elif _type == 'float':
            try:
                _data = round(_data, 3)
                _data = '{:,.2f}'.format(_data)
            except KeyError:
                _data = ''
        elif _type == 'int':
            try:
                _data = int(_data)
                _data = '{:,}'.format(_data)
            except KeyError:
                _data = ''
        else:
            print('invalid _type')
        return _data


class googleCloudStrorageToolbox:
    def __init__(self, keyFile, downloadPath):
        self.keyFile = keyFile
        self.downloadPath = downloadPath

    def upload_to_bucket(self, blob_name, path_to_file, bucket_name):
        """ Upload data to a bucket"""
        storage_client = storage.Client.from_service_account_json(self.keyFile)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(path_to_file)
        return blob.public_url

    def list_blobs(self, bucket_name):
        """Lists all the blobs in the bucket."""
        # bucket_name = "your-bucket-name"

        # storage_client = storage.Client()
        storage_client = storage.Client.from_service_account_json(self.keyFile)

        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(bucket_name)
        gcpFileList = []

        for blob in blobs:
            # print(blob.name)
            gcpFileList.append(blob.name)

        return gcpFileList

    def upload_file(self, gcpFilename, gcpBucketName):
        # Upload file to GCP
        print('Uploading to Google Cloud Storage...')
        filePath = '{}{}'.format(self.downloadPath, gcpFilename)
        uploadURL = self.upload_to_bucket(gcpFilename, filePath, gcpBucketName)
        return uploadURL


class mySQLToolbox:
    def __init__(self, sqlPath, host, user, password, db):
        self.sqlPath = sqlPath
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def readQuery(self, qry, _type):
        if _type == 'f':
            with open('{}{}'.format(self.sqlPath, qry), 'r') as f:
                fString = f.read()
        elif _type == 'q':
            fString = qry
        else:
            raise Exception('Invalid readFile type.')

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        cursor.execute(fString)
        data = cursor.fetchall()
        db.close()

        return data

    def runQuery(self, qry):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()

        try:
            # Execute the SQL command
            cursor.execute(qry)
            db.commit()
            return 'Passed'
        except Exception as e:
            db.rollback()
            return 'Failed', e
        finally:
            db.close()

    def create_log(self, logType='log', log_=None, logMode='Testing', sessionID=None):
        if log_ is None or logMode == 'Testing' or sessionID is None:
            # Invalid log
            return

        type_ = {
            'e': 'Error',
            'err': 'Error',
            'error': 'Error',
        }

        logType = type_.get(logType.lower())
        if logType is None:
            logType = 'Log'

        module = inspect.getmodule(inspect.stack()[1][0])
        module_ = str(module)[str(module).find("'") + 1:]
        module_ = module_[:module_.find("'")]
        filename = str(module.__file__)
        filename = filename[filename.rfind('/') + 1:].replace('.py', '')
        sessionID = '{}{}'.format(filename.lower(), sessionID)

        log_ = '("{}", "{}", "{}", "{}", "{}", "{}")'.format(sessionID, dt.datetime.utcnow(), filename, module_,
                                                             logType, log_)
        log_ = 'INSERT INTO NathanJames_Monitoring.logs ' \
               '(session_id, datetime, scriptName, function, type, description) VALUES {}'.format(log_)
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()

        try:
            # Execute the SQL command
            cursor.execute(log_)
            db.commit()
            return 1
        except Exception as e:
            db.rollback()
            return 0, e
        finally:
            db.close()

    def stringfy(self, _string):
        if _string is None or _string == '' or _string == 'None':
            return 'NULL'
        else:
            return '"{}"'.format(str(_string))

    def convert_date(self, dateString, fromFormat, toFormat):
        if dateString is None:
            return 'NULL'
        else:
            dateString = dt.datetime.strptime(dateString, fromFormat)
            return self.stringfy(dt.datetime.strftime(dateString, toFormat))


class FlexportToolbox:
    def __init__(self, token, version=2):
        self.base_url = 'https://api.flexport.com/'
        self.token = token
        self.version = version
        self.headers = {
            'Authorization': 'Token token="%s"' % self.token,
            'Content-Type': 'application/json; charset=utf-8',
            'Flexport-Version': '{}'.format(version)
        }

    def get_json_list(self, endpoint, **kwargs):
        params = []
        page_specific = False
        for idx, k in enumerate(kwargs, start=1):
            page_specific = True if k == 'page' else page_specific
            params.append('='.join([str(k), str(kwargs.get(k))]))
        base_url = '?'.join([''.join([self.base_url, endpoint.replace('/', '')]), '&'.join(params)])

        if page_specific:
            print(base_url)
            data = requests.request('GET', url=base_url, headers=self.headers)
            if data.status_code != 200:
                return data, []

            if self.version == 1:
                return data, data.json()['records']
            elif self.version == 2:
                return data, data.json()['data']['data']
            else:
                return 'Invalid API version'

        page = 0
        list_json = []
        while True:
            page += 1
            url = '&'.join([base_url, 'page={}'.format(page)])
            print(url)
            data = requests.request('GET', url=url, headers=self.headers)
            if data.status_code != 200:
                return data, []

            json = data.json()

            if self.version == 1:
                if len(json['records']) == 0:
                    break

                [list_json.append(i) for i in json['records']]
            elif self.version == 2:
                [list_json.append(i) for i in json['data']['data']]

                if json['data']['next'] is None:
                    break
            else:
                return 'Invalid API version'

        return data, list_json

    def get_json(self, endpoint, **kwargs):
        if 'api.flexport.com' not in endpoint:
            url = '{}{}'.format(self.base_url, endpoint)
        else:
            url = endpoint

        parameters = '&'.join(['{}={}'.format(i[0], i[1]) for i in list(kwargs.items())])
        url = '?'.join([url, parameters]) if len(kwargs) != 0 else url

        list_json = []
        if self.version == 1:
            print(url)
            r = requests.request('GET', url, headers=self.headers)
            page_result = r.json()
            list_json.append(page_result['data']['data'])
        elif self.version == 2:
            while True:
                print(url)
                r = requests.request('GET', url, headers=self.headers)
                page_result = r.json()
                list_json.extend(page_result['data']['data'])
                url = page_result['data']['next']
                if url is None:
                    break

        return list_json

    def post_payload(self, endpoint, payload, *args):
        url = '{}{}'.format(self.base_url, endpoint)
        if len(args) != 0:
            url += '?'
            for arg in args:
                url += arg + '&'
            url = url[:-1]
        return requests.post(url, data=payload, headers=self.headers)

    def check_version(self, url):
        r = requests.get(url, headers=self.headers).json()
        try:
            ver = r['version']
        except KeyError:
            ver = 1
        return ver

    def create_dictionary(self, endpoint, *args):
        url = '{}{}'.format(self.base_url, endpoint)
        ver = self.check_version(url)
        _dict_id = {}
        if ver == 2:
            while True:
                print(url)
                data = requests.get(url, headers=self.headers).json()
                for r in data['data']['data']:
                    _list_args = []
                    id_ = r['id']
                    for arg in args:
                        _list_args.append(r[arg])
                    _dict_id[id_] = _list_args
                # if ver == 1 or 'page=' in url:
                #     return _dict_id
                url = data['data']['next']
                if url is None:
                    return _dict_id


class Cin7Toolbox:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.baseURL = 'https://api.cin7.com/api/v1/'

    def get_json(self, endpoint):
        jsonURL = '{}{}'.format(self.baseURL, endpoint)
        if 'page=' in jsonURL:
            print(jsonURL)
            r = requests.get(jsonURL, auth=(self.username, self.password))
            if r.status_code != 200:
                return r
            elif isinstance(r, str):
                raise Exception(r)
            else:
                return r.json()
        else:
            # loop all pages
            jsonAll = []
            pg = 0
            string_instance_counter = 0
            while True:
                string_instance_counter += 1
                pg += 1
                url = jsonURL + '&page={}'.format(pg) if '?' in jsonURL else jsonURL + '?page={}'.format(pg)
                print(url)

                data = requests.get(url, auth=(self.username, self.password))
                time.sleep(1)

                if isinstance(data, str):
                    if string_instance_counter >= 50:
                        raise Exception(data)
                    continue

                if data.status_code != 200:
                    return data

                if len(data.json()) != 0:
                    for r in data.json():
                        jsonAll.append(r)
                else:
                    break
            return jsonAll


class FreshdeskToolbox:
    def __init__(self, key):
        self.base_url = 'https://bluefyn.freshdesk.com/api/v2/'
        self.key = key
        self.auth_ = (self.key, '')

    def create_list(self, endpoint, *args):
        pg = 0

        url = 'https://bluefyn.freshdesk.com/api/v2/{}'.format(endpoint)

        _list_generic = []
        totalData = 0
        while True:
            if 'page=' in url:
                reqURL = url
            else:
                pg += 1
                reqURL = '{}?page={}'.format(url, pg) if '?' not in url else '{}&page={}'.format(url, pg)

            print(reqURL)

            while True:
                data = requests.get(reqURL, auth=self.auth_)
                if data.status_code == 429:
                    print('\n')
                    print('{} {} - Retrying...'.format(data.status_code, data.reason))
                    time.sleep(60)
                else:
                    data = data.json()
                    break

            totalData += len(data)

            if 'search' not in url:
                if len(data) == 0:
                    break
                for r in data:
                    _list_arg = []
                    for arg in args:
                        _list_arg.append(r[arg])
                    _list_generic.append(_list_arg)
            else:
                if len(data.get('results')) == 0:
                    break
                for r in data.get('results'):
                    _list_arg = []
                    for arg in args:
                        _list_arg.append(r[arg])
                    _list_generic.append(_list_arg)

            if 'page=' in url:
                break
        return _list_generic

    def get_json(self, endpoint):
        url = '{}{}'.format(self.base_url, endpoint)
        return requests.get(url, auth=self.auth_).json()


class Price2SpyToolbox:
    def __init__(self, key):
        self.key = key
        self.base_url = 'https://api.price2spy.com/rest/v1/'
        self.headers = {'content-type': 'application/json', 'Authorization': self.key}

    def getCurrentPricing(self, **kwargs):
        url = '{}get-current-pricing-data'.format(self.base_url)
        numType = ['active', 'brandId', 'categoryId', 'productId', 'supplierId']
        payload = ''

        for k in kwargs:
            if k in numType:
                payload += '"{}": {},'.format(k, kwargs.get(k))
            else:
                payload += '"{}": "{}",'.format(k, kwargs.get(k))

        payload = '{%s}' % payload[:-1]

        r = requests.post(url, headers=self.headers, data=payload)
        return r.json()


class SaddleCreekToolbox:

    class SaddleCreekSFTP:
        def __init__(self, _hostname, _username, _password):
            self._hostname = _hostname
            self._username = _username
            self._password = _password

        def get_sftp_data(self, source_path, source_filename, dest_filename_path):
            import pysftp

            myHostname = self._hostname
            myUsername = self._username
            myPassword = self._password

            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
                print("Connection succesfully stablished ... ")
                sftp.cwd(source_path)
                sftp.get(source_filename, dest_filename_path)


class MiscToolbox:
    def getWeek(self):
        return abs(int((dt.datetime.utcnow() - dt.datetime(2017, 9, 3)).days / 7)) - 1

    def check_exists_by_xpath(self, driver, xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

    def get_key(self):
        module = inspect.getmodule(inspect.stack()[1][0])
        # path_ = str(module)[str(module).find("from '") + 6:-2]
        path_ = pathlib.Path(module.__file__).parent.absolute()
        path_ = str(path_).replace('\\', '/')
        print(path_)
        while True:
            index_ = path_.rfind('/')
            if index_ >= 0:
                path_ = path_[:index_]
                filename = path_ + '/key/key.json'
                if pathlib.Path(filename).is_file():
                    break
            else:
                print('!!! Key file missing !!!')
                raise Exception('!!!CRITICAL!!! Key file is missing')
        with open(filename, 'r') as f:
            key = f.read()
            key = json.loads(key)
        return key

    def divide_list(self, _list, n):
        for i in range(0, len(_list), n):
            yield _list[i:i + n]

    def convert_to_json(self, value):
        value = value.strip(',')
        value = eval(value)
        return json.dumps(value)

    def get_eom(self, base_date):
        if not isinstance(base_date, dt.datetime):
            raise Exception('Invalid datetime value: Expected valid datetime value')

        base_date = dt.datetime(year=base_date.year, month=base_date.month, day=1)
        base_end = base_date + dt.timedelta(days=32)
        eom = dt.datetime(year=base_end.year, month=base_end.month, day=1) - dt.timedelta(days=1)
        return eom
