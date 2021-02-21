import pandas as pd
import requests
import parsel
import requests
import re
import json
from tqdm import tqdm
import concurrent.futures


def get_good_stock(page=5):
    url = "http://fund.eastmoney.com/data/rankhandler.aspx"
    headers = {
        "Host": "fund.eastmoney.com",
        "Referer": "http://fund.eastmoney.com/data/fundranking.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63"
    }
    urls = []

    def get_urls(page):
        params = {
            "op": "ph",
            "sc": "6yzf",
            "sd": "2020-02-11",
            "ed": "2021-02-11",
            "pi": str(page),
            "dx": "1",
        }
        response = requests.get(url, headers=headers, params=params)
        response.encoding = response.apparent_encoding
        data = re.findall('var rankData = {datas:(.*),allRe', response.text)[0]
        data = eval(data)
        list = ['http://fund.eastmoney.com/' +
                re.findall(r'(\d*),', i)[0]+'.html' for i in data]
        for i in list:
            urls.append(i)
    for i in range(1, page):
        get_urls(i)

    def get_stock(url):
        df = pd.read_html(url)
        return list(df[5]['股票名称'])
    stocks = []

    def main(url):
        print(url)
        for i in get_stock(url):
            stocks.append(i)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            print(url)
            executor.submit(main, url)
    stock = {}
    for i in stocks:
        stock[i] = stocks.count(i)
    df = pd.DataFrame(stock, index=['count']).T
    df = df.sort_values(by='count', ascending=False)
    df.to_csv('count.csv', encoding='utf8')
    return df
