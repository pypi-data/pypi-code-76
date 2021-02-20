import json
import pandas as pd
from datetime import timedelta

import xmltodict
from colorama import Fore

import yandexdirectpy.settings as settings
from yandexdirectpy.exceptions import *

USER = settings.USER
TOKEN = settings.TOKEN
AGENCY_ACCOUNT = settings.AGENCY_ACCOUNT


# class Table:
#     def __init__(self):
#         self.base_id = os.getenv('BASE_ID')
#         self.api_key = os.getenv('AIRTABLE_API_KEY')
#         self.name = os.getenv('TABLE_NAME')
#
#
# table = Table()

# def get_table():
#     base_id = table.base_id
#     airtable_token = table.api_key
#     table_name = table.name
#
#     airtable = Airtable(base_key=base_id, table_name=table_name, api_key=airtable_token)
#     return airtable


def set_agency(agency_account=None, ):
    global AGENCY_ACCOUNT

    # if table is None:
    # table = get_table()

    if agency_account is None and AGENCY_ACCOUNT is None:
        print(alert_string('Unset AgencyAccount'))
    elif agency_account is not None:
        AGENCY_ACCOUNT = agency_account
    return True


# def tech_auth(token: str, login: str = None, agency_account: str = None):
#     # tech block auth
#     global USER
#     global AGENCY_ACCOUNT
#
#     # check options
#     # if table is None:
#     #     table = get_table()
#
#     if login is None:
#         # login
#         if login is None and USER is not None:
#             login = USER
#
#         # agency
#         if agency_account is None and AGENCY_ACCOUNT is not None:
#             agency_account = AGENCY_ACCOUNT
#
#     # detect type of token object
#     if not isinstance(token, dict):
#         raise UnexpectetTokenError(msg='Token must be "dict" and contain "access_token"')
#
#     # detect of account type, agency or client
#     if agency_account is not None:
#         load_login = agency_account
#         is_agency = True
#     else:
#         load_login = login
#         is_agency = False
#     token = auth(token=token, login=load_login, is_agency=is_agency)
#
#     if 'error' in token:
#         # check for error
#         return {
#             'res': {},
#             'error': token['error']
#         }
#     else:
#         token = token['access_token']
#         return token


def parse_api_response(response):
    try:
        # convert bytes response to dict
        decoded = response.content.decode('utf-8').replace('reports:', '')
        json_obj = json.dumps(xmltodict.parse(decoded), ensure_ascii=False)
        # if 'reportDownloadError' in json_obj:
        #     data = json.loads(json_obj['reportDownloadError'])
        # else:
        data = json.loads(json_obj)
        return data
    except:
        return response


def dates_range(start, end, freq):
    dates = pd.date_range(start=start, end=end, freq=freq,)
    dates = dates.to_list()
    for i in dates:
        dates[dates.index(i)] = i.date()

    if end not in dates:
        dates.append(end)
        
    return dates

def is_run_list(task_list):
    int_list = []
    for future in task_list:
        int_list.append(int(not future.running()))
    return int_list

def convert_time(time: timedelta or str):
    if isinstance(time, timedelta):
        time = time.total_seconds()
    if time > 3600:
        time /= 3600
        time = f'{time} hours'
    elif time > 60:
        time /= 60
        time = f'{time} minutes'
    else:
        time = f'{time} seconds'
    return time


def wait_for_response_status():
    pass


def color_string(string):
    return f'{Fore.CYAN}{string}{Fore.WHITE}'


def alert_string(string):
    return f'{Fore.RED}{string}{Fore.WHITE}'


def success_string(string):
    return f'{Fore.GREEN}{string}{Fore.WHITE}'

data_types = {
    'CampaignName': str,
    'Impressions': str,
    'Clicks': str,
    'Cost': str,
    'Date': str,
    }