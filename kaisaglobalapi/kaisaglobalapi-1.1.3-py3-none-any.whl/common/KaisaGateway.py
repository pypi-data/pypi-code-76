
# -*- coding: utf-8 -*-

# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# KaisaGlobal rights are reserved.
# ===================================================================

"""
This code provide basic market and trade function for KaisaGlobal-Open.
Pls. note that only HK market is supported now.

developed by KaisaGlobal quant team.
2020.12.11
"""


import os, sys, json

import numpy as np
import pandas as pd

import traceback
import requests

import threading

import websocket
from copy import deepcopy


appendIpAddress = "192.168.1.1"
# appendIpAddress = None

# REAL ENV.
KAISA_ROOT_URL = "kgl.jt00000.com"
KAISA_ROOT_URL_SIM = "sit-kgl.jt00000.com"
# KAISA_ROOT_URL = KAISA_ROOT_URL_SIM
KAISA_ROOT_URL_API = "openapi.jt00000.com"
#
CRYPTO_RSA_URL = "https://__kaisarooturl__/kgl-third-authorization/crypto/key/RSA"
AUTHENTICA_URL = "https://__kaisarooturl__/kgl-third-authorization/oauth/token"
# AUTHENTICA_URL = "https://openapi.jt00000.com"
QUOTE_URL = "https://kgl.jt00000.com/hq"

# WEBSOCKET_DATA_HOST = "ws://__kaisarooturl__/dz_app_ws/ws"
WEBSOCKET_DATA_HOST = "ws://sit-kgl.jt00000.com/dz_app_ws/ws"
REST_DATA_HOST = "https://__kaisarooturl__/dzApp/dzHttpApi"

TRADE_CRYPTO_RSA_URL = "https://__kaisarooturl__/kgl-trade-service/crypto/key/RSA"
ClientByMobile_URL = "https://__kaisarooturl__/kgl-user-center/userOaccAccount/selectClientIdByMobile"
REST_HOST = "https://__kaisarooturl__/kgl-trade-service"
WEBSOCKET_TRADE_HOST = "wss://__kaisarooturl__/kgl-trade-push-service/ws"

openapi_scope = "wthk"

MARKET_POST_URL = "https://sit-kgl.jt00000.com/kgl-stock-push-provider"
MARKET_WS_URL = "ws://uat-stock.jt00000.com/stock"

from kaisaglobalapi.common import KaisaCrypto
from kaisaglobalapi.common.utils import *

from kaisaglobalapi.common import KaisaProtoc

kcrypto = KaisaCrypto()
kprotoc = KaisaProtoc()

START_PUSH = 200
STOP_PUSH = 201
SYNCHRONIZE_PUSH = 250
QUERY_HISTORY = 36
QUERY_CONTRACT = 52
ON_TICK = 251
ON_MARKETDATA = 153
PING = 2
PONG = 3
LOGIN = 10
HKSE_MARKET = 2002

CREATION = 101
UPDATE = 102
TRADE = 103
CANCELLATION = 104
ACCOUT = 106
POSITION = 105


