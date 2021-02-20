import datetime
import json
import time
from io import StringIO
from functools import reduce

import pandas as pd
import requests
import yandexdirectpy.settings as settings
from colorama import init
from yandexdirectpy.exceptions import *
from yandexdirectpy.utils import color_string, alert_string, success_string, convert_time, dates_range, is_run_list, parse_api_response, data_types
from yandexdirectpy.executors import execute_func_in_individual_thread
from itertools import cycle

USER = settings.USER
TOKEN = settings.TOKEN
AGENCY_ACCOUNT = settings.AGENCY_ACCOUNT

CLIENT_ID = '365a2d0a675c462d90ac145d4f5948cc'
CLIENT_SECRET = 'f2074f4c312449fab9681942edaa5360'

init()


def converter(o):
    # Convert datetime objects to str
    if isinstance(o, datetime.datetime):
        return o.__str__().split(' ')[0]


# def get_token(login: str = None, token_path=token_path()):
#     # Redirect user to webpage for getting a token and returns it
#     global TOKEN
#
#     webbrowser.open(f'https://oauth.yandex.ru/authorize?response_type=token&client_id={CLIENT_ID}')
#     token = {
#         'token_type': 'bearer',
#         'access_token': input('Enter your token: '),
#         'expires_in': 26715505,
#         'refresh_token': None,
#         'expires_at': datetime.datetime.now() + datetime.timedelta(seconds=26715505),
#     }
#
#     TOKEN = token
#
#     print(f'Do you want save API credential in local file {token_path}/{login}.json, for use it between sessions?')
#     ans = input('y / n (recomendation - y): ')
#     if ans.lower() in ['y', 'yes', 'ok', 'save']:
#         with open(f'{token_path}/{login}.json', 'w+') as f:
#             data = json.dumps({login: token}, indent=4, default=converter)
#             f.write(data)
#             f.close()
#         print(f'Token saved in file', color_string(f'{token_path}/{login}.json'))
#
#     return token

def send_api_request(query_body, headers: dict, field_names: list, current_login: str, skip_errors: bool = True):
    response = requests.post('https://api.direct.yandex.com/v5/reports', data=query_body, headers=headers)

    start_api_time = datetime.datetime.now()

    answer = parse_api_response(response)

    if str(response.status_code)[0] == '4':
        answer = answer["reportDownloadError"]
        print(alert_string(
            'Error in request parameters or limit on the number of requests or reports in the queue is exceeded. In this case, analyze the error message, correct the request and send it again.'))

        # parse error
        print(alert_string(f' > Request Id \n {answer["ApiError"]["requestId"]}'))

        print(alert_string(f' > Error Code \n {answer["ApiError"]["errorCode"]}'))

        print(alert_string(f' > Error Message \n {answer["ApiError"]["errorMessage"]}'))

        print(alert_string(f' > Error Detail \n {answer["ApiError"]["errorDetail"]}'))

        if answer["ApiError"]["errorCode"] == '54' or answer["ApiError"]["errorCode"] == 54:
            pass

        if not skip_errors:
            return {
                'res': {},
                'error': answer["ApiError"]["errorDetail"]
            }, True
        else:
            pass

    if response.status_code == 500:
        print(f'{current_login} - ')
        print(
            alert_string(
                'While generating the report an error occurred on the server. If for this report the error on the server occurred for the first time, try to generate a report again. If the error persists, contact support.'))

        if not skip_errors:
            error_detail = answer['reportDownloadError']['ApiError']['errorDetail']
            return {
                'res': {},
                'error': error_detail
            }, True
        else:
            pass

    if response.status_code == 201:
        # print(success_string('The report has been successfully queued for offline generation.'))
        print(alert_string('x'))
        return None, False

    if response.status_code == 202:
        print(alert_string('x'))
        return None, False

    wait_for_resp_s_time = datetime.datetime.now()

    if response.status_code == 500:
        return {
            'res': {},
            'error': 'While generating the report an error occurred on the server. If for this report the error on the server occurred for the first time, try to generate a report again. If the error persists, contact support.'
        }, True

    if response.status_code == 502:
        return {
            'res': {},
            'error': 'Request processing time exceeded server limit.'
        }, True

    waiting_time = datetime.datetime.now() - wait_for_resp_s_time

    parse_time = datetime.datetime.now() - start_api_time - waiting_time

    request_id = response.headers["RequestId"]

    # success message
    if response.status_code == 200:
        df_new = pd.read_csv(StringIO(str(response.content, 'utf-8')), sep='\t', names=field_names, dtype=data_types)
        df_new = df_new.drop([0])
        
        return {
            'res': df_new,
            'parse_time': parse_time,
            'request_id': request_id,
            'waiting_time': waiting_time,
        }, True

