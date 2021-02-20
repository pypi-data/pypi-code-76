import json
import requests
import math
import pymysql
import datetime as dt
import sys
from slacker import Slacker
from skpy import Skype


class KonnektiveToolbox:
    def __init__(self, username, password):
        self.baseurl = 'https://api.konnektive.com/'
        self.username = username
        self.password = password

    def create_url(self, endpoint=None):
        if endpoint is not None:
            return '{}{}/query/?loginId={}&password={}'.format(self.baseurl, endpoint, self.username, self.password)
        else:
            raise Exception('Endpoint is not defined.')

    def get_json(self, url, method='GET', *args):
        arg = '&'.join(args)
        baseURL = '&'.join([url, arg])
        print('Base URL: {}\n'.format(baseURL))

        if 'page=' in arg:
            r = requests.request(method, baseURL)
            return r.json()

        _list = []
        page = 1
        while True:
            url = '&'.join([baseURL, 'page={}'.format(page)])
            _json = requests.request(method, url).json()
            totalResults = _json['message']['totalResults']
            resultsPerPage = _json['message']['resultsPerPage']
            maxPage = math.ceil(int(totalResults) / int(resultsPerPage))

            if page > maxPage:
                print('\n')
                return _list

            comp = int((page / maxPage) * 100)
            remain = 100 - comp
            sys.stdout.write('\rProcessing page {} of {}[{}{}]'.format(page, maxPage, '#' * comp, '.' * remain))
            sys.stdout.flush()

            for _data in _json['message']['data']:
                _list.append(_data)

            if maxPage != page:
                page += 1
            else:
                print('\n')
                return _list

    def checkIfNone(self, value, _type='STR'):
        if _type == 'STR' and value is not None:
            return '"{}"'.format(value)
        elif _type == 'INT' and value is not None:
            return value
        elif value is None:
            return 'NULL'
        elif _type == 'STR' and len(value) == 0:
            return 'NULL'
        else:
            return 'NULL'

    def remError(self, value):
        if value is None:
            return None

        errorChars = {
            '"': "'",
            '\\': '/',
            '\u200b': '',
            '\u2105': 'c/o',
            '\u0101': 'a'
        }

        for errorChar in errorChars:
            value = value.replace(errorChar, errorChars.get(errorChar))

        return value


class ClickBank:
    def __init__(self, base_url, endpoint, developer_key, clerk_key):
        self.base_url = base_url
        self.endpoint = endpoint
        self.developer_key = developer_key
        self.clerk_key = clerk_key
        self.headers = {'Accept': 'application/json', 'Authorization': f'{self.developer_key}:{self.clerk_key}'}

    def create_url(self, method, **params):
        url = f'{self.base_url}{self.endpoint}/{method}'.replace('//', '/').replace('https:/', 'https://')
        parameters = '&'.join([f'{param}={params[param]}' for param in params])
        return '?'.join([url, parameters])

    def get_json(self, url, get_all=True):
        page = 0
        headers = self.headers

        _list = []

        while True:
            page += 1
            headers['page'] = str(page)
            print(f'{url} - page: {page}')
            r = requests.get(url, headers=headers)
            _json = r.json()

            if 'orders2' in self.endpoint:
                if _json is not None:
                    for data in _json['orderData']:
                        _list.append(data)
                else:
                    break

                if not get_all:
                    break

            if 'analytics' in self.endpoint:
                try:
                    for data in _json['rows']['row']:
                        _list.append(data)
                except TypeError:
                    break

                if not get_all:
                    break

        return _list

    def check_if_null(self, _value, string=True):
        if _value is None:
            return 'NULL'

        if isinstance(_value, dict):
            _value = 'NULL'
        else:
            _value = f'"{_value}"' if string else _value

        return _value


class EarnwareToolbox:
    def __init__(self, userId):
        self.userId = userId
        self.headers = {'Content-Type': 'application/json'}

    def upload_to_contacts(self, url, payload):
        r = requests.post(url, payload, headers=self.headers)
        return r


class OntraportToolbox:
    def __init__(self, version=1, api_key='', api_appid=''):
        self.version = version
        self.api_key = api_key
        self.api_appid = api_appid
        self.base_url = 'https://api.ontraport.com/'
        self.headers = {'Api-Key': api_key, 'Api-Appid': api_appid}

    def get_request(self, endpoint, **kwargs):
        url = f'{self.base_url}{self.version}/{endpoint}'
        params = ''
        for kwarg in kwargs:
            params += f'{kwarg}={kwargs.get(kwarg)}&'

        url = f'{url}?{params[:-1]}' if len(kwargs) != 0 else url
        r = requests.get(url, headers=self.headers)
        print(f'Response: {r.status_code} {r.reason} | URL: {url}')
        return r

    def convert_date_to_epoch(self, _my_datetime):
        if isinstance(_my_datetime, dt.datetime):
            return _my_datetime.timestamp()
        else:
            raise Exception('Invalid datetime provided.')


