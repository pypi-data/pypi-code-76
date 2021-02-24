import requests
import bs4
import re
import pandas as pd
from ftplib import FTP
from munch import munchify


import os
import shutil

if os.path.exists("cache") == False:
    os.mkdir("cache")
else:
    shutil.rmtree("cache")




def getLiveData(ticker, format="Dict"):
    page = None
    try:
        page = requests.get(f"https://finance.yahoo.com/quote/{ticker}")
    except:
        raise Exception(f"Ticker '{ticker}' does exist / cannot get page")

    soup = bs4.BeautifulSoup(page.content, 'html.parser')


    price = getPrice(soup)

    changes = getChange(soup)
    numChange = changes[0]
    percChange = changes[1]

    pe = getPEttm(soup)

    ranges = getRange(soup)
    low = ranges[0]
    high = ranges[1]

    open = getOpen(soup)
    prevClose = getPrevClose(soup)

    eps = getEPS(soup)

    mktCap = getMktCap(soup)

    volume = getVolume(soup)


    dataDict = {
        "Symbol": ticker,
        "Price": price,
        "Change": [{
            "change": numChange,
            "percentageChange": percChange
        }],
        "P/E": pe,
        "Ranges": [{
            "Low": low,
            "High": high
        }],
        "Open": open,
        "previousClose": prevClose,
        "EPS": eps,
        "marketCap": mktCap,
        "volume": volume
    }

    if format == "Dict":
        return dataDict
    if format == "DataFrame":
        return pd.DataFrame(dataDict)
    if format == "Object":
        return munchify(dataDict)

    raise Exception("Invalid Format Option")




def getPrice(soup):
    hits = soup.find(class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')

    if hits==None:
        return "N/A"

    if "," in hits.text:
        hits = hits.text.replace(",", "")
    else:
        hits = hits.text

    try:
        return float(hits)
    except:
        return "N/A"


def getChange(soup):
    hits = soup.find(class_='Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)')

    if hits == None:
        hits = soup.find(class_='Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)')

    if hits == None:
        return "N/A"

    try:
        numChange = hits.text.split(" ")[0].replace("+", "")
        percChange = re.search(r'\((.+)\)', hits.text).group(0).split("(")[1].split(")")[0]
    except:
        return "N/A"

    if "," in numChange:
        numChange = numChange.replace(",", "")

    return [float(numChange), percChange]

def getPEttm(soup):

    hits = soup.find(attrs={"data-reactid":149})

    if hits == None:
        return "N/A"

    val = hits.text.replace(",", "")

    try:
        return float(val)
    except:
        return val

def getRange(soup):
    hits = soup.find(attrs={"data-reactid": 117})
    if hits == None:
        return "N/A"

    split = hits.text.split("-")
    try:
        low = float(split[0])
        high = float(split[1])
    except:
        return "N/A"
    return [low, high]


def getOpen(soup):
    hits = soup.find(attrs={"data-test": "OPEN-value"})

    if hits == None:
        return "N/A"

    if "," in hits.text:
        hits = hits.text.replace(",", "")
        final = float(hits)


    try:
        final = float(hits)
    except:
        try:
            final = float(hits.text)
        except:
            return "N/A"
    return final

def getPrevClose(soup):
    hits = soup.find(attrs={"data-test": "PREV_CLOSE-value"})
    if hits == None:
        return "N/A"

    if "," in hits.text:
        hits = hits.text.replace(",", "")
        final = float(hits)
    else:
        final = float(hits.text)


    return final

def getEPS(soup):
    hits = soup.find(attrs={"data-test": "EPS_RATIO-value"})
    try:
        final = float(hits.text)
    except:
        return "N/A"
    return final

def getMktCap(soup):
    hits = soup.find(attrs={"data-test": "MARKET_CAP-value"})
    try:
        final = str(hits.text)
    except:
        return "N/A"
    if "B" in final:
        final = final.replace("B", "")
        final = float(final)
        final *= 1000000000
    elif "M" in final:
        final = final.replace("M", "")
        final = float(final)
        final *= 1000000


    return final

def getVolume(soup):
    hits = soup.find(attrs={"data-test": "TD_VOLUME-value"})
    if hits == None:
        return "N/A"

    final = hits.text.replace(",", "", -1)
    final = float(final)

    return final





def getIndex(index):
    if index == "S&P500":
        page = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        return page[0]['Symbol'].tolist()

    if index == "NASDAQ":
        #ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt

        ftp = FTP('ftp.nasdaqtrader.com')
        ftp.login()
        ftp.cwd("SymbolDirectory")

        file = ftp.nlst()[9]

        ftp.retrbinary("RETR " + file, open("cache/nasdaq.txt", 'wb').write)

        df = pd.read_csv("cache/nasdaq.txt", sep="|")["Symbol"].tolist()
        return df

    if index == "NASDAQ.OTHER":
        ftp = FTP('ftp.nasdaqtrader.com')
        ftp.login()
        ftp.cwd("SymbolDirectory")
        file = ftp.nlst()[13]

        ftp.retrbinary("RETR " + file, open("cache/other.txt", 'wb').write)
        df = pd.read_csv("cache/other.txt", sep="|")["NASDAQ Symbol"].tolist()
        return df

    if index == "DOW":
        #https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average
        page = pd.read_html("https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI")[0]["Symbol"].tolist()

        return page

    if index == "NYSE":
        ftp = FTP('ftp.nyse.com')
        ftp.login()
        ftp.cwd("NYSESymbolMapping")
        file = ftp.nlst()[0]

        ftp.retrbinary("RETR " + file, open("cache/nyse.txt", 'wb').write)

        df = pd.read_csv("cache/nyse.txt", sep="|").iloc[:, 0].tolist()
        return df


