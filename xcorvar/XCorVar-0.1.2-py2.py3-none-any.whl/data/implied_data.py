# coding: utf-8

import math as mth

import numpy as np
from matplotlib import pyplot as plt

from sample.constants import Constants
from sample.toolbox.black_scholes_functions import get_implied_total_variance, get_volatility
from sample.toolbox.mathbox import find_index, square, get_file_name, load, dump, is_in_frame, cleaner, linear_regression, get_mid
from sample.toolbox.interpolation.curve_interpolation import LinearInterpolation, Point
from sample.toolbox.interpolation.curve_interpolation import Point, CubicSplineInterpolation 

class ImpliedDataFrom:

    def get (self):
        raise NotImplementedError

class ForwardDataFromScratch (ImpliedDataFrom):

    def get (self, fwd, inter_style=LinearInterpolation):
        print ("==> Extracting forward data from scratch ...")
        fwd = [dict (mat = stm ["mat"], bid = stm ["fwd"], ask = stm ["fwd"], mid = stm ["fwd"]) for stm in fwd]        
        print ('==> Forward data extracted.')
        return Forward (fwd, inter_style)

class ForwardDataFromFile (ImpliedDataFrom):

    def get (self, ticker, date, inter_style=LinearInterpolation):
        print ("==> Requesting forward data from file for ", ticker, "on ", date, " ...")
        date = date.replace ('/', '')
        file = get_file_name (ticker, date)
        fwd = load (file ('fwd'))
        print ("==> Forward data downloaded.")
        return Forward (fwd, inter_style)

class RepoDataFromFile (ImpliedDataFrom):

    def get (self, ticker, date):
        print ("==> Requesting repo data from file for ", ticker, "on ", date, " ...")
        date = date.replace ('/', '')
        file = get_file_name (ticker, date)
        repo = load (file ('repo'))
        print ("==> Repo data downloaded.")
        return Repo (repo)

class ImpliedDataFromMarketData (ImpliedDataFrom):

    #public:

        def __init__ (self, spot, opt):
            self.spot = spot
            self.opt = opt.slicer

        def get (self, inter_style=LinearInterpolation):
            print ("==> Extracting implied data from market data ...")
            spot = self.spot
            opt = self.opt
            def get_implied_from_regression (a, b):
                fwd = - a / b
                dsc_repo = a / spot.mid
                dsc_rate = -b
                return fwd, dsc_rate, dsc_repo
            def get_implied (mat, *prices):
                strk, call_bid, call_ask, put_bid, put_ask = prices
                call_put = np.array (call_ask) - np.array (put_bid)
                fwd_ask, dsc_rate_ask, dsc_repo_ask = get_implied_from_regression (*linear_regression (strk, call_put))
                call_put = np.array (call_bid) - np.array (put_ask) 
                fwd_bid, dsc_rate_bid, dsc_repo_bid = get_implied_from_regression (*linear_regression (strk, call_put))
                return [
                    {'mat' : mat, 'bid' : fwd_bid, 'ask' : fwd_ask, 'mid' : get_mid (fwd_bid, fwd_ask)},
                    {'mat' : mat, 'bid' : dsc_rate_bid, 'ask' : dsc_rate_ask, 'mid' : get_mid (dsc_rate_bid, dsc_rate_ask)},
                    {'mat' : mat, 'bid' : dsc_repo_bid, 'ask' : dsc_repo_ask, 'mid' : get_mid (dsc_repo_bid, dsc_repo_ask)}
                ]
            implied = [get_implied (mat, *prices) for mat, prices in opt.items ()]
            fwd, dsc_rate, dsc_repo = zip (*implied)
            fwd0 = {'mat' : 0, 'bid' : spot.bid, 'ask' : spot.ask, 'mid' : spot.mid}
            fwd = [fwd0] + list (fwd)
            print ('==> Implied data extracted.')
            return Forward (list (fwd), inter_style), Rate (list (dsc_rate)), Repo (list (dsc_repo)) 

