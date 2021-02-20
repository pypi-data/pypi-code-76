# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 10:22:47 2020

@author: Peter
"""

import os; os.chdir("S:/siat")
from siat.financials import *

#==============================================================================
tickers=['AMZN','EBAY','BABA','JD','VIPS']
roa=compare_snapshot(tickers,'ROA')
roe=compare_snapshot(tickers,'ROE')
beta=compare_snapshot(tickers,'beta')

tickers=['AMZN','EBAY','SHOP','BABA','JD','PDD','VIPS']
cr=compare_snapshot(tickers,'Current Ratio')
dtoe=compare_snapshot(tickers,'Debt to Equity')
teps=compare_snapshot(tickers,'Trailing EPS')
roe=compare_snapshot(tickers,'ROE')
hpinst=compare_snapshot(['AAPL','MSFT','BRKB'],'Held Percent Institutions')

#==============================================================================
rates=get_stock_profile('AAPL',info_type='fin_rates')

tickers=['AAPL','MSFT','WMT','FB','QCOM']
cr=compare_snapshot(tickers,'Current Ratio')
beta=compare_snapshot(tickers,'beta')
dtoe=compare_snapshot(tickers,'Debt to Equity')
dtoe=compare_snapshot(tickers,'?')
teps=compare_snapshot(tickers,'Trailing EPS')
tpe=compare_snapshot(tickers,'Trailing PE')

tickers1=['AMZN','EBAY','GRPN','BABA','JD','PDD','VIPS']
gm=compare_snapshot(tickers1,'Gross Margin')
pm=compare_snapshot(tickers1,'Profit Margin')

df1,df2=compare_history('AAPL','Current Ratio')
df1,df2=compare_history('AAPL',['Current Ratio','Quick Ratio'])
df1,df2=compare_history('AAPL',['BasicEPS','DilutedEPS'])
df1,df2=compare_history('AAPL',['Current Ratio','BasicEPS'],twinx=True)
df1,df2=compare_history('AAPL',['BasicPE','BasicEPS'])
df1,df2=compare_history('AAPL',['BasicPE','BasicEPS'],twinx=True)

df1,df2=compare_history(['AAPL','MSFT'],['BasicPE','BasicEPS'])
df1,df2=compare_history(['AAPL','MSFT'],['BasicPE','BasicEPS'],twinx=True)
df1,df2=compare_history(['AAPL','MSFT'],'BasicEPS',twinx=True)

cr=compare_history(['INTL','QCOM'],'Current Ratio',twinx=True)

cr=compare_history(['600519.SS','000002.SZ'],'Current Ratio',twinx=True)
#==============================================================================

Chinabanks = ["1398.HK","0939.HK","3988.HK","1288.HK"]
USbanks=["BAC", "TD","PNC"]
Japanbanks = ["8306.T","7182.T","8411.T"]

esg=compare_snapshot(Chinabanks+USbanks+Japanbanks,'Total ESG')
ep=compare_snapshot(Chinabanks+USbanks+Japanbanks,'Environment Score')
csr=compare_snapshot(Chinabanks+USbanks+Japanbanks,'Social Score')
emp=compare_snapshot(Chinabanks+USbanks+Japanbanks,'Employees')
gov=compare_snapshot(Chinabanks+USbanks+Japanbanks,'Governance Score')
roe=compare_snapshot(Chinabanks+USbanks+Japanbanks,'ROE')


cnnr=['2330.TW','2317.TW','2474.TW','3008.TW','2454.TW']
usnr=['SLB','COP','HAL','OXY','FCX']
otns=['5713.T','1605.T','5020.T']

esg=compare_snapshot(cnnr+usnr+otns,'Total ESG')
ep=compare_snapshot(cnnr+usnr+otns,'Environment Score')
csr=compare_snapshot(cnnr+usnr+otns,'Social Score')
gov=compare_snapshot(cnnr+usnr+otns,'Governance Score')


ep=compare_snapshot(['9988.HK','9618.HK','0700.HK'],'Environment Score')

#==============================================================================

market={'Market':('China','^HSI')}
stocks={'0700.HK':3,'9618.HK':2,'9988.HK':1}
portfolio=dict(market,**stocks)

_,_,stocklist,_=decompose_portfolio(portfolio)
collist=['symbol','totalEsg','environmentScore','socialScore','governanceScore']
sust=pd.DataFrame(columns=collist)
    for t in stocklist:
        try:
            info=stock_info(t).T
        except:
            print("#Error(): esg info not available for",t)
            continue
        if (info is None) or (len(info)==0):
            print("#Error(): failed to get esg info for",t)
            continue
        sub=info[collist]
        sust=pd.concat([sust,sub])
        