class KaisaGateway():

    req_id = 0

    # gateway - market, trade;
    gateway_auth_status = False

    # ws
    market_ws_alive = False
    trade_ws_alive = False

    # trade;
    trade_connect_status = False
    trade_auth_status = False

    # token
    gatewayToken = None
    tradeToken = None

    _market_ws = None
    _trade_ws = None

    _market_connect_status = False

    _ws_trade_connect_status = False

    def __init__(self):
        pass

    def jq_user_config(self, user_id, user_pwd, account_code, account_pwd, openapi_token, environment='paper'):

        self.user_id = user_id
        self.user_pwd = user_pwd
        self.account_code = account_code
        self.account_pwd = account_pwd
        self.openapi_token = openapi_token
        self.environment = environment
        self.root_url = KAISA_ROOT_URL_SIM if self.environment in ["simulate", "paper"] else KAISA_ROOT_URL
        self._update_urls()

        self.m_req_id = 0
        self.trade_req_id = 0

    def _update_urls(self):

        update_url = lambda url: url.replace("__kaisarooturl__", self.root_url)

        self.CRYPTO_RSA_URL = update_url(CRYPTO_RSA_URL)
        self.AUTHENTICA_URL = update_url(AUTHENTICA_URL)
        self.QUOTE_URL = update_url(QUOTE_URL)

        self.REST_DATA_HOST = update_url(REST_DATA_HOST)
        self.WEBSOCKET_DATA_HOST = update_url(WEBSOCKET_DATA_HOST)

        self.ClientByMobile_URL = update_url(ClientByMobile_URL)
        self.REST_HOST = update_url(REST_HOST)
        self.WEBSOCKET_TRADE_HOST = update_url(WEBSOCKET_TRADE_HOST)

        self.TRADE_CRYPTO_RSA_URL = update_url(TRADE_CRYPTO_RSA_URL)

    def write_error(self, data):
        print("error: {}".format(data))

    def write_log(self, data):
        print("log: {}".format(data))

    def _authentica(self, auth_username: str, auth_password: str) -> None:
        """
        获取网关登录令牌;
        :param auth_username:
        :param auth_password:
        :return:
        """

        if self.gateway_auth_status:
            return self.gateway_auth_status

        # only for token of gateway.
        timestamp_ = generate_timestamp()
        sign_ = kcrypto.encrypt_md5("username{}Timestamp{}".format(auth_username, timestamp_))

        auth_username_encrypt = kcrypto.encrypt_rsa_username(auth_username, crypto_rsa_url=self.CRYPTO_RSA_URL)
        auth_password_encrypt = kcrypto.encrypt_aes_password(auth_password, "MAKRET")

        params = {
            "username": auth_username_encrypt,
            "password": auth_password_encrypt,
            "grant_type": "password",
            "scope": openapi_scope
        }

        if appendIpAddress:
            params["ipAddress"] = appendIpAddress

        headerParam = {"ipAddress":"14.154.204.168","phoneModel":"","deviceId":"","deviceToken":"","macAddress":"","channelId":"","country":"","sysVersion":"","apiVersion":"","platform":""}
        headerParam = json.dumps(headerParam)
        headers = {
            "Authorization": "basic {}".format(self.openapi_token),
            "Content-Type": "application/x-www-form-urlencoded",
            "Sign": sign_,
            "Timestamp": timestamp_,
            "headerParam": headerParam
        }
        response = requests.post(
            url=self.AUTHENTICA_URL, params=params, headers=headers
        )

        self.gateway_auth_msg = ""

        data = response.json()
        if response.status_code // 100 == 2:
            self.write_log("网关认证成功")
            if data['success']:
                self.write_log("获取登录令牌成功")
                token_body = data["body"]["accessToken"]
                self.gatewayToken = f"bearer {token_body}"
                self.token = self.gatewayToken
                self.gateway_auth_status = True
            else:
                self.token = None
                self.gatewayToken = None
                self.write_log("获取登录令牌失败")
                self.write_error(data)
        else:
            self.write_log("网关认证失败")
            self.write_error(data)


        return self.gateway_auth_status, self.gateway_auth_msg

    def gateway_auth(self):
        return self._authentica(self.user_id, self.user_pwd)

    def market_connect_ws(self):
        ret_ok, ret_msg = self.gateway_auth()
        if ret_ok:
            self.market_connect_ws()
        time.sleep(5)

    def do_market_requests(self, url, reqdata):

        reqdata = self._market_req_decorate(reqdata)
        method = reqdata["method"] if ("method" in reqdata) else "POST"
        headers = reqdata["headers"] if ("headers" in reqdata) else None
        params = reqdata["params"] if ("params" in reqdata) else None
        data = reqdata["data"] if ("data" in reqdata) else None

        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            data=json.dumps(data)
        )
        status_code = response.status_code
        resp_data = response.json()
        return status_code, resp_data


    def do_trade_requests(self, url, reqdata, reqtype="normal"):

        reqdata = self._trade_req_decorate(reqdata, reqtype)
        method = reqdata["method"] if ("method" in reqdata) else "POST"
        headers = reqdata["headers"] if ("headers" in reqdata) else None
        params = reqdata["params"] if ("params" in reqdata) else None
        data = reqdata["data"] if ("data" in reqdata) else None

        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data
        )
        status_code = response.status_code
        resp_data = response.json()
        return status_code, resp_data


    def _market_req_decorate(self, reqdata):

        reqdata['headers'] = {
            "Authorization": self.gatewayToken,
            "Content-Type": "application/json"
        }
        return reqdata

    def query_all_symbollist(self):

        contractdata_all = []
        beginpos = 0
        count = 1000
        while True:
            symbols = self.query_symbollist(beginpos=beginpos, count=count)
            if symbols is None:
                break
            contractdata_all += symbols
            if len(symbols)<count:
                break
            beginpos += count
        if len(contractdata_all)>0:
            self.write_log("合约信息查询成功")
        else:
            self.write_log("合约信息查询失败")

        return contractdata_all


    def query_symbollist(self, beginpos=0, count=1000):

        self.req_id += 1
        data = {
            "reqtype": QUERY_CONTRACT,
            "reqid": self.req_id,
            "session": "",
            "data": {
                "marketid": HKSE_MARKET,
                "idtype": 1,
                "beginpos": beginpos,
                "count": count,
                "getquote": 1
            }
        }

        reqdata = {"data": data}
        status_code, resp_data = self.do_market_requests(url=self.QUOTE_URL, reqdata=reqdata)
        if status_code//100==2:
            symbols = resp_data['data']['symbol']
        else:
            symbols = None
        return symbols


    def query_history_kline(self, symbol='01638', market='HK', klinetype='1d', adjfactortype='0', pagenum=1, pagesize=100):
        """
        query history kline (only for hk market)
        """
        post_url = MARKET_POST_URL+"/quoteInfo/kLine"

        klinetype2klineid = {'1min': 1,
                             '5min': 3,
                             '15min': 5,
                             '30min': 6,
                             '1hour': 7,
                             '1day': 10
                             }
        klineid = klinetype2klineid.get(klinetype)
        rqdata = {
            'code': symbol,
            'market': market,
            'quoteTypeEnumCode': klineid,
            'adjFactorType': adjfactortype,
            'pageNum': pagenum,
            'pageSize': pagesize
        }
        response = requests.request(
            'POST',
            post_url,
            headers={'Content-Type':'application/json'},
            params=None,
            data=json.dumps(rqdata)
        )
        status_code = response.status_code
        resp_data = response.json()
        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']['records']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def query_history_tick(self, symbol='00700', market='HK', pagesize=10, pagenum=1):

        post_url = MARKET_POST_URL + "/stock/quote/tick"
        rqdata = {
            'code': symbol,
            'market': market,
            'size': str(pagesize),
            'index': str(pagesize*pagenum)
        }
        response = requests.request(
            'POST',
            post_url,
            headers={'Content-Type':'application/json'},
            params=None,
            data=json.dumps(rqdata)
        )
        status_code = response.status_code
        resp_data = response.json()
        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def query_detailstate(self, symbol='01638', market='HK'):

        post_url = MARKET_POST_URL+ "/quoteInfo/todayDetailState"
        rqdata = {
            'code': symbol,
            'market': market,
            'hasQuoteInfo': True,
            'hasQuoteExt': True,
            'hasQuoteStat': True,
            'hasQuoteFinancial': True,
            'hasQuotePro': True
        }
        response = requests.request(
            'POST',
            post_url,
            headers={'Content-Type': 'application/json', 'headerParam':json.dumps({'apiVersion':"1.2.0"})},
            params=None,
            data=json.dumps(rqdata)
        )
        status_code = response.status_code
        resp_data = response.json()
        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
            del body_data['assetInfoResp']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def market_connect_ws(self):

        threading.Thread(target=self.__market_connect_ws, daemon=True).start()

    def get_market_connect_ws_status(self):

        return self._market_connect_status, self._market_connect_msg

    def __market_connect_ws(self):

        if self._market_connect_status:
            return

        header = {"Authorization": self.gatewayToken,
                  "deviceId":"xxx",
                  "platform":"open"}

        self._market_ws = websocket.create_connection(MARKET_WS_URL, header=header)
        self._market_ping_th = threading.Thread(target=self._market_ping, args=(self._market_ws,), daemon=True)
        self._market_ping_th.start()

        self._market_connect_status = True
        self._market_connect_msg = ""

        print('wait to receive.')
        while True:

            text = self._market_ws.recv()
            data = kprotoc.rec_bstring_to_json(text)
            if data is None:
                continue
            self.on_market_data(data)


    def on_market_packet(self, packet):

        self.on_market_data(packet)

    def on_market_data(self, data):
        pass

    def subscribe_marketdata(self, code_list):
        """
        推送行情和分笔；
        """
        self.req_id += 1
        bstring = kprotoc.get_subscribe_bstring(code_list, self.req_id)
        self._market_ws.send_binary(bstring)

    def unsubscribe_marketdata(self, code_list):
        """
        取消推送行情和分笔
        :param symbols:
        :return:
        """
        self.req_id+=1
        bstring = kprotoc.get_unsubscribe_bstring(code_list, self.req_id)
        self._market_ws.send_binary(bstring)

    def market_heartbeat(self):

        self.req_id += 1
        ping_bstring = kprotoc.get_ping_bstring(self.req_id)
        self._market_ws.send_binary(ping_bstring)

    def send_market_packet(self, packet):

        text = json.dumps(packet)
        self._market_ws.send(text)

    def generate_req(self, reqtype: int, data: dict) -> dict:

        self.req_id += 1
        req = {
            "reqtype": reqtype,
            "reqid": self.req_id,
            "session": "",
            "data": data
        }
        return req


    def _trade_req_decorate(self, reqdata, reqtype="normal"):

        json_dumps = lambda item: json.dumps(item, separators=(',', ':'))
        method = reqdata['method'] if 'method' in reqdata else "POST"
        headers = reqdata['headers'] if 'headers' in reqdata else {}
        data = reqdata['data'] if 'data' in reqdata else {}
        params = reqdata['params'] if 'params' in reqdata else {}

        this_timestamp = generate_timestamp()

        if (reqtype=="connect") and (method=="POST") and ('q' in reqdata['data']):
            headers = {"Content-Type": "application/json",
                       "Authorization": self.token
                        }
            params = deepcopy(reqdata['data'])
            reqdata = {'method':method,
                       'headers':headers,
                       'data':json_dumps(reqdata['data']),
                       'params': params
                       }
            return reqdata

        if (reqtype=="login"):

            headers['Content-Type'] = "application/json"
            headers["Authorization"] = self.token
            if reqtype=="login":
                data['Authorization'] = self.token
            if self.tradeToken is not None:
                headers['X-Trade-Token'] = self.tradeToken
            if reqtype=="normal":
                if 'tradeToken' in data:
                    del data['tradeToken']
            if method=="POST":
                header_ = reqdata['data'].copy()
                if self.tradeToken is not None:
                    header_["tradeToken"] = self.tradeToken
                headers["Sign"] = self.__sign(header_=header_, timestamp_=this_timestamp, request_="POST")
                headers["Timestamp"] = this_timestamp

            reqdata = {"method":method,
                       "data":json_dumps(data),
                       "headers":headers,
                       "params":json_dumps(params)}
            return reqdata

        headers = {"Content-Type": "application/json",
                   "Authorization": self.gatewayToken,
                   "X-Trade-Token": self.tradeToken
                   }

        if method=="GET":
            if 'params' in reqdata:
                header_ = reqdata['params'].copy()
            else:
                header_ = {}
            header_["Authorization"] = self.token
            headers["Sign"] = self.__sign(header_=header_, timestamp_=this_timestamp, request_="GET")
            headers["Timestamp"] = this_timestamp

        if method=="POST":
            header_ = data.copy()
            if self.tradeToken is not None:
                header_["tradeToken"] = self.tradeToken
            headers["Sign"] = self.__sign(header_=header_, timestamp_=this_timestamp, request_="POST")
            headers["Timestamp"] = this_timestamp

        if (method=="POST") and ('q' not in data):
            q_string = json_dumps(data)
            q_string = kcrypto.encrypt_aes_password_forQ(q_string, "SECRET")
            data = {'q': q_string}

        reqdata = {"method":method,
                   "data":json_dumps(data),
                   "headers":headers,
                   "params":params}

        return reqdata

    def _sign(self, reqdata, reqtype="normal"):

        json_dumps = lambda item: json.dumps(item, separators=(',', ':'))
        method = reqdata['method']
        headers = reqdata['headers'] if 'headers' in reqdata else {}
        data = reqdata['data'] if 'data' in reqdata else {}
        params = reqdata['params'] if 'params' in reqdata else {}

        if (reqtype=="connect") and (method=="POST") and ('q' in reqdata['data']):
            headers = {"Content-Type": "application/json",
                       "Authorization": self.token
                        }
            params = deepcopy(reqdata['data'])
            reqdata = {'method':method,
                       'headers':headers,
                       'data':json_dumps(reqdata['data']),
                       'params': params
                       }
            return reqdata

        if (reqtype=="login"):

            headers['Content-Type'] = "application/json"
            headers["Authorization"] = self.token
            if reqtype=="login":
                data['Authorization'] = self.token

            if self.tradeToken is not None:
                headers['X-Trade-Token'] = self.tradeToken

            if reqtype=="normal":
                if 'tradeToken' in data:
                    del data['tradeToken']

            if method=="POST":
                timestamp_ = generate_timestamp()
                header_ = reqdata['data'].copy()
                if self.tradeToken is not None:
                    header_["tradeToken"] = self.tradeToken
                headers["Sign"] = self.__sign(header_=header_, timestamp_=timestamp_, request_="POST")
                headers["Timestamp"] = timestamp_

            reqdata = {"method":method,
                       "data":json_dumps(data),
                       "headers":headers,
                       "params":json_dumps(params)}

            return reqdata

        headers = {"Content-Type": "application/json",
                   "Authorization": self.gatewayToken,
                   "X-Trade-Token": self.tradeToken
                   }

        if method=="GET":
            header_ = reqdata['params'].copy()
            header_["Authorization"] = self.token
            headers["Sign"] = self.__sign(header_=header_, timestamp_=timestamp_, request_="GET")
            headers["Timestamp"] = timestamp_

        if method=="POST":
            timestamp_ = generate_timestamp()
            header_ = data.copy()
            if self.tradeToken is not None:
                header_["tradeToken"] = self.tradeToken
            headers["Sign"] = self.__sign(header_=header_, timestamp_=timestamp_, request_="POST")
            headers["Timestamp"] = timestamp_

        if (method=="POST") and ('q' not in data):
            q_string = json_dumps(data)
            q_string = kcrypto.encrypt_aes_password_forQ(q_string, "SECRET")
            data = {'q': q_string}

        reqdata = {"method":method,
                   "data":json_dumps(data),
                   "headers":headers,
                   "params":params}

        return reqdata


    def __sign(self, header_: dict = {}, request_=None, timestamp_=None):

        sign_ = None
        str_ = ""
        for key_ in sorted(header_):
            str_ += str(key_)+str(header_[key_])
        str_ += "Timestamp"+timestamp_
        sign_ = kcrypto.encrypt_md5(str_)
        return sign_


    def trade_connect(self):
        """
        交易连接
        :return: trade_connect_status
        """
        if self.gateway_auth():
            en_password_trade = kcrypto.encrypt_aes_password(self.account_pwd, type="TRADE")
            self.en_password_trade = en_password_trade
            secret_q = kcrypto.encrypt_rsa_secretQ(crypto_rsa_url = self.TRADE_CRYPTO_RSA_URL)
            data = {
                "q": secret_q,
                "accountCode": self.account_code
            }
            url = self.REST_HOST + "/v1/account/shakeHand"
            reqdata = {"data": data}

            status_code, resp_data = self.do_trade_requests(url, reqdata, "connect")
            self.sessionId = resp_data['body']['sessionId']
            self.trade_connect_status = True

        self.trade_connect_msg = ''
        return self.trade_connect_status, self.trade_connect_msg


    def trade_auth(self):

        data = {
            "channelType": "INTERNET",
            "accountCode": self.account_code,
            "password": self.en_password_trade,
            "secondAuthFromOther": "Y",
            "sessionId": self.sessionId
        }
        reqdata = {"data": data}

        url = self.REST_HOST + "/v1/account/login"
        status_code, resp_data = self.do_trade_requests(url, reqdata, "login")

        if status_code//100==2:
            self.tradeToken = resp_data['body']['tradeToken']
            self.trade_auth_status = True
        else:
            self.tradeToken = None
            self.trade_auth_status = False
        self.trade_auth_msg = ''
        return self.trade_auth_status, self.trade_auth_msg


    def trade_connect_ws(self):
        threading.Thread(target=self._start_trade_ws, daemon=True).start()

    def get_trade_connect_ws_status(self):
        return self._ws_trade_connect_status, ""

    def _market_ping(self, this_ws):
        """
        :param this_ws:
        :return:
        """
        while True:
            self.market_heartbeat()
            time.sleep(5)

    def _trade_ping(self, this_ws):
        """
        :param this_ws:
        :return:
        """
        pass


    def _start_trade_ws(self):

        if self._ws_trade_connect_status:
            return True

        #
        data = {
            "channelType": "INTERNET",
            "accountCode": self.account_code,
            "password": self.en_password_trade,
            "ipAddress": "",
            "secondAuthFromOther": "Y",
            "sessionId": self.sessionId,
        }

        host = self.WEBSOCKET_TRADE_HOST
        header = {"Authorization": self.token}

        self._trade_ws = websocket.create_connection(host, header=header)

        req = self.generate_req(LOGIN, data)

        req = json.dumps(req)
        self._trade_ws.send(req)
        self._trade_ping_th = threading.Thread(target=self._trade_ping, args=(self._trade_ws,), daemon=True)
        self._trade_ping_th.start()
        self._ws_trade_connect_status = True

        while True:
            text = self._trade_ws.recv()
            self.on_trade_packet(text)


    def on_trade_packet(self, packet):

        if len(packet)==0:
            return
        data = json.loads(packet)
        if data.get('reqtype',0)==2:
            req_data = {"ts":data['data']["ts"]}
            req_data = self.generate_req(PONG, req_data)
            self._trade_ws.send(json.dumps(req_data))
        else:
            data = json.loads(packet)
            self.on_trade_data(packet)


    def send_order(self, bsFlag='B', price=550, qty=600, code='00700'):

        return self.place_order(bsFlag=bsFlag, price=price, qty=qty, code=code)

    def place_order(self, bsFlag='B', price=550, qty=600, code='00700'):

        data = {'channelType': "I",
                'exchangeCode': 'HKEX',
                'accountCode': self.account_code,
                'productCode': code,
                'price': price, 'qty': qty,
                'bsFlag': bsFlag, 'orderType': 'L',
                'tradeToken': self.tradeToken}

        reqdata = {"data": data,
                   "params": {'accountCode': self.account_code}}

        url = self.REST_HOST+"/v1/order/orders/place"
        status_code, resp_data = self.do_trade_requests(url, reqdata)

        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def cancel_order(self, sys_orderid):

        data = {
            "channelType": "I",
            "accountCode": self.account_code,
            "orderID": sys_orderid,
            "tradeToken": self.tradeToken,
        }
        reqdata = {"data": data,
                   "params": {'accountCode': self.account_code}}

        url = self.REST_HOST+"/v1/order/orders/cancel"
        status_code, resp_data = self.do_trade_requests(url, reqdata)

        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def query_portfolio(self):

        reqdata = {"method":"GET",
                   "params": {'accountCode': self.account_code}}

        url = self.REST_HOST+"/v1/account/accounts/portfolio"
        status_code, resp_data = self.do_trade_requests(url, reqdata)

        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def query_balance(self):

        reqdata = {"method": "GET",
                   "params": {'accountCode': self.account_code}}
        url = self.REST_HOST + "/v1/account/accounts/balance"
        status_code, resp_data = self.do_trade_requests(url, reqdata)
        resp_data = resp_data.json()
        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def query_position(self):

        reqdata = {"method": "GET",
                   "params": {'accountCode': self.account_code}}
        url = self.REST_HOST + "/v1/account/accounts/position"
        status_code, resp_data = self.do_trade_requests(url, reqdata)

        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data


    def query_order(self):

        reqdata = {"method": "GET",
                   "params": {'accountCode': self.account_code}}
        url = self.REST_HOST + "/v1/order/orders"
        status_code, resp_data = self.do_trade_requests(url, reqdata)

        resp_status = resp_data['success']
        if resp_status:
            body_data = resp_data['body']
        else:
            body_data = {'retCode': resp_data['retCode'],
                         'retMsg': resp_data['retMsg']
                         }
        return resp_status, body_data

if __name__=="__main__":

    print("Hello, Kaisa.")