class Rate:

    #public:

        def __init__ (self, data):
            self.data = data

        def save (self, ticker, date):
            print ('==> Saving rate data ...')
            date = date.replace ('/', '')
            file = get_file_name (ticker, date)
            file_name = file ("rate")
            dump (self.data, file_name)
            print ('==> Rate data saved.')

        def plot (self):
            print ('==> Plotting rate discount factors ...')
            plt.figure ()
            plt.title ('Rate discount factors')
            plt.xlabel ('Maturity (in yrs)')
            plt.ylabel ('Rate discound factor (in %)')
            for ft in self.data:
                mat, _, _, mid = ft.values ()
                plt.scatter (mat, 100 * mid, marker='x', color='black')
            plt.show ()
            print ('==> Rate discount factors plotted.')

class Repo:

    #public:

        def __init__ (self, data):
            self.data = data
            self.slicer = self._build_slicer ()

        def save (self, ticker, date):
            print ('==> Saving repo data ...')
            date = date.replace ('/', '')
            file = get_file_name (ticker, date)
            file_name = file ("repo")
            dump (self.data, file_name)
            print ('==> Repo data saved.')
        
        def plot (self):
            print ('==> Plotting repo discount factors ...')
            plt.figure ()
            plt.title ('Repo discount factors')
            plt.xlabel ('Maturity (in yrs)')
            plt.ylabel ('Repo discound factor (in %)')
            for ft in self.data:
                mat, _, _, mid = ft.values ()
                plt.scatter (mat, 100 * mid, marker='x', color='black')
            plt.show ()
            print ('==> Repo discount factors plotted.')

    #private:

        def _build_slicer (self):
            return {data ['mat'] : data ['mid'] for data in self.data}

class Forward:

    #public:

        def __init__ (self, data, inter_style=LinearInterpolation):
            self.data = data
            self.slicer = self._build_slicer ()
            self.interpoler = self._build_interpoler (inter_style)

        def __call__ (self, mat):
            return self.interpoler.interpoler (mat)

        def plot_interpolated (self, lft=0, rgt=1, size=100):
            self.interpoler.plt (lft, rgt, size)
    
        def save (self, ticker, date):
            print ('==> Saving forward data ...')
            date = date.replace ('/', '')
            file = get_file_name (ticker, date)
            file_name = file ("fwd")
            dump (self.data, file_name)
            print ('==> Forward data saved.')

        def plot (self):
            print ('==> Plotting forward prices ...')
            plt.figure ()
            plt.title ('Forward prices')
            plt.xlabel ('Maturity (in yrs)')
            plt.ylabel ('Forward price')
            for ft in self.data:
                mat, bid, ask, mid = ft.values ()
                plt.scatter (mat, bid, marker='_', color='red')
                plt.scatter (mat, mid, marker='x', color='black')
                plt.scatter (mat, ask, marker='+', color='blue')
            plt.show ()
            print ('==> Forward prices plotted.')

    #private:

        def _build_interpoler (self, inter_style=LinearInterpolation):
            return inter_style ([Point (data ['mat'], data ['mid']) for data in self.data])

        def _build_slicer (self):
            return {data ['mat'] : data ['mid'] for data in self.data}
    
class VolatilityDataFromScratch (ImpliedDataFrom):

    def get (self, spot, vol):
        print ("==> Extracting volatility data from scratch ...")
        vol = [
            dict (
                mat = stm ["mat"], 
                strike = spot * stm ["fwd_mnn"] / 100, 
                fwd_mnn = stm ["fwd_mnn"] / 100,
                log_fwd_mnn =  mth.log (stm ["fwd_mnn"] / 100),
                impl_tot_var_bid = stm ["mat"] * square (stm ["vol"] / 100),
                impl_tot_var_ask = stm ["mat"] * square (stm ["vol"] / 100)
            )
            for stm in vol
        ]
        print ('==> Volatility data extracted.')
        return Volatility (vol)

class VolatilityDataFromFile (ImpliedDataFrom):

    def get (self, ticker, date):
        print ("==> Requesting volatility data from file for ", ticker, "on ", date, " ...")
        date = date.replace ('/', '')
        file = get_file_name (ticker, date)
        vol = load (file ('vol'))
        print ("==> Volatility data downloaded.")
        return Volatility (vol)

