# -*- coding: utf-8 -*-

"""
LINC
======

This package is required in order to participate in the LINC Hackathon (Lund University Finance Society). 


"""

from .auth import init
from .private import buyStock, sellStock, getPortfolio, getSaldo, getHistory
from .public import getTickers, getTickersNames, getStock, getStockHistory
from .orders import placeOrder, deleteOrder, getOrders
from .stoploss import placeStoploss, deleteStoploss, getStoplosses
