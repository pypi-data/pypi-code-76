import bs4
import requests
import re
import StockStalker.present as present
import pandas as pd
from munch import munchify

def getCrypto(cryptoTicker, format="Dict"):
    try:
        page = requests.get(f"https://finance.yahoo.com/quote/{cryptoTicker}-USD")
    except:
        raise Exception(f"Ticker '{cryptoTicker}' does exist / cannot get page")

    soup = bs4.BeautifulSoup(page.content, 'html.parser')


    price = getPrice(soup)

    getChanges = getChange(soup)
    numChange = getChanges[0]
    percChange = getChanges[1]

    ranges = getRange(soup)
    low = ranges[0]
    high = ranges[1]

    open = present.getOpen(soup)
    close = present.getPrevClose(soup)

    dataDict = {
        "Symbol": cryptoTicker,
        "Currency": "USD",
        "Price": price,
        "Change": [{
            "change": numChange,
            "percentageChange": percChange
        }],
        "Ranges": [{
            "Low": low,
            "High": high
        }],
        "Open": open,
        "previousClose": close,
    }

    if format == "Dict":
        return dataDict
    if format == "DataFrame":
        return pd.DataFrame(dataDict)
    if format == "Object":
        return munchify(dataDict)

    raise Exception("Invalid Format Option")




def getPrice(soup):
    hits = soup.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")

    if "," in hits.text:

        hits = hits.text.replace(",", "")

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



    return [float(numChange), percChange]


def getRange(soup):
    hits = soup.find(attrs={"data-test": "DAYS_RANGE-value"})

    if hits == None:
        return "N/A"

    split = hits.text.split("-")

    try:

        if "," in split[0]:
           low = float(split[0].replace(",", ""))
        else:
            low = float(split[0])
        if "," in split[1]:
            high = float(split[1].replace(",", ""))
        else:
            high = float(split[1])

    except:
        return "N/A"
    return [low, high]