class VolatilityDataFromMarketData (ImpliedDataFrom):

    #public:

        def __init__ (self, spot, fwd, repo, opt):
            self.spot = spot.mid
            self.fwd = fwd.slicer  
            self.repo = repo.slicer
            self.opt = opt.data

        def get (self, frame=[90, 110], mat_min=Constants.MINIMUM_MATURITY):
            print ("==> Extracting volatility data from data ...")
            spot = self.spot
            fwd = self.fwd
            opt = self.opt
            repo = self.repo
            def get_total_variance (mat, strike, price, _): 
                bid, ask = price.values ()
                fwd_mnn = strike / fwd [mat]
                log_fwd_mnn = mth.log (fwd_mnn)
                if spot * max (1 - fwd_mnn, 0) < bid and ask < spot and is_in_frame (100 * fwd_mnn, frame) and mat > mat_min:
                    bid = get_implied_total_variance (bid, log_fwd_mnn, fwd_mnn, spot, repo [mat])
                    ask = get_implied_total_variance (ask, log_fwd_mnn, fwd_mnn, spot, repo [mat])
                    return {'mat' : mat, 'strike' : strike, 'fwd_mnn' : fwd_mnn, 'log_fwd_mnn' : log_fwd_mnn, 'bid' : bid, 'ask' : ask}
                else: return None
            tot_vars = cleaner ([get_total_variance (*data.values ()) for data in opt])
            print ('==> Volatility data extracted.')
            return Volatility (tot_vars) 
            
class Volatility:

    #public:

        def __init__ (self, data):
            self.data = data
            self.slicer = self._build_slicer ()

        def __call__ (self, mat, log_fwd_mnn):
            return self.interpoler (mat, log_fwd_mnn)

        def save (self, ticker, date):
            print ('==> Saving volatility data ...')
            date = date.replace ('/', '')
            file = get_file_name (ticker, date)
            file_name = file ("vol")
            dump (self.data, file_name)
            print ('==> volatility data saved.')

        def plot (self, kind='fwd_mnn'):
            print ('==> Plotting implied volatility ...')
            for mat, (strk, fwd_mnn, log_fwd_mnn, impl_tot_var) in self.slicer.items ():
                plt.figure ()
                plt.title ('Implied volatility at maturity date ' + str (mat))
                xlabel = 'Forward moneyness (in %)' if kind is 'fwd_mnn' else 'Strike' if kind is 'strike' else 'LogForward moneyness'
                plt.xlabel (xlabel)
                plt.ylabel ('Implied volatility (in %)')
                if kind is 'log_fwd_mnn': x = log_fwd_mnn
                elif kind is 'fwd_mnn': x = 100 * fwd_mnn
                elif kind is 'strike': x = strk
                else: raise ValueError ('Cannot find kind of abscisse')
                for k, (bid, ask) in zip (x, impl_tot_var):
                    plt.scatter (k, 100 * get_volatility (bid, mat), marker='_', color='red')
                    plt.scatter (k, 100 * get_volatility (ask, mat), marker='+', color='blue')
                plt.show ()
            print ('==> Implied volatility plotted.')

        def show (self):
            print ('==> Showing volatility data ...')
            for mat, vol in self.slicer.items ():
                print ('Maturity: ', mat)
                print ('@@@@@@@@@@')
                for strk, fwd_mnn, log_fwd_mnn, (bid, ask) in zip (*vol):
                    bid = get_volatility (bid, mat)
                    ask = get_volatility (ask, mat)
                    print ('Strike: ', strk)
                    print ('Fwd mnn: ', round (100 * fwd_mnn, 0), '%')
                    print ('Log fwd mnn: ', round (log_fwd_mnn, 4))
                    print ('bid ', round (100 * bid, 2), ' | ', round (100 * ask, 2), ' ask')
                    print ('##########')
                print ('@@@@@@@@@@')
            print ('==> Volatility data shown.')

    #private:

        def _build_slicer (self):
            mat_wise_data = {}
            for ft in self.data:
                mat, strk, fwd_mnn, log_fwd_mnn, impl_tot_var_bid, impl_tot_var_ask = ft.values ()
                impl_tot_var = impl_tot_var_bid, impl_tot_var_ask
                if mat in mat_wise_data:
                    for idx, var in enumerate ([strk, fwd_mnn, log_fwd_mnn, impl_tot_var]): 
                        mat_wise_data [mat] [idx].append (var)
                else:
                    mat_wise_data [mat] = [[strk], [fwd_mnn], [log_fwd_mnn], [impl_tot_var]]
            return mat_wise_data

