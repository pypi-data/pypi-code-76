# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 11:08:56 2021

@author: yasse
"""

# =============================================================================
#  Imports
# =============================================================================
import requests
import pandas as pd
from . import ipaddr as u

# =============================================================================
# Buy one stock
# =============================================================================

def buyStock(symbol, amount):
    """
    This function allows you to buy a specific amount of shares of a certain 
    stock. For example, buying 3 shares of AAPL. This function will be 
    executed instantly and will succeed only if the market is open.

        Args:
            symbol: a ticker symbol or stock symbol (ex: AAPL for Apple)
            amount: number of shares 
    """

    try:
        int(amount)
    except:
        raise ValueError("""The amount must be an integer""")


    amount = int(amount)
    url_s = u.url+ '/private/' + u.token + '/buy'
    body ={'symbol': symbol, 'amount': amount}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")



# =============================================================================
# sell one stock
# =============================================================================
	
def sellStock(symbol, amount):
    """
    This function allows you to sell a specific amount of shares of a certain 
    stock you own. For example, sellinging 3 shares of AAPL. This function 
    will be executed instantly and will succeed only if the market is open
    and you own more or equal than the amount you sell.

        Args:
            symbol: a ticker symbol or stock symbol (ex: AAPL for Apple)
            amount: number of shares 
    """


    try:
        int(amount)
    except:
        raise ValueError("""The amount must be an integer""")


    amount = int(amount)
    url_s = u.url+ '/private/' + u.token + '/sell'
    body ={'symbol': symbol, 'amount': amount}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")



# =============================================================================
# get portfolio
# =============================================================================

def getPortfolio():
    """
    This function returns a dictionary that contains the amount of shares you 
    own from each stock.
    """


    url_g = u.url + '/private/' + u.token + '/getPortfolio'
    response = requests.get(url_g)

    return response.json()


# =============================================================================
# get saldo
# =============================================================================

def getSaldo():
    """
    This function returns an integer representing your current balance
    """


    url_g = u.url + '/private/' + u.token + '/getSaldo'
    response = requests.get(url_g)

    return response.json()


# =============================================================================
# get Hisory
# =============================================================================

def getHistory():
    """
    This function will return a dictionary that contains every historical 
    transaction you've made whether its buying or selling.
    """


    url_g = u.url + '/private/' + u.token + '/getHistory'
    response = requests.get(url_g)
	
    history = pd.DataFrame(response.json())
    history.index += 1
	
    return history