def get_report_fun(
        token: str,
        login: list,
        report_type: str = 'CUSTOM_REPORT',
        date_range_type: str = 'CUSTOM_DATE',
        date_from=datetime.date.today() - datetime.timedelta(days=31),
        date_to=datetime.date.today() - datetime.timedelta(days=1),
        field_names=None,
        filter_list=None,
        goals=None,
        attribution_models=None,
        include_vat: str = 'YES',
        include_discount: str = 'NO',
        agency_account=AGENCY_ACCOUNT,
        skip_errors=True
):
    # start time
    if field_names is None:
        field_names = ["CampaignName", "Impressions", "Clicks", "Cost", "Date"]

    # field names
    fields = ''.join([f'<FieldNames>{fil}</FieldNames>' for fil in field_names])

    # for limited accounts
    limit_reached = []

    # for time
    waiting_data = {}
    parsing_data = {}

    # request Ids
    request_id = {}

    # request list
    reqeust_list = []

    # filters
    if filter_list is not None:
        fil_list = None
        filt = filter_list
        for fil in filt:
            val = "".join(fil.split(" ")[0][2:len(fil.split(" ")[0])]).split(',| |;')[0]
            fil_list = ''.join([fil_list[fil_list is None],
                                f'<Filter><Field>{fil.split(" ")[0][0]}</Field>',
                                f'<Operator>{fil.split(" ")[0][1]}</Operator>',
                                f'<Values>{val}</Values></Filter>'
                                ])

    # goals and attributions
    goals = '' if goals is None else ''.join([f"<Goals>{goal}</Goals>" for goal in goals])

    # if AttributionModels is None:
    attribution_models = '' if attribution_models is None else ''.join(
        [f'<AttributionModels>{model}</AttributionModels>' for model in attribution_models])

    # compose request body
    query_body = ''.join([
        '<ReportDefinition xmlns="http://api.direct.yandex.com/v5/reports"><SelectionCriteria>',
        f'<DateFrom>{date_from}</DateFrom><DateTo>{date_to}</DateTo>' if date_range_type == 'CUSTOM_DATE' else '',
        fil_list if filter_list is not None else '',
        '</SelectionCriteria>',
        goals,
        attribution_models,
        fields,
        f'<ReportName>"MyReport {datetime.datetime.now()}"</ReportName>',
        f'<ReportType>{report_type}</ReportType>',
        f'<DateRangeType>{date_range_type}</DateRangeType>',
        f'<Format>TSV</Format>',
        f'<IncludeVAT>{include_vat}</IncludeVAT>',
        f'<IncludeDiscount>{include_discount}</IncludeDiscount>',
        '</ReportDefinition>'
    ])

    # result frame
    result = pd.DataFrame()

    for current_login in login:
        # auth
        token

        # start message
        print('-----------------------------------------------------------')
        print('Loading data by', color_string(current_login))

        # send request to API
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept-Language': 'ru',
            'skipReportHeader': 'true',
            'skipReportSummary': 'true',
            'Client-Login': current_login,
            'returnMoneyInMicros': 'false',
            'processingMode': 'auto',
        }

        send_api_request(query_body, headers, field_names, token, skip_errors=skip_errors)

        data, parsed = send_api_request(query_body=query_body, headers=headers, current_login=current_login, field_names=field_names, skip_errors=skip_errors)

        if not parsed:
            return None

        # check for errors
        if 'error' in data:
            return {
                'res': {},
                'error': data['error']
            }

        df_new = data['res']

        # check if there are APi limits
        if len(df_new.index) >= 1000000:
            print(alert_string(
                f'{color_string(current_login)}: You have reached the limits of Yandex.Direct API. Try to use "FetchBy" parameter with DateRangeType = "CUSTOM_DATE", "DateFrom" and "DateTo". If you are already using it, try to choose a smaller value.'))
            limit_reached.append(current_login)

            # request id
            request_id[current_login] = data['request_id']

            # convert dates
            if 'Date' in df_new.columns:
                df_new['Date'] = pd.to_datetime(
                    df_new['Date'],
                    format='%Y-%m-%d'
                )

            # add login
            df_new['Login'] = current_login

            # add to result
            result = result.append(df_new, ignore_index=True)

            # calc time
            parse_time = data['parse_time']

            waiting_time = convert_time(data['waiting_time'])
            parse_time = convert_time(data['parse_time'])

            waiting_data[current_login] = waiting_time
            parsing_data[current_login] = parse_time

        # end of cycle

    # check limits
    if len(limit_reached) > 0:
        print(
            f'Limit of 1 000 000 rows reached by next accounts: {",".join(color_string(login) for login in limit_reached)}')

    # tech messages
    print(f'')
    print(f'Number of rows is {color_string(len(result.index))}')
    print('-----------------------------------------------------------')

    # return result
    res = {
        'res': result,
        'time': {
            'waiting': waiting_data,
            'parsing': parsing_data,
        },
        'limit_reached': limit_reached,
        'request_id': request_id,
    }

    return res
        