class AtheMoneyVolatilityDataFromVolatilityData:

    #public:

        def __init__ (self, vol):
            self.vol = vol.slicer

        def get (self, inter_style='linear'):
            print ("==> Extracting at the money volatility data from volatility data ...")        
            def get_atm (mat, *val):
                _, _, log_fwd_mnn, tot_var = val
                begin, end = find_index (log_fwd_mnn)
                atm_log_fwd_mnn = [log_fwd_mnn [idx] for idx in [begin, end]]
                atm_tot_var_bid, atm_tot_var_ask = zip (*[tot_var [idx] for idx in [begin, end]])
                atm_tot_var_bid_skew = (atm_tot_var_bid [1] - atm_tot_var_bid [0]) / (atm_log_fwd_mnn [1] - atm_log_fwd_mnn [0])
                atm_tot_var_ask_skew = (atm_tot_var_ask [1] - atm_tot_var_ask [0]) / (atm_log_fwd_mnn [1] - atm_log_fwd_mnn [0])
                bid = atm_tot_var_bid [0] - atm_tot_var_bid_skew * atm_log_fwd_mnn [0]
                ask = atm_tot_var_ask [0] - atm_tot_var_ask_skew * atm_log_fwd_mnn [0]
                return {'mat' : mat, 'bid' : bid, 'ask' : ask}
            print ('==> At the money data extracted.')
            atm0 = {'mat' : 0, 'bid' : 0, 'ask' : 0}
            return AtTheMoneyVolatilityData ([atm0] + [get_atm (mat, *val) for mat, val in self.vol.items ()], inter_style)

class AtTheMoneyVolatilityData:

    #public:

        def __init__ (self, data, inter_style='linear'):
            self.data = data
            self.interpoler = self._build_interpoler (inter_style)

        def show (self):
            for data in self.data:
                mat = data ['mat']
                impl_tot_var_bid = data ['bid']
                impl_tot_var_ask = data ['ask']
                print ('Maturity: ', round (mat, 2), ' bid ', round (impl_tot_var_bid, 2), ' ask ', round (impl_tot_var_ask, 2))

        def plot (self):
            print ('==> Plotting ATM implied total variance ...')
            plt.figure ()
            plt.title ('ATM (in %)')
            plt.xlabel ('Maturity (in yrs)')
            plt.ylabel ('ATM')
            for data in self.data:
                plt.scatter (data ['mat'], data ['bid'], marker='_', color='red')
                plt.scatter (data ['mat'], data ['ask'], marker='+', color='blue')
            plt.show ()
            print ('==> ATM implied total variance plotted.')

        def plot_interpolated (self):
            print ('==> Plotting ATM implied total variance function ...')
            plt.figure ()
            plt.title ('ATM (in %)')
            plt.xlabel ('Maturity (in yrs)')
            plt.ylabel ('ATM')
            mats = [data ['mat'] for data in self.data]
            bid = [data ['bid'] for data in self.data]
            ask = [data ['ask'] for data in self.data]
            mdl = [self.interpoler (mat) for mat in mats]
            plt.scatter (mats, bid, marker='_', color='red')
            plt.scatter (mats, ask, marker='+', color='blue')
            plt.plot (mats, mdl, color='green', marker='x')
            plt.show ()
            print ('==> ATM implied total variance function plotted.')

    #private:

        def _build_interpoler (self, inter_style="linear"):
            if inter_style is "splin":
                atm_tot_var_pts = [Point (data ['mat'], get_mid (data ['bid'], data ['ask'])) for data in self.data]
                return CubicSplineInterpolation (atm_tot_var_pts).interpoler
            elif inter_style is "linear":
                mats = [data ['mat'] for data in self.data]
                bid = [data ['bid'] for data in self.data]
                ask = [data ['ask'] for data in self.data]
                mats = np.array (mats + mats)
                impl_tot_var = np.array (bid + ask)
                sq_sig = np.sum (mats * impl_tot_var) / np.sum (mats ** 2)
                return lambda t: sq_sig * t
            else: 
                raise NameError ("Interpolation mode not found")