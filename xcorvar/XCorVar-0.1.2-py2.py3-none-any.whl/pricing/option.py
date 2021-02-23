# coding: utf-8

from itertools import groupby

class Payoff:

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

class Opt:

    #public:

        def __init__ (self, payoff=None, mat=None, opts=None):
            if payoff is not None: self.payoff = payoff
            if mat is not None: self.mat = mat
            self.opts = [({'opt': self, 'wght': 1})] if opts is None else opts

        def __add__ (self, opt):
            return Opt (opts=self.opts + opt.opts)

        def __sub__ (self, opt):
            return self + (-opt)

        def __mul__ (self, wght):
            return Opt (opts=[{'opt' : opt_wght ['opt'], 'wght' : wght * opt_wght ['wght']} for opt_wght in self.opts])

        def __neg__ (self):
            return Opt (opts=[{'opt' : opt_wght ['opt'], 'wght' : -opt_wght ['wght']} for opt_wght in self.opts])

        def black_scholes_price (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_price (mdl, time) for opt in self.opts])

        def black_scholes_delta (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_delta (mdl, time) for opt in self.opts])

        def black_scholes_dollargamma (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_dollargamma (mdl, time) for opt in self.opts])

        def black_scholes_vega (self, mdl, time=0):
            return sum ([opt ['wght'] * opt ['opt'].black_scholes_vega (mdl, time) for opt in self.opts])