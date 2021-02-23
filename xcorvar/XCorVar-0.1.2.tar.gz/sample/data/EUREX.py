# coding: utf-8

import datetime as dt

from bs4 import BeautifulSoup
import urllib.request

from sample.constants import Constants
from sample.data.market_data import MarketDataFrom, Spot, Options
from sample.toolbox.mathbox import get_time_to_expiry, union

IDX = {'strike' : 0, 'bid' : 5, 'ask' : 7}

#box:

def get_strike (data):
    return float (fine_tuned_string (data [IDX ['strike']].getText ()))

def get_bid_ask (data, bid_ask):
    opt_val = data [IDX [bid_ask]].getText ()
    return None if opt_val == 'n.a.' or opt_val == 0 else float (fine_tuned_string (opt_val))

def fine_tuned_string (s):
    return s.replace ('.', '').replace (',', '.')

def clean_call (data):
    bid_ask = data ['call']
    for val in bid_ask.values (): 
        if val is None: return False
    return True

def clean_put (data):
    bid_ask = data ['put']
    for val in bid_ask.values (): 
        if val is None: return False
    return True

#core

class MarketDataFromEUREX (MarketDataFrom):

    #public:

        def get (self, ticker):
            print ('==> Requesting current market data from EUREX for ' + ticker + ' ...')
            date = Constants.TODAY
            if ticker is "STOXX50E":
                id_ticker = 'euro_stoxx/'
                id_url_dates = 'EURO-STOXX-50-Index-Options-46548/' 
            else: raise NameError ('Cannot retrieve data for ' + ticker)
            url = 'https://www.eurexchange.com/asia-01/products/equity_index_derivatives/'
            url_data = url + id_ticker
            url_dates = url_data + id_url_dates 

            #get spot and maturities

            page = urllib.request.urlopen (url_dates)
            data = BeautifulSoup (page, 'html.parser')
            maturities = data.find ('div', attrs={'class': 'dataTableFilter'}).find_all ('select') [0].find_all ('option') [:-1]
            spot = float (data.find_all ('div', attrs={'class': 'slot3'}) [1].find ('dl').find ('dd').getText ().replace (',', ""))
            spot = {'bid': spot, 'ask': spot}

            # get option 

            def get_data (kind):
                opt = []
                for mat in maturities:
                    mat = date.get ('value')   
                    url = url_data + '69660!quotesSingleViewOption?callPut=' + kind + '&maturityDate=' + mat 
                    page = urllib.request.urlopen (url)
                    lines = BeautifulSoup (page, 'html.parser').find ('table', attrs={'class' : 'dataTable'}).find_all ('tr')
                    flag = True
                    for line in lines [1:-1]:
                        data = line.find_all ('td')
                        if flag: 
                            mat = dt.datetime.strptime (mat, '%Y%m').strftime (Constants.CODE_DATE)
                            mat = get_time_to_expiry (date, mat)
                            flag = not flag
                        strike = get_strike (data)
                        bid = get_bid_ask (data, 'bid')
                        ask = get_bid_ask (data, 'ask')
                        if kind is 'Call': feature = {'mat' : mat, 'strike' : strike, 'call' : {'bid' : bid, 'ask' : ask}}
                        else: feature = {'put' : {'bid' : bid, 'ask' : ask}}
                        opt.append (feature)
                return opt
            calls = get_data ('Call')
            puts = get_data ('Put')
            opt = [union (call, put) for call, put in zip (calls, puts) if clean_call (call) and clean_put (put)]
            
            print ('==> Market data downloaded.')
            return Spot (spot), Options (opt)

