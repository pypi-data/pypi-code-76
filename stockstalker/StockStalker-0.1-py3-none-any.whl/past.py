import datetime
import time
import requests
import pandas as pd

date_format = "%m/%d/%Y"

def now():
    return datetime.datetime.utcnow()

def prettyDate(dt):
    return datetime.datetime.strftime(dt, date_format)


def futureError(date):
    raise Exception(f"Supplied Date ({date}) is in the future")


def toUnixStamp(strDate):
    #return datetime.datetime.strptime(strDate, date_format).timestamp()
    return int(pd.Timestamp(strDate).timestamp())




def getPastData(ticker, startDate, toDate, interval="d"):

    start = datetime.datetime.strptime(startDate, date_format)
    end = datetime.datetime.strptime(toDate, date_format)

    current = datetime.datetime.strptime(prettyDate(now()), date_format)

    if start > current:
        futureError(startDate)
    if start > current:
        futureError(startDate)

    if end > start:
        raise Exception("Start date cant be less than destination date")


    if interval not in ["d", "w", "mo"]:
        raise Exception("Interval must be day (d), week (w) or month (mo)")

    startUnix = toUnixStamp(startDate)
    endUnix = toUnixStamp(toDate)


    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={endUnix}&period2={startUnix}&interval=1d&events=history&incl"
    #print(url)

    df = pd.read_csv(url)

    return df

