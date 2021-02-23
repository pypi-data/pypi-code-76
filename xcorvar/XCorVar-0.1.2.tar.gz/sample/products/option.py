# coding: utf-8

from typing import NewType
import datetime as dt

from sample.constants import CODE_DATE

Underlying = NewType ('Underlying', str)
Strike = NewType ('Strike', float)
Cash = NewType ('Cash', float)

class Date:
    def __init__ (self, date: str, code: str = CODE_DATE):
        self.date = dt.datetime.strptime (date, code)

class Amount:
    def __init__ (self, val: Cash = None):
        self.val = val
    def eval (self):
        raise NotImplementedError
    
class FloatingAmount (Amount):
    def __init__ (self, fixing_date: Date, undl: Underlying, quote: Cash = None):
        super ().__init__ (quote)
        self.fixing_date = fixing_date
        self.undl = undl
        self.quote = quote
    def fix (self, val: Cash):
        self.quote = val
    def eval (self):
        if self.quote is None: raise ValueError ("Cannot find quote")
        else: return self.quote

class FixedAmount (Amount):
    def __init__ (self, val: Cash):
        super ().__init__ (val)
    def eval (self):
        return self.val

class BinaryOperation (Amount):
    def __init__ (self, lhs: Amount, rhs: Amount):
        super ().__init__ ()
        self.lhs = lhs
        self.rhs = rhs
    def eval (self):
        raise NotImplementedError

class UnaryOperation (Amount):
    def __init__ (self, x: Amount):
        super ().__init__ ()
        self.x = x
    def eval (self):
        raise NotImplementedError

class SUB (BinaryOperation):
    def __init__ (self, lhs: Amount, rhs: Amount):
        super ().__init__ (lhs, rhs)
    def eval (self):
        return self.lhs.eval () - self.rhs.eval ()

class MAX (BinaryOperation):
    def __init__ (self, lhs: Amount, rhs: Amount):
        super ().__init__ (lhs, rhs)
    def eval (self):
        return max (self.rhs.eval (), self.lhs.eval ())

class CashFlow:
    def __init__ (self, payment_date: Date, amount: Amount):
        self.payment_date = payment_date
        self.amount = amount
    def eval (self):
        return self.amount.eval ()

class Contract:
    def __init__ (self, *args: CashFlow):
        self.cash_flows = args

def build_call (maturity: Date, strike: float, underlying: Underlying):
    return Contract (
        CashFlow (
            payment_date=maturity, 
            amount=MAX (
                SUB (
                    FloatingAmount (
                        fixing_date=maturity,
                        undl=underlying,
                        quote=100
                    ),
                    FixedAmount (val=strike)
                ), 
                FixedAmount (val=0)
            )
        )
    )



'''
from itertools import groupby

class Payoff_:

    #public:

        def __init__ (self, func, grad=None, hess=None):
            self.func = func
            self.grad = grad
            self.hess = hess
            
        def add_ctrl_func (self, *ctrl_func):
            for idx, ctrl_fun in enumerate (ctrl_func):
                name = 'ctrl_func' if idx == 0 else 'ctrl_func_' + str (idx)
                setattr (self, name, ctrl_fun)
            return self

class Option:

    #public:

        def __init__ (self, payoff=None, mat=None, opts=None):
            if payoff is not None: self.payoff = payoff
            if mat is not None: self.mat = mat
            self.opts = [({'opt': self, 'wght': 1})] if opts is None else opts

        def __add__ (self, opt):
            return Option (opts=self.opts + opt.opts)

        def __sub__ (self, opt):
            return self + (-opt)

        def __mul__ (self, wght):
            return Option (opts=[{'opt' : opt_wght ['opt'], 'wght' : wght * opt_wght ['wght']} for opt_wght in self.opts])

        def __neg__ (self):
            return Option (opts=[{'opt' : opt_wght ['opt'], 'wght' : -opt_wght ['wght']} for opt_wght in self.opts])

        def black_scholes_price (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_price (mdl, time) for opt in self.opts])

        def black_scholes_delta (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_delta (mdl, time) for opt in self.opts])

        def black_scholes_dollargamma (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_dollargamma (mdl, time) for opt in self.opts])

        def black_scholes_vega (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_vega (mdl, time) for opt in self.opts])
'''