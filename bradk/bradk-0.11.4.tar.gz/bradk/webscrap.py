#!/usr/bin/env python
# coding: utf-8

# In[ ]:


__version__ = 'v20210131'


# In[ ]:


import requests
import os
from tqdm import tqdm

def download_file_from_url( # update: 2021-01-31
    url='http://ftp.mozilla.org/pub/firefox/releases/63.0.3/linux-x86_64/en-US/firefox-63.0.3.tar.bz2',
    save_dirpath='./', save_filename=None, verbose=False,
):
    if verbose: print('cf) firefox: https://ftp.mozilla.org/pub/firefox/releases/')
    if verbose: print('cf) geckodriver: https://github.com/mozilla/geckodriver/releases')
    if verbose: print('cf) chromedriver: https://chromedriver.chromium.org/downloads')
    if verbose: print('>> Downloading file from :', url)
        
    # r = requests.get(url)
    r = requests.get(url, stream=True)
    if verbose: print('>> headers =',r.headers)

    if isinstance(save_filename, str):
        filename = save_filename
    else:
        filename = os.path.basename(url.strip().replace('\\','/')) # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    if len(filename) == 0: raise(Exception(f'Brad error: A zero-length filename. Check the inputs, i.e. save_filename or url: {url}'))
    if verbose: print('>> filename =',filename)

    filesize = int(r.headers.get('Content-Length',0))
    if verbose: print('>> filesize =',filesize)

    if not os.path.exists(save_dirpath): os.makedirs(save_dirpath)
    filepath = os.path.join(save_dirpath, filename)
    with open(filepath,'wb') as f, tqdm(desc=filename, total=filesize, unit='iB', unit_scale=True, unit_divisor=1024) as bar: # https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
        for data in r.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)
            
    return filepath

# filepath_firefox = download_file_from_url(url='http://ftp.mozilla.org/pub/firefox/releases/63.0.3/linux-x86_64/en-US/firefox-63.0.3.tar.bz2')
# filepath_geckodriver = download_file_from_url(url='https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz')


# In[ ]:


import os

def upzip_launch_firefox_in_linux(filepath_firefox=None, filepath_geckodriver=None, verbose=False): # update: 2021-01-31
    if verbose: print('cf) Kaggle web scraping via headless Firefox+selenium: https://www.kaggle.com/dierickx3/kaggle-web-scraping-via-headless-firefox-selenium')
    cmds = []
    cmds += [ # commands for firfox
        f'tar -xvjf "{filepath_firefox}"', # upzip file
#         'chmod -R 777 "./firefox"', # ADD READ/WRITE/EXECUTE CAPABILITES
        'apt-get install -y libgtk-3-0 libdbus-glib-1-2 xvfb', # LAUNCHING FIREFOX, EVEN INVISIBLY, HAS SOME DEPENDENCIES ON SOME SCREEN-BASED LIBARIES
        'export DISPLAY=:99', # SETUP A VIRTUAL "SCREEN" FOR FIREFOX TO USe
        'ls -l /usr/local/bin/',
    ] if isinstance(filepath_firefox,str) else []
    cmds += [ # commands for geckodriver
        f'tar -xvf "{filepath_geckodriver}"', # upzip file
#         'chmod 777 ./geckodriver',
    ] if isinstance(filepath_geckodriver,str) else []
    
    for cmd in cmds:
        result = os.system(cmd)
        if verbose: print(f'[{result}] {cmd}')
        if result != 0: raise(Exception('Brad error: an error occured...'))
            
# upzip_launch_firefox_in_linux(filepath_firefox=filepath_firefox, filepath_geckodriver=filepath_geckodriver)       


# In[ ]:


# !pip install selenium
from selenium import webdriver #ref) https://selenium-python.readthedocs.io/
import os