def get_report(

        logins: list,
        token: str,
        report_type: str = 'CUSTOM_REPORT',
        date_range_type: str = 'CUSTOM_DATE',
        date_from=None,
        date_to=None,
        field_names=None,
        filter_list=None,
        goals=None,
        attribution_models=None,
        include_vat: str = 'YES',
        include_discount: str = 'NO',
        agency_account=AGENCY_ACCOUNT,
        fetch_by=None,
        skip_errors=False,
):
    # try:
    if field_names is None:
        field_names = ["CampaignName", "Impressions", "Clicks", "Cost", "Date"]

    if date_from is None:
        date_from = datetime.date.today() - datetime.timedelta(days=31)
    elif isinstance(date_from, str):
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()

    if date_to is None:
        date_to = datetime.date.today() - datetime.timedelta(days=1)
    elif isinstance(date_to, str):
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
    # if table is None:
    #     table = get_table()

    total_start_time = datetime.datetime.now()

    # for limited accounts
    limit_reached = []

    # for time records
    time_data = {}

    request_id = {}

    # FetchBy
    if fetch_by is not None:
        if (date_range_type != 'CUSTOM_DATE') and (date_from is None) and (date_to is None):
            raise FetchByDateError(
                'You should use "FetchBy" parameter only with DateRangeType "CUSTOM_DATE"'
                ' and existing DateFrom and DateTo.')
        else:
            # dates df
            dates = pd.date_range(start=date_from, end=date_to, freq=fetch_by)

            print(success_string('Batch processing mode is enabled.'))
            print(
                f'Fetching data by {color_string(fetch_by)}: from {color_string(date_from)} to {color_string(date_to)}.')
            print('')
    else:
        # dates df

        dates = dates_range(date_from, date_to, '365D')
        # list_cycle = cycle(dates)
        # next(list_cycle)
        # return dates

    # result
    result = pd.DataFrame()

    print('Processing', end=' ')

    while len(dates) >= 2:

        for i in dates[:-2]:
            d_from = i 
            d_to = dates[dates.index(i) + 1]

            data = get_report_fun(
                date_range_type=date_range_type,
                report_type=report_type,
                date_from=d_from,
                date_to=d_to,
                field_names=field_names,
                filter_list=filter_list,
                goals=goals,
                attribution_models=attribution_models,
                include_vat=include_vat,
                include_discount=include_discount,
                login=logins,
                agency_account=agency_account,
                token=token,
                skip_errors=skip_errors)

            if data is None:
                continue                

            if 'error' in data:
                return {
                    'res': {},
                    'error': data['error']
                }

            limit_reached += data['limit_reached']
            result = result.append(data['res'], ignore_index=True)
            time_data.update(data['time'])
            request_id.update(data['request_id'])

            dates.pop(dates.index(i))
        
        print('=', end='')
        time.sleep(15)

    # calc time
    total_time = (datetime.datetime.now() - total_start_time)
    total_time = convert_time(total_time)

    # logs
    if fetch_by is not None and len(limit_reached) == 0:
        print(success_string('Function with batch processing mode has executed successfully.'))

    elif len(limit_reached) > 0:
        limit_reached = set(limit_reached)

    # compile result

    res = {
        'res': result,
        'limit_reached': limit_reached,
        'total_time': total_time,
        'time': time_data,
        'rows_count': len(result.index),
        'request_id': request_id,
    }

    return res


# except Exception as e:
#     error_logger.error(msg=e.__str__())
#     return {
#         'res': {},
#         'error': e.__str__()
#     }


