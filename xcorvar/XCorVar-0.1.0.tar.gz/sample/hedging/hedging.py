# coding: utf-8

import csv as csv
import copy as cpy
import numpy as np

class Spot:

    #public:

        def __init__ (self, time, spot):
            self.time = time
            self.spot = spot

        def dtime (self, time):
            return time - self.time

        def dspot (self, spot):
            return spot - self.spot

        def dspot0 (self, time, rate):
            return rate * self.dtime (time)

        def show (self):
            print ('time: ', self.time)
            print ('spot: ', self.spot)
    
class SpotVol (Spot):

    #public:

        def __init__ (self, time, spot, vol):
            super ().__init__ (time, spot)
            self.vol = vol

        def show (self):
            super ().show ()
            print ('vol: ', self.vol)

class Greeks:

    #public:

        def __init__ (self, delta, dollargamma):
            self.delta = delta
            self.dollargamma = dollargamma

class Opt:

    #public:

        def __init__ (self, pricer, price=None, greeks=None):
            self.pricer = pricer
            self.price = price
            self.greeks = greeks

        def dprice (self, price):
            return price - self.price

        def deposit (self, spot):
            return self.price - self.greeks.delta * spot

        def get_pnl (self, dspot, dspot0, spot, price):
            return -self.dprice (price) + self.greeks.delta * dspot + self.deposit (spot) * dspot0

        def show (self):
            print ('price: ', self.price)
            print ('delta: ', self.greeks.delta)
            print ('dollargamma: ', self.greeks.dollargamma)

class Ptf:

    #public:

        def __init__ (self, exo):
            self.exo = exo

        def show (self):
            self.exo.show ()

class DeltaHedgedPtf (Ptf):

    #public:

        def __init__ (self, exo):
            super ().__init__ (exo)

        def get_pnl (self, dspot, dspot0, spot, price):
            return self.exo.get_pnl (dspot, dspot0, spot, price)

class DeltaGammaHedgedPtf (Ptf):

    #public:

        def __init__ (self, exo, van):
            super ().__init__ (exo)
            self.van = van

        def hedge_ratio (self):
            return self.exo.greeks.dollargamma / self.van.greeks.dollargamma

        def get_pnl (self, dspot, dspot0, spot, price_exo, price_van):
            pnl_exo = self.exo.get_pnl (dspot, dspot0, spot, price_exo)
            pnl_van = self.van.get_pnl (dspot, dspot0, spot, price_van)
            return pnl_exo + self.hedge_ratio () * pnl_van

class State:

    #public:

        def __init__ (self, ptf, mkt=None, pnl=None):
            self.ptf = ptf
            self.mkt = mkt
            self.pnl = pnl

        def show (self):
            print ('@@@@@')
            self.mkt.show ()
            print ('@@@@@')
            self.ptf.show ()
            print ('@@@@@')
            print ('pnl: ', self.pnl)

class Hedging:

    #public:

        def __init__ (self, ptf):
            self.state = State (ptf)
            self.tot_pnl = 0
            self.hist = []

        @property
        def current (self):
            return self.state

        def show (self):
            for state in self.hist: state.show ()

        def plt (self):
            '''
                spot/rate/vol trajectory
                price/delta/gamma evolution
                pnl/carry_pnl/tot_pnl progression
            '''
            pass

        def run (self, file_name, verbose=0):
            for data in csv.reader (open (file=file_name, mode='r'), delimiter=','):
                pnl = self.next (data, verbose)
                if pnl is not None: self.tot_pnl += pnl
                if verbose > 0: print ('tot_pnl: ', self.tot_pnl)
            return self

    #private:

        def next (self, data, verbose=0):
            raise NotImplementedError

class DeltaHedging (Hedging):

    #public:

        def __init__ (self, ptf, vol, rate):
            super ().__init__ (ptf)
            self.rate = rate
            self.vol = vol

    #private:

        def next (self, data, verbose=0):
            time, spot = np.float64 (data)
            price, delta, dollargamma = self.state.ptf.exo.pricer (time, spot, self.vol, self.rate)
            if self.state.mkt is not None:
                dspot = self.state.mkt.dspot (spot)
                dspot0 = self.state.mkt.dspot0 (time, self.rate)
                self.state.pnl = self.state.ptf.get_pnl (dspot, dspot0, spot, price)
            self.state.ptf.exo.price = price
            self.state.ptf.exo.greeks = Greeks (delta, dollargamma)
            self.state.mkt = Spot (time, spot)
            self.hist.append (cpy.copy (self.state))
            if verbose > 0: self.state.show ()
            return self.state.pnl

class DeltaGammaHedging (Hedging):

    #public:

        def __init__ (self, ptf, rate):
            super ().__init__ (ptf)
            self.rate = rate

    #private:

        def next (self, data, verbose=0):
            time, spot, vol = np.float64 (data)
            price_exo, delta_exo, dollargamma_exo = self.state.ptf.exo.pricer (time, spot, vol, self.rate)
            price_van, delta_van, dollargamma_van = self.state.ptf.van.pricer (time, spot, vol, self.rate)
            if self.state.mkt is not None:
                dspot = self.state.mkt.dspot (spot)
                dspot0 = self.state.mkt.dspot0 (time, self.rate)
                self.state.pnl = self.state.ptf.get_pnl (dspot, dspot0, spot, price_exo, price_van)
            self.state.ptf.exo.price = price_exo
            self.state.ptf.exo.greeks = Greeks (delta_exo, dollargamma_exo)
            self.state.ptf.van.price = price_van
            self.state.ptf.van.greeks = Greeks (delta_van, dollargamma_van)
            self.state.mkt = SpotVol (time, spot, vol)
            self.hist.append (cpy.copy (self.state))
            if verbose > 0: self.state.show ()
            return self.state.pnl