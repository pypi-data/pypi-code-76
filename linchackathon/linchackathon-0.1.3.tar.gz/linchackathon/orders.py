# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:50:58 2021

@author: yasse
"""

# =============================================================================
#  Imports
# =============================================================================
import requests
from . import ipaddr as u

# =============================================================================
# Get orders
# =============================================================================

def getOrders():
    """
    This function returns a list of all the order that you have placed
    (completed and active)
    """

    url_g = u.url+ '/private/' + u.token + '/order'
    with requests.Session() as session:
        get = session.get(url_g)
		
    return get.json()


# =============================================================================
# Place order
# =============================================================================

def placeOrder(symbol, amount, price):
    """
    This function places an order to buy a specific stock with a specific amount
    of shares when the price of that stock goes below a certain price. 

        Args:
            symbol: A ticker symbol or stock symbol (ex: AAPL for Apple)
            Amount: number of shares
            price : The price for which you want the stock to be under
                    in order to buy

        Example:
            The AAPL price currently is at 160 per share and we place an order
            so :
                placeOrder('AAPL', 2, 150)

            then this order will wait until the price of the AAPL hits 150 and 
            then buys 2 shares.

            If the AAPL price is currently at 100 and we place the same order
            then it will be executed instantly and buy 2 shares for 100. Unless
            its a weekend of course then it will wait till the market is open.
    """

    try:
        int(amount)
        int(price)
    except:
        raise ValueError("""The amount and price must be integers""")


    amount = int(amount)
    price = int(price)
	
    url_s = u.url+ '/private/' + u.token + '/order'
    body ={'symbol': symbol, 'amount': amount, 'price' : price}
    with requests.Session() as session:
        post = session.post(url_s, json= body)

    return post.content.decode("utf-8")




# =============================================================================
# Delete Order
# =============================================================================

def deleteOrder(symbol):
    """
    This function is used to delete an order on a specific stock that is still 
    active. 

        Args:
            symbol: A ticker symbol or stock symbol (ex: AAPL for Apple)
    """

    url_s = u.url+ '/private/' + u.token + '/order'
    body ={'symbol': symbol}
    with requests.Session() as session:
        post = session.delete(url_s, json= body)

    return post.content.decode("utf-8")
