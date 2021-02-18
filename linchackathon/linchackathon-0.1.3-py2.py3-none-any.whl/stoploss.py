# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:21:56 2021

@author: yasse
"""

# =============================================================================
#  Imports
# =============================================================================
import requests
from . import ipaddr as u

# =============================================================================
# Get stoploss
# =============================================================================

def getStoplosses():
    """
    This function returns a list of all the stoplosses that you have placed
    (completed and active)
    """

    url_g = u.url+ '/private/' + u.token + '/stoploss'
    with requests.Session() as session:
        get = session.get(url_g)
		
    return get.json()


# =============================================================================
# Place Stoploss
# =============================================================================

def placeStoploss(symbol, trigger, amount):
    """
    This function places a stoploss to sell a specific stock with a specific amount
    of shares when the price of that stock hits the trigger AKA falls below the stoploss. 

        Args:
            symbol: A ticker symbol or stock symbol (ex: AAPL for Apple)
            Amount: number of shares
            trigger : Lower bound of the stock price. This is an actual price change 
            and not a percentage change.

        Example:
            The AAPL price currently is at 160 per share and we place an stoploss
            so :
                placeOrder('AAPL', 150, 3)

            then this order will wait until the price of the AAPL hits 150 and 
            then sells 3 shares.

            If the AAPL price is currently at 100 and we place the same stoploss
            then it will be executed instantly and sell 3 shares for 100. Unless
            its a weekend of course then it will wait till the market is open.
    """

    try:
        int(amount)
        int(trigger)
    except:
        raise ValueError("""The amount and price must be integers""")


    amount = int(amount)
    trigger = int(trigger)
	
    url_s = u.url+ '/private/' + u.token + '/stoploss'
    body ={'symbol': symbol, 'trigger': trigger, 'amount' : amount}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")




# =============================================================================
# Delete Stoploss
# =============================================================================

def deleteStoploss(symbol):
    """
    This function is used to delete an stoploss on a specific stock that is still 
    active. 

        Args:
            symbol: A ticker symbol or stock symbol (ex: AAPL for Apple)
    """

    url_s = u.url+ '/private/' + u.token + '/stoploss'
    body ={'symbol': symbol}
    with requests.Session() as session:
        post = session.delete(url_s, json= body)

    return post.content.decode("utf-8")
