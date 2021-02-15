import pandas_datareader as web
from datetime import datetime

year = int(datetime.today().year) - 1
start = datetime(year, 1, 1)
end = datetime.now()


def sma(ticker, period):
    symbol = web.DataReader(ticker, 'yahoo', start, end)
    return symbol['Adj Close'].rolling(window=period).mean()

def ema(ticker, period):
    symbol = web.DataReader(ticker, 'yahoo', start, end)
    return symbol.Close.ewm(span=period, adjust=False).mean()

def bollingerBands(ticker, period, std):
    symbol = web.DataReader(ticker, 'yahoo', start, end)

    symbol['20sma'] = symbol['Adj Close'].rolling(window=period).mean()
    symbol['20std'] = symbol['Adj Close'].rolling(window=period).std()

    symbol['Upper Band'] = symbol['20sma'] + (symbol['20std'] * std)
    symbol['Lower Band'] = symbol['20sma'] - (symbol['20std'] * std)

    return symbol['Upper Band'], symbol['Lower Band']

def LowerBand(ticker, period, std):
    symbol = web.DataReader(ticker, 'yahoo', start, end)
    symbol['20std'] = symbol['Adj Close'].rolling(window=period).std()
    symbol['Lower Band '] = symbol['20ma'] - (symbol['20std'] * std)
    return symbol['Lower Band']

def UpperBand(ticker, period, std):
    symbol = web.DataReader(ticker, 'yahoo', start, end)
    symbol['20std'] = symbol['Adj Close'].rolling(window=period).std()
    symbol['Upper Band '] = symbol['20ma'] + (symbol['20std'] * std)
    return symbol['Upper Band']

def MACD(ticker, signal, short, long):
    symbol = web.DataReader(ticker, 'yahoo', start, end)

    short_ema = symbol.Close.ewm(span=short, adjust=False).mean()
    long_ema = symbol.Close.ewm(span=long, adjust=False).mean()

    MACD = short_ema - long_ema
    sig = MACD.ewm(span=signal, adjust=False).mean()

    symbol['macd'] = MACD
    symbol['signal'] = sig

    return symbol['macd']








