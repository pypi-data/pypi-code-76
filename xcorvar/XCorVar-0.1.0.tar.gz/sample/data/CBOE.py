# coding: utf-8

import os as os
import csv as  csv
import datetime as dt

import numpy as np

from sample.constants import Constants
from sample.data.market_data import MarketDataFrom, Spot, Options
from sample.toolbox.mathbox import get_time_to_expiry

IDX = {'strike' : 11, 'call_bid' : 4, 'call_ask' : 5, 'vol_call' : 6, 'put_bid' : 15, 'put_ask' : 16, 'vol_put' : 17}

class MarketDataFromCBOE (MarketDataFrom):

    def get (self, ticker, date, min_vol=0):
        print ('==> Requesting market data from CBOE for ' + ticker + ' on ' + date + ' ...')
        file_date = date.replace ('/', '')
        file_name = Constants.DATA_PATH + 'cboe' + '_' + ticker + '_' + file_date + '.csv'
        if not os.path.isfile (file_name): raise ValueError ("==> No data found.")
        else:
            opt = []
            file = open (file_name, 'r')
            data = csv.reader (file, delimiter=',')
            for cpt, line in enumerate (data):
                if cpt == 2:
                    bid = float (line [1].split (': ') [1])
                    ask = float (line [2].split (': ') [1])
                    spot = {'bid' : bid, 'ask' : ask}
                elif cpt >= 4: 
                    mat = line [0]
                    mat = dt.datetime.strptime (mat, '%a %b %d %Y').strftime (Constants.CODE_DATE)
                    mat = get_time_to_expiry (date, mat)
                    if mat < 0: continue
                    else:
                        strk, call_bid, call_ask, call_vol, put_bid, put_ask, put_vol = np.float64 (np.array (line) [list (IDX.values ())])
                        if call_bid != 0 and call_ask != 0 and put_bid != 0 and put_ask != 0 and put_vol > min_vol and call_vol > min_vol:
                            data = {
                                'mat' : mat,
                                'strike' : strk, 
                                'call' : {
                                    'bid' : call_bid,
                                    'ask' : call_ask
                                },
                                'put' : {
                                    'bid' : put_bid,
                                    'ask' : put_ask
                                }
                            }
                            opt.append (data)
            print ('==> Market data downloaded.')
        return Spot (spot), Options (opt)