def get_client_list(token: str, agency_account: str = AGENCY_ACCOUNT):  
    token = token  

    # prepare query body
    query = {
        'method': 'get',
        'params': {
            'SelectionCriteria': {},
            'FieldNames': [
                "AccountQuality",
                "Archived",
                "ClientId",
                "ClientInfo",
                "CountryId",
                "CreatedAt",
                "Currency",
                "Grants",
                "Login",
                "Notification",
                "OverdraftSumAvailable",
                "Phone",
                "Representatives",
                "Restrictions",
                "Settings",
                "Type",
                "VatRate"
            ]
        }
    }

    # convert body to json format
    query_json = json.dumps(query)

    # set headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept-Language': 'ru',
    }

    # send HTTP query
    answer = requests.post('https://api.direct.yandex.com/json/v5/agencyclients', data=query_json, headers=headers)

    # check query for error
    answer_data = answer.json()

    # check answer for error
    if 'error' in answer_data:
        return {
            'res': {},
            'error': {
                'request_id': answer_data["error"]["request_id"],
                'error_code': answer_data["error"]["error_code"],
                'error_detail': answer_data["error"]["error_detail"],
                'error_sting': answer_data["error"]["error_string"]
            }
        }

    # result_data
    data = []

    for i in answer_data['result']['Clients']:
        data.append({
            'Login': i['Login'],
            'FIO': i['ClientInfo'],
            'StatusArch': i['Archived'],
            'DateCreate': i['CreatedAt'],
            'Role': i['Type'],
            'Email': i['Notification']['Email'],
            'Phone': i['Phone'],
            'Currency': i['Currency'],
            'VatRate': i['VatRate'],
            'ClientId': i['ClientId'],
            'CountryId': i['CountryId'],
            'AccountQuality': i['AccountQuality'] if 'AccountQuality' in i else None,
            'Grants': '; '.join(
                map(lambda x: f'{x["Agency"]}: {x["Privilege"]} - {x["Value"]}', i['Grants'])
            ),
            'Representatives': '; '.join(
                map(lambda x: f'{x["Login"]}: {x["Role"]}', i['Representatives'])
            ),
            'Restrictions': '; '.join(
                map(lambda x: f'{x["Element"]}: {x["Value"]}', i['Restrictions'])
            ),
            'Settings': '; '.join(
                map(lambda x: f'{x["Option"]}: {x["Value"]}', i['Settings'])
            ),
        })

    # binding to data frame
    data_total = pd.DataFrame(data)

    return data_total


