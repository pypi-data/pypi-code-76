#!/usr/bin/env python
# coding: utf-8

# In[1]:


__version__ = 'v20210207'


# # Yahoo Finance

# In[2]:


from datetime import datetime
import requests
import re
import csv
import os

def get_from_yahoo_finance( # update: 2021-02-06
    symbol='^GSPC', save_dirpath='./downloads_yahoo',
    datetime1=datetime(1800,1,1), datetime2=datetime(3000,1,1), verbose=False,
):
#     period1 = int(datetime1.timestamp())
#     period2 = int(datetime2.timestamp())
    period1 = int((datetime1 - datetime(1970, 1, 1)).total_seconds()) # https://stackoverflow.com/questions/59199985/why-is-datetimes-timestamp-method-returning-oserror-errno-22-invalid-a
    period2 = int((datetime2 - datetime(1970, 1, 1)).total_seconds()) # https://stackoverflow.com/questions/59199985/why-is-datetimes-timestamp-method-returning-oserror-errno-22-invalid-a
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
    if verbose: print('url =', url)

    r = requests.get(url)
    if verbose: print('status_code =', r.status_code)
    if r.status_code == 404:
        raise(Exception(f'Brad error: Connection failed. Check if the url is valid: {url}'))
    if verbose: print('headers =', r.headers)

    content_disp = r.headers.get('content-disposition',float('nan'))
    if isinstance(content_disp,str) and (len(content_disp.strip()) > 0):
        m = re.search('filename[\s]*=(.+)', content_disp)
        if m:
            filename = m.group(1).strip()
        else:
            filename = f'{symbol}.csv'
    else:
        filename = f'{symbol}.csv'

    if not os.path.exists(save_dirpath): os.makedirs(save_dirpath)
    filepath = os.path.join(save_dirpath, filename)
    if verbose: print('filepath =',filepath)
    with open(filepath,'wb') as f:
        size = f.write(r.content)
        if verbose: print('filesize =',size)

    with open(filepath,'r') as f:
        reader = csv.DictReader(f)
        quotes = []
        for row in reader:
            quotes.append(row)
            
    return quotes

if __name__ == '__main__':
    quotes = get_from_yahoo_finance(symbol='^GSPC', save_dirpath='./downloads_yahoo', verbose=True) # S&P 500
    # quotes = get_from_yahoo_finance(symbol='AAPL')


# # Naver Finance

# In[ ]:


import requests
# !pip install beautifulsoup4
from bs4 import BeautifulSoup
import csv
import re     # ref) https://en.wikipedia.org/wiki/Regular_expression
import os

def naver_finance_extract_header(trs):
    headers = []
    for i, rhead in enumerate(trs):
        for cell in rhead.find_all('th'):
            if i > len(headers)-1: headers.append([]) # initialize row

            cell_value = cell.text.strip()

            idxs_nan = [j for j, h in enumerate(headers[i]) if not isinstance(h,str)]

            # multi-cell
            rowspan = int(cell['rowspan']) if 'rowspan' in cell.attrs.keys() else 1
            colspan = int(cell['colspan']) if 'colspan' in cell.attrs.keys() else 1
            for r in range(rowspan):
                for c in range(colspan):
                    if r == 0:
                        if len(idxs_nan) == 0:
                            headers[i+r].append(cell_value)
                        else:
                            headers[i+r][idxs_nan[c]] = cell_value

                    else:
                        if i+r > len(headers)-1: headers.append([]) # initialize row

                        # initialize column
                        if (c == 0) and (len(headers[i+r]) < len(headers[i+r-1]) - colspan):
                            headers[i+r] += [float('nan')] * (len(headers[i+r-1]) - colspan - len(headers[i+r]))
                        elif (c == 0) and (len(headers[i+r]) > len(headers[i+r-1]) - colspan):
                            raise(Exception('Brad error: Unknown header structure...'))

                        if len(idxs_nan) == 0:
                            headers[i+r].append('')
                        else:
                            headers[i+r][idxs_nan[c]] = ''

    assert len(set([len(h) for h in headers])) <= 1
    header = ['\n'.join(rs).strip() for rs in zip(*headers)]
    
    return header, headers

def naver_finance_extract_paging(soup):
    if soup.find('div', {'class':'paging'}) is not None:
        paging = [p.text.strip() for p in soup.find('div', {'class':'paging'}).find_all('a')]
    elif len(soup.find_all('table')) == 2:
        paging = [p.text.strip() for p in soup.find_all('table')[-1].find_all('td')]
    else:
        raise(Exception(f'Brad error: failed to detect paging...'))
    return paging

def naver_finance_extract_data_from_page(url_daily, verbose=False):
    #--- connect to the page --------------