class MySQLToolbox:
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

    def createQuery(self, table=None, values=None, dups=None):
        if table is None or values is None:
            raise Exception('Error in creating query. The following are required:\n\tTable Name\n\tValues')

        if dups is not None:
            return 'INSERT INTO {}.{} VALUES\n{}\nON DUPLICATE KEY UPDATE\n{}'.format(self.db, table, values, dups)
        else:
            return 'INSERT INTO {}.{} VALUES\n{}'.format(self.db, table, values)

    def stringfy(self, _string):
        if _string is None or _string == '' or _string == 'NULL' or _string == 'None':
            return 'NULL'
        else:
            if "'" in _string:
                _string = _string.replace("'", '\\"')
            return "'{}'".format(str(_string))

    def convert_date(self, dateString, fromFormat, toFormat):
        if dateString is None:
            return 'NULL'
        else:
            dateString = dt.datetime.strptime(dateString, fromFormat)
            return self.stringfy(dt.datetime.strftime(dateString, toFormat))

    def convert_unix_datetime(self, unix_int, _format='%Y-%m-%d %H:%M:%S'):
        if unix_int == '' or unix_int is None or unix_int == 0 or unix_int == '0':
            return 'NULL'

        try:
            unix_int = unix_int.replace("'", '') if "'" in unix_int else unix_int
            return dt.datetime.utcfromtimestamp(int(unix_int)).strftime(_format)
        except Exception as err:
            raise Exception(err)


class slackToolbox:
    def __init__(self, _key, _channel):
        self._key = _key
        self._channel = _channel

    def send_message(self, scriptname='-', funcname='-', description='-'):
        _message = 'Python File: {}\n' \
                   'Function Name: {}\n' \
                   'Description: {}'.format(scriptname, funcname, description)
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)

    def send_info(self, description='-'):
        _message = f'Information: {description}'
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)


class SkypeToolbox:
    def __init__(self, username, password, channel):
        self.username = username
        self.password = password
        self.channel = channel
        self.sk = Skype(username, password)
        self.channel = self.sk.chats.chat(self.channel)

    def send_message(self, filename=None, function=None, message=None):
        if filename is None or function is None or message is None:
            raise Exception('Please provide valid filename, function name, and message...')

        message_format = f'Filename:\n\t{filename}\n' \
                         f'Function Name:\n\t{function}\n' \
                         f'Description:\n\t{message}\n{"=" * 78}'
        self.channel.sendMsg(message_format)

    def send_report(self, report_name=None, message=None):
        if report_name is None or message is None:
            raise Exception('Please provide valid report_name and message...')

        message_format = f'***{report_name}***\n\n' \
                         f'{message}\n' \
                         f'{"=" * 78}'
        self.channel.sendMsg(message_format)


class ShopifyToolbox:
    def __init__(self, endpoint, auth):
        self.endpoint = endpoint
        self.auth = auth
        self.url = f'https://lexapure-nutrition.myshopify.com/admin/{endpoint}'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': auth
        }

    def get_request(self, **kwargs):
        params = []
        for kwarg in kwargs:
            params.append(f'{kwarg}={kwargs.get(kwarg)}')
        params = '&'.join(params)

        page_link = None
        _list_json = []

        while True:
            url = f'{self.url}?{params}' if page_link is None else page_link
            print(url)

            r = requests.request('GET', url, headers=self.headers)
            _dict_headers = r.headers

            json = r.json()

            for data in json['orders']:
                _list_json.append(data)

            link_dict = {}
            page_link = _dict_headers.get('Link')
            if page_link is not None:
                page_link = page_link.split(',')
                for link in page_link:
                    v, k = link.split(';')
                    k = k.strip().replace('"', '').replace('rel=', '')
                    link_dict[k] = v.strip()

                page_link = link_dict.get('next')
                if page_link is None:
                    break
                else:
                    page_link = page_link[1:-1]
            else:
                break

        return _list_json


class MondayToolbox:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.monday.com/v2'
        self.headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }


class MiscToolbox:
    def divide_list(self, _list, n):
        for i in range(0, len(_list), n):
            yield _list[i:i + n]

    def convert_to_json(self, value):
        value = value.strip(',')
        value = eval(value)
        return json.dumps(value)