def get_campaign(
        token: dict,
        logins: str = USER,
        states=None,
        types=None,
        statuses=None,
        statuses_payment=None,
        agency_account=AGENCY_ACCOUNT,
):
    # try:
    # check vars

    if statuses_payment is None:
        statuses_payment = ["DISALLOWED", "ALLOWED"]
    if statuses is None:
        statuses = ["ACCEPTED", "DRAFT", "MODERATION", "REJECTED"]
    if types is None:
        types = ["TEXT_CAMPAIGN", "MOBILE_APP_CAMPAIGN", "DYNAMIC_TEXT_CAMPAIGN", "CPM_BANNER_CAMPAIGN"]
    if states is None:
        states = ["OFF", "ON", "SUSPENDED", "ENDED", "CONVERTED", "ARCHIVED"]

    # result frame
    result = pd.DataFrame(
        columns=[
            'Name',
            'Type',
            'Status',
            'State',
            'StatusPayment',
            'SourceId',
            'DailyBudgetAmount',
            'DailyBudgetMode',
            'Currency',
            'StartDate',
            'Impressions',
            'Clicks',
            'ClientInfo',
            'FundsMode',
            'CampaignFundsBalance',
            'CampaignFundsBalanceBonus',
            'CampaignFundsSumAvailableForTransfer',
            'SharedAccountFundsRefund',
            'SharedAccountFundsSpend',
            'TextCampBidStrategySearchType',
            'TextCampBidStrategyNetworkType',
            'TextCampAttributionModel',
            'DynCampBidStrategySearchType',
            'DynCampBidStrategyNetworkType',
            'DynCampAttributionModel',
            'MobCampBidStrategySearchType',
            'MobCampBidStrategyNetworkType',
            'CpmBannerBidStrategySearchType',
            'CpmBannerBidStrategyNetworkType',
            'Login',
            'stringsAsFactors',
        ]
    )
    result['stringsAsFactors'] = False

    # filters

    states = ', '.join([f'\"{state}\"' for state in states])
    types = ', '.join([f'\"{type}\"' for type in types])
    statuses = ', '.join([f'\"{status}\"' for status in statuses])
    statuses_payment = ', '.join([f'\"{status}\"' for status in statuses_payment])

    # offset
    lim = 0

    # message
    print('Processing')

    while lim != 'stopped':
        query_body = {"method": 'get',
                      'params': {
                          "SelectionCriteria": {
                              "States": states,
                              "Types": types,
                              "StatusesPayment": statuses_payment,
                              "Statuses": statuses,
                          },
                          'FieldNames': [
                              'Id',
                              "Name",
                              "Type",
                              "StartDate",
                              "Status",
                              "StatusPayment",
                              "SourceId",
                              "State",
                              "Statistics",
                              "Funds",
                              "Currency",
                              "DailyBudget",
                              'ClientInfo',
                          ],
                          "TextCampaignFieldNames": ["BiddingStrategy", "AttributionModel"],
                          "MobileAppCampaignFieldNames": ["BiddingStrategy"],
                          "DynamicTextCampaignFieldNames": ["BiddingStrategy", "AttributionModel"],
                          "CpmBannerCampaignFieldNames": ["BiddingStrategy"],
                          "Page": {
                              "Limit": 1000,
                              "Offset": lim,
                          }
                      }
                      }

        query_body = json.dumps(query_body)

        for l in range(len(logins)):
            token = token  
            
            answer = requests.post("https://api.direct.yandex.com/json/v5/campaigns", data=query_body, headers={
                'Authorization': f'Bearer {token}',
                'Accept-Language': "ru",
                "Client-Login": logins[l]
            })

            # check answer status
            print(logins[l])
            data_raw = answer.json()

            if 'error' in data_raw:
                print(alert_string(f"{data_raw['error']['error_string']} - {data_raw['error']['error_detail']}"))
                if data_raw['error']['error_code'] == 54:
                    pass
                else:
                    return {
                        'res': {},
                        'error': data_raw['error']
                    }

            # parsing
            try:
                c_data = data_raw['result']['Campaigns']
                for i in range(len(c_data)):
                    d = c_data[i]
                    data = {
                        'Id': d['Id'],
                        'Name': d['Name'],
                        'Type': d['Type'],
                        'Status': d['Status'],
                        'State': d['State'],
                        'StatusPayment': d['StatusPayment'],
                        'SourceId': d['SourceId'] if 'SourceId' in d else None,
                        'DailyBudgetAmount': d['DailyBudgetAmount'][
                                                 'Amount'] / 1000000 if 'DailyBudgetAmount' in d and 'Amount' in d[
                            'DailyBudgetAmount'] else None,
                        'DailyBudgetMode': d['DailyBudgetMode']['Mode'] if 'DailyBudgetMode' in d and 'Mode' in d[
                            'DailyBudgetMode'] else None,
                        'Currency': d['Currency'],
                        'StartDate': d['StartDate'],
                        'Impressions': d['Statistics']['Impressions'] if 'Impressions' in d['Statistics'] else None,
                        'Clicks': d['Statistics']['Clicks'] if 'Clicks' in d['Statistics'] else None,
                        'ClientInfo': d['ClientInfo'],
                        'FundsMode': d['Funds']['Mode'],
                        'CampaignFundsBalance': d['Funds']['CampaignFunds'][
                                                    'Balance'] / 1000000 if 'CampaignFunds' in
                                                                            d[
                                                                                'Funds'] and 'Balance' in
                                                                            d['Funds'][
                                                                                'CampaignFunds'] else None,
                        'CampaignFundsBalanceBonus': d['Funds']['CampaignFunds'][
                                                         'BalanceBonus'] / 1000000 if 'CampaignFunds' in d[
                            'Funds'] and 'BalanceBonus' in d['Funds']['CampaignFunds'] else None,
                        'CampaignFundsSumAvailableForTransfer': d['Funds']['CampaignFunds'][
                                                                    'SumAvailableForTransfer'] / 1000000 if 'CampaignFunds' in
                                                                                                            d[
                                                                                                                'Funds'] and 'SumAvailableForTransfer' in
                                                                                                            d[
                                                                                                                'Funds'][
                                                                                                                'CampaignFunds'] else None,
                        'SharedAccountFundsRefund': d['Funds']['SharedAccountFunds'][
                            'Refund'] if 'SharedAccountFunds' in d[
                            'Funds'] and 'Refund' in d['Funds']['SharedAccountFunds'] else None,
                        'SharedAccountFundsSpend': d['Funds']['SharedAccountFunds'][
                            'Spend'] if 'SharedAccountFunds' in
                                        d[
                                            'Funds'] and 'Spend' in
                                        d['Funds'][
                                            'SharedAccountFunds'] else None,
                        'TextCampBidStrategySearchType': d['TextCampaign']['BiddingStrategy']['Search'][
                            'BiddingStrategyType'] if 'BiddingStrategy' in d['TextCampaign'] and 'Search' in
                                                      d['TextCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['TextCampaign']['BiddingStrategy']['Search'] else '',
                        'TextCampBidStrategyNetworkType': d['TextCampaign']['BiddingStrategy']['Network'][
                            'BiddingStrategyType'] if 'BiddingStrategy' in d['TextCampaign'] and 'Network' in
                                                      d['TextCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['TextCampaign']['BiddingStrategy']['Network'] else '',
                        'TextCampAttributionModel': d['TextCampaign']['AttributionModel'] if 'AttributionModel' in
                                                                                             d[
                                                                                                 'TextCampaign'] else None,
                        'DynCampBidStrategySearchType': d['DynamicTextCampaign']['BiddingStrategy']['Search'][
                            'BiddingStrategyType'] if 'DynamicTextCampaign' in d and 'BiddingStrategy' in d[
                            'DynamicTextCampaign'] and 'Search' in d['DynamicTextCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['DynamicTextCampaign']['BiddingStrategy']['Search'] else '',
                        'DynCampBidStrategyNetworkType': d['DynamicTextCampaign']['BiddingStrategy']['Network'][
                            'BiddingStrategyType'] if 'DynamicTextCampaign' in d and 'BiddingStrategy' in d[
                            'DynamicTextCampaign'] and 'Network' in d['DynamicTextCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['DynamicTextCampaign']['BiddingStrategy'][
                                                          'Network'] else '',
                        'DynCampAttributionModel': d['DynamicTextCampaign'][
                            'AttributionModel'] if 'DynamicTextCampaign' in d and 'AttributionModel' in d[
                            'DynamicTextCampaign'] else '',
                        'MobCampBidStrategySearchType': d['MobileAppCampaign']['BiddingStrategy']['Search'][
                            'BiddingStrategyType'] if 'MobileAppCampaign' in d and 'BiddingStrategy' in d[
                            'MobileAppCampaign'] and 'Search' in d['MobileAppCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['MobileAppCampaign']['BiddingStrategy']['Search'] else '',
                        'MobCampBidStrategyNetworkType': d['MobileAppCampaign']['BiddingStrategy']['Network'][
                            'BiddingStrategyType'] if 'MobileAppCampaign' in d and 'BiddingStrategy' in d[
                            'MobileAppCampaign'] and 'Network' in d['MobileAppCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['MobileAppCampaign']['BiddingStrategy']['Network'] else '',
                        'CpmBannerBidStrategySearchType': d['CpmBannerCampaign']['BiddingStrategy']['Search'][
                            'BiddingStrategyType'] if 'CpmBannerCampaign' in d and 'BiddingStrategy' in d[
                            'CpmBannerCampaign'] and 'Search' in d['CpmBannerCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['CpmBannerCampaign']['BiddingStrategy']['Search'] else '',
                        'CpmBannerBidStrategyNetworkType': d['CpmBannerCampaign']['BiddingStrategy']['Network'][
                            'BiddingStrategyType'] if 'CpmBannerCampaign' in d and 'BiddingStrategy' in d[
                            'CpmBannerCampaign'] and 'Network' in d['CpmBannerCampaign'][
                                                          'BiddingStrategy'] and 'BiddingStrategyType' in
                                                      d['CpmBannerCampaign']['BiddingStrategy']['Network'] else '',
                        'Login': logins[l],
                    }
                    df = pd.DataFrame(data, index=[i])
                    result = result.append(df, ignore_index=True)
            except KeyError:
                continue

        # add progress
        print('.', end='')

        # check for next iteration
        lim = data_raw['result']['LimitedBy'] + 1 if 'LimitedBy' in data_raw['result'] else 'stopped'

    # convert to factor

    res_data = {
        'res': result,
    }

    return res_data
# except Exception as e:
#     error_logger.error(msg=e.__str__())
#     return {
#         'res': {},
#         'error': e.__str__()
#     }
# TODO:
#   get_criteria
#   get_adset