def initialize_driver_firefox( # last update: 2020-11-14
    firefox_binary="./firefox/firefox", executable_path='/usr/local/bin/geckodriver',
    download_dir=r'C:\Users\bomsoo\Downloads',
    headless=False, window_size=(1920,1080), 
):
    #--- FIRE UP A HEADLESS BROWSER SESSION WITH A "SCREEN SIZE" OF 1920x1080 ----
    # Kaggle web scraping via headless Firefox+selenium: https://www.kaggle.com/dierickx3/kaggle-web-scraping-via-headless-firefox-selenium
    options = webdriver.firefox.options.Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--window-size=%s,%s"%window_size)

    capabilities = webdriver.common.desired_capabilities.DesiredCapabilities().FIREFOX
    capabilities["marionette"] = True
    
    #--- disable the "Save as this file" window ---------------------------
    if not os.path.exists(download_dir): os.makedirs(download_dir)
    #https://stackoverflow.com/questions/37077600/how-to-handle-save-file-dialog-box-in-firefox-using-selenium-with-python
    fp = webdriver.FirefoxProfile()
    fp.set_preference('browser.download.folderList', 2) 
    fp.set_preference('browser.download.manager.showWhenStarting', False)
    fp.set_preference('browser.download.dir', download_dir)
    fp.set_preference('browser.helperApps.neverAsk.openFile', 'text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml')
    fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml')
    fp.set_preference('browser.helperApps.alwaysAsk.force', False)
    fp.set_preference('browser.download.manager.alertOnEXEOpen', False)
    fp.set_preference('browser.download.manager.focusWhenStarting', False)
    fp.set_preference('browser.download.manager.useWindow', False)
    fp.set_preference('browser.download.manager.showAlertOnComplete', False)
    fp.set_preference('browser.download.manager.closeWhenDone', False)

    #--- create driver ------------------------------
    driver = webdriver.Firefox(
        options=options, 
        capabilities=capabilities, 
        firefox_binary=firefox_binary, 
        executable_path=executable_path,
        firefox_profile=fp,
    )
    
    return driver

def initialize_driver_chrome():
    #--- disalbe image loading for fast loading --------------
    # https://tarunlalwani.com/post/selenium-disable-image-loading-different-browsers/
    options = webdriver.ChromeOptions()
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    #--- create driver ------------------------------
#     driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options)

    return driver


# In[ ]:


from selenium import webdriver #ref) https://selenium-python.readthedocs.io/
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_csv_from_yahoo_finance_w_selenium(driver, symbol='^GSPC', verbose=False): # update: 2021-01-31
    if verbose: print(symbol, end=' ')
        
    #--- leave only one tab ------------------------------
    for i in range(1, len(driver.window_handles)): # keep only one tab
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

    #--- launch a target webpage --------------------------
    url = f'https://finance.yahoo.com/quote/{symbol}/history?p={symbol}'
    driver.get(url)

    #--- click buttons to download historical data --------
    by_whats = [ # https://www.programcreek.com/python/index/8077/selenium.webdriver.common.by.By
        (By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/div[1]/div/div/div/span'),
        (By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/div[1]/div/div/div/div/div/ul[2]/li[4]/button/span'),
        (By.LINK_TEXT, 'Download'),]    
    for i, (by, what) in enumerate(by_whats): 
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((by, what))).click()
        if verbose: print(f'...click{i+1}/{len(by_whats)}', end='' if i+1<len(by_whats) else '\n')

    return driver

#######################################################
if __name__ == '__main__':
    #--- initialize driver --------------------------------
    driver = initialize_driver_firefox(
    #     download_dir=r'C:\Users\bomsoo\bomsoo1\python\_web_scrap\data_yahoo', # absolute path
    #     headless=False, 
    #     firefox_binary=r'C:\Program Files\Mozilla Firefox\firefox.exe', 
    #     executable_path='geckodriver.exe',
        #--- only for Kaggle --------------
        download_dir='./downloads_yahoo',
        headless=True, 
        firefox_binary='./firefox/firefox', 
        executable_path='./geckodriver',
    )
    driver.implicitly_wait(5) # https://stackoverflow.com/questions/44119081/how-do-you-fix-the-element-not-interactable-exception
    driver.set_page_load_timeout(120) # https://stackoverflow.com/questions/17533024/how-to-set-selenium-python-webdriver-default-timeout

    #--- download csv for each symbol ---------------------
    from datetime import datetime
    import matplotlib.pyplot as plt

    symbols=['^GSPC','AAPL'] # ex) S&P 500, Apple, etc.

    for i, symbol in enumerate(symbols):
        print(f'[{i+1}/{len(symbols)}] {datetime.now()} ::: ', end='')

        try:
            driver = download_csv_from_yahoo_finance_w_selenium(driver, symbol=symbol, verbose=True)
        except Exception as err:
            driver.save_screenshot("screenshot.png")
            img = plt.imread('screenshot.png')
            fig, ax = plt.subplots(figsize=(20,20))
            ax.imshow(img)            
            plt.show()
            print('Brad error:',err)

    #--- close driver --------------------------
    driver.close()


# In[ ]:


from datetime import datetime
import requests
import re
import csv

def download_csv_from_yahoo_finance( # update: 2021-01-31
    symbol='^GSPC', save_dirpath='./downloads_yahoo',
    date1=datetime(1800,1,1), date2=datetime(3000,1,1), verbose=False,
):
    period1 = int(datetime.timestamp(date1))
    period2 = int(datetime.timestamp(date2))
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
    quotes = download_csv_from_yahoo_finance(symbol='^GSPC', verbose=True)
    # quotes = download_csv_from_yahoo_finance(symbol='AAPL')


# In[ ]:




