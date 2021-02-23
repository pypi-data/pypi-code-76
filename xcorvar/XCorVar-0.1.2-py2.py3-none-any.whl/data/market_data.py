# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt

from sample.toolbox.mathbox import get_file_name, load, dump, get_mid

class MarketDataFrom:

    def get ():
        raise NotImplementedError

class MarketDataFromFile (MarketDataFrom):

    def get (self, ticker, date):
        print ("==> Requesting market data from file for ", ticker, "on ", date, " ...")
        date = date.replace ('/', '')
        file = get_file_name (ticker, date)
        spot = load (file ('spot'))
        opt = load (file ('opt'))
        if spot is None: print ("==> Spot not found.")
        if opt is None: print ("==> Option not found.")
        print ("==> Market data downloaded.")
        return Spot (spot), Options (opt)

class Spot:

    def __init__ (self, data):
        self.data = data 
        self.bid = data ['bid']
        self.ask = data ['ask']
        self.mid = get_mid (self.bid, self.ask)

    def save (self, ticker, date):
        print ('==> Saving spot data ...')
        date = date.replace ('/', '')
        file = get_file_name (ticker, date)
        file_name = file ("spot")
        dump (self.data, file_name)
        print ('==> Spot data saved.')

class Options:

    #public

        def __init__ (self, data):
            self.data = data
            self.slicer = self._slicer () if data is not None else None               

        def save (self, ticker, date):
            print ('==> Saving option data ...')
            date = date.replace ('/', '')
            file = get_file_name (ticker, date) 
            file_name = file ("opt")
            print (file_name)
            dump (self.data, file_name)
            print ('==> Option data saved.')

        def plot_call_put_parity (self):
            print ('==> Plotting call - put parity ...')
            for mat, (strk, call_bid, call_ask, put_bid, put_ask) in self.mat_wise_data.items ():
                plt.figure ()
                plt.title ('Call-Put Parity Arbitrage for maturity date ' + str (round (mat, 2)))
                plt.xlabel ('Strike')
                plt.ylabel ('Call Minus Put')
                call = 0.5 * (np.array (call_bid) + np.array (call_ask))
                put = 0.5 * (np.array (put_bid) + np.array (put_ask))
                call_minus_put = call - put
                plt.scatter (strk, call_minus_put, marker='+', color='black')
                plt.show ()
            print ('==> Call - Put parity plotted.')

        def plot_price (self):
            print ('==> Plotting option prices ...')
            for mat, (strk, call_bid, call_ask, put_bid, put_ask) in self.mat_wise_data.items ():
                plt.figure ()
                plt.title ('Put and call prices at maturity date ' + str (mat))
                plt.xlabel ('Strike')
                plt.ylabel ('Option price')
                plt.scatter (strk, call_bid, marker='_', label='Call bid price', color='red')
                plt.scatter (strk, call_ask, marker='+', label='Call ask price', color='blue')
                plt.scatter (strk, put_bid, marker='_', label='Put bid price', color='grey')
                plt.scatter (strk, put_ask, marker='+', label='Put ask price', color='green')
                plt.legend (loc='best')
                plt.show ()
            print ('==> Options prices plotted.')

        def show (self):
            def show (mat):
                print ('Maturity: ', mat)
                print ('@@@@@@@@@@')
                opt = self.mat_wise_data [mat]   
                for strk, call_bid, call_ask, put_bid, put_ask in zip (*opt):
                    print ('Strike: ', strk)
                    print ('C: ', 'bid ', call_bid, ' | ', call_ask, ' ask')
                    print ('P: ', 'bid ', put_bid, ' | ', put_ask, ' ask')
                    print ('##########')
                print ('@@@@@@@@@@')
            print ('==> Showing option data ...')
            for mat in self.mat_wise_data.keys (): show (mat)
            print ('==> Option data shown.')

    #private

        def _slicer (self):
            mat_wise_data = {}
            for ft in self.data:
                mat, strk, call, put = ft.values ()
                call_bid, call_ask = call.values ()
                put_bid, put_ask = put.values ()
                if mat in mat_wise_data:
                    for idx, var in enumerate ([strk, call_bid, call_ask, put_bid, put_ask]):
                        mat_wise_data [mat] [idx].append (var)
                else: mat_wise_data [mat] = [[strk], [call_bid], [call_ask], [put_bid], [put_ask]]                
            return mat_wise_data