#     r = requests.get(url_daily)
    # https://towardsdatascience.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf
    r = requests.get(url_daily, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',})
    if verbose: print('status_code =', r.status_code)
    if verbose: print('headers =', r.headers)
    if r.status_code == 404:
        raise(Exception(f'Brad error: Connection failed. Check if the url is valid: {url_daily}'))

    soup = BeautifulSoup(r.content, "html.parser")
    
    #--- extract table header from the page ---
    trs = (soup.find('thead').find_all('tr') if soup.find('tbody') is not None else soup.find('table').find_all('tr'))
    header, _ = naver_finance_extract_header(trs)
    if verbose: print('>> HEAD :::',header)

    #--- extract table data from the page ---
    rows = []
    trs = (soup.find('tbody').find_all('tr') if soup.find('tbody') is not None else soup.find('table').find_all('tr'))
    for row in trs:
        data = [td.text.strip() for td in row.find_all('td')]
        
        if len(data) == len(header):
            rows.append({h:v for h,v in zip(header, data)})
            if verbose: print('>> DATA :::', data)
        else:
            if verbose: print('>> SKIP!!! :::', data)

    paging = naver_finance_extract_paging(soup)
    if verbose: print('>> PAGE :::', paging)
        
    return rows, paging, soup

def naver_finance_extract_data_from_multi_pages(url_sample, rows_all=[], start_page=1, end_page=1, verbose=False):
    rows_new, rows_all_ = [], rows_all[1:]
    for page in range(start_page, end_page+1):
        url_daily = re.sub('&page=[\d]*$', '&page=%s'%(page), url_sample)
        rows, paging, soup = naver_finance_extract_data_from_page(url_daily, verbose=verbose)
        
        if re.search('[\d,]+',paging[-1]) and (page > int(paging[-1].replace(',',''))):
            break
        else:
            print('url =', url_daily)
            for row in rows:
#                 if row in rows_all_:
                if row in rows_all_[:1]:
                    rows_all = rows_new + rows_all_ # update and end if there is a common row
                    return rows_all
                else:
                    rows_new.append(row)
            
    rows_all = rows_new + rows_all # update
    return rows_all

def get_from_naver_finance(url_sample='', save_dirpath="./data/naver/", reset_db=False, MAX_PAGE_NUM=9999):
    #-- define file name & symbol ----------------
    m = re.search('(?:marketindexCd=|code=)(.*)&page=', url_sample)
    if m:
        symbol = m.group(1)
    else:
        m = re.search('marketindex/(.*).nhn', url_sample)
        if m:
            symbol = m.group(1)
        else:
            raise(Exception(f'Brad error: failed to extract a file name from url: {url_sample}'))

    filepath = os.path.join(save_dirpath, symbol+'.csv')
    
    #--- extract data ----------------------------
    if os.path.isfile(filepath) and (not reset_db):
        # read csv file
        with open(filepath, newline='', encoding="utf-8") as f: 
            reader = csv.DictReader(f)
            quotes = [row for row in reader]
        
        # update
        quotes = naver_finance_extract_data_from_multi_pages(url_sample, rows_all=quotes, start_page=1, end_page=MAX_PAGE_NUM, verbose=False)
        
    else:
        # extract data from scratch
        print("> File not found in the DB or DB reset chosen. Now, searching the internet to download information...")
        quotes = naver_finance_extract_data_from_multi_pages(url_sample, rows_all=[], start_page=1, end_page=MAX_PAGE_NUM, verbose=False)
        print("> Downloading completed!")
        
    #--- write csv file ------------------------
    if not os.path.exists(save_dirpath): os.makedirs(save_dirpath)
    with open(filepath, 'w', newline='', encoding="utf-8") as f:
        fieldnames = quotes[0].keys() if len(quotes)>0 else []
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(quotes)
        print(f"> the data is saved in the path: {filepath}")
        
    return quotes, symbol

#------------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    save_dirpath="./downloads_naver"
    
    samples = [
        ('USDKRW','https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page=1'),
        ('KOSPI','https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI&page=1'),
        ('국내 금','https://finance.naver.com/marketindex/goldDailyQuote.nhn?&page=1'),
        ('휘발유','https://finance.naver.com/marketindex/oilDailyQuote.nhn?marketindexCd=OIL_GSL&page=1'),
        ('구리','https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=2&marketindexCd=CMDT_CDY&page=1'),
        ('옥수수','https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=2&marketindexCd=CMDT_C&page=1'),
        ('삼성SDI','https://finance.naver.com/item/sise_day.nhn?code=006400&page=1'),
        ('삼성전자','https://finance.naver.com/item/sise_day.nhn?code=005930&page=1'),
        ('LG전자','https://finance.naver.com/item/sise_day.nhn?code=066570&page=1'),
        ('대한항공','https://finance.naver.com/item/sise_day.nhn?code=003490&page=1'),
        ('SK이노베이션','https://finance.naver.com/item/sise_day.nhn?code=096770&page=1'),
        ('NAVER','https://finance.naver.com/item/sise_day.nhn?code=035420&page=1'),
        ('카카오','https://finance.naver.com/item/sise_day.nhn?code=035720&page=1'),
    ]
    quotes, symbols = {}, {}
    for name, url_sample in samples:
        quotes[name], symbols[name] = get_from_naver_finance(url_sample=url_sample, save_dirpath=save_dirpath, reset_db=False)


# In[ ]:




