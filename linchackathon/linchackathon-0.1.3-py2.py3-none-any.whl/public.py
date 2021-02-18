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
import numpy as np
from . import ipaddr as u


# =============================================================================
# Getting all the tickers
# =============================================================================

def getTickers():
    """
    This function returns a list with all the tickers.
    
    """

    ticker_url = u.url+'/public/tickers'
    response = requests.get(ticker_url)

    return response.json()['tickers']



def getTickersNames():
    """
    This function returns a dataframe with all the tickers included and the names 
    of the companies. This function uses the getTickers() function and also yahoo
    finance to fine the names of the companies.
    
    """

    tickers_list = getTickers()

    def get_info(symbol):
        url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
        result = requests.get(url).json()

        for x in result['ResultSet']['Result']:
            if x['symbol'] == symbol:
                return x['name']
            else:
                return 'Unknown'
    
    names_list = [get_info(j) for j in tickers_list]
    tickers_df= pd.DataFrame( data = np.array([tickers_list, names_list]).transpose(), 
                              columns = ['Ticker', 'Company name'])
    tickers_df.index += 1

    return tickers_df

# =============================================================================
# Getting One point data One ticker
# =============================================================================

def getStock(ticker):
    """
    This function takes in one argument, which is the ticker, as a string 
    and returns the current price of the stock.

        Args:
            ticker : the ticker symbol or stock symbol (ex: AAPL for Apple)

    """

    if type(ticker) == str:
    	pass
    else:
    	raise ValueError("""
    			   
    	You have entered a wrong value. Make sure that the ticker is in the 
    	form of a string like : 
    		
    		'AAPL'

    		""")
    if ticker not in u.tickers:
        raise NameError("""

                The Ticker you included is incorrect.
                Check the Tickers available by running 'getTickers()'
                
                """)
			
    gstock_url = u.url+ '/public/' + ticker 
    response = requests.get(gstock_url)
	
    return response.json()[0]



# =============================================================================
# Getting Multiple point data One ticker
# =============================================================================

def getStockHistory(ticker, daysback):
    """
    This function utilizes the getStock function and returns the history. It 
    requires the ticker and the ammount of days in the past. You can also
    insert 'all' in the ticker argument to get the history of all the stocks
    instead of a specifc one.

        Args:
            ticker : the ticker symbol or stock symbol (ex: AAPL for Apple)
            daysback : an integer specifying the number of days to scrape from
                       in the past

    """

    if type(ticker) == str:
    	pass
    else:
    	raise ValueError("""
    			   
    	You have entered a wrong value. Make sure that the ticker is in the 
    	form of a string like : 
    		
    		'AAPL'
    		""")
       
    

    if ticker not in u.tickers:
        raise NameError("""

                The Ticker you included is incorrect.
                Check the Tickers available by running 'getTickers()'
                
                """)


    gstock_url = u.url+ '/public/' + ticker + f'/{daysback}'
    response = requests.get(gstock_url)

    return response.json()['result']

