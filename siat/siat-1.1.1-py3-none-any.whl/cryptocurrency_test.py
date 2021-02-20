# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os; os.chdir("S:/siat")
from siat.cryptocurrency import *



fsym = "ETH"; tsym = "USD"
begdate="2020-1-1"; enddate="2020-12-31"
markets=fetchCrypto_Exchange(fsym,tsym)
cp=fetchCrypto_Price_byExchList(fsym,tsym,markets,begdate,enddate)

dist1,dist2=calcSpread_in2Markets(cp)
printSpread_in2Markets(dist1,dist2)


investment = 10000
account1, account2 = investment/2, investment/2
position = 0.5*(investment/2) 

#价差最高的市场：primexbt  Coinbase
market1 = "primexbt"
market2 = "Coinbase"
df1,df2=evalSpread_in2Markets(fsym,tsym,market1,market2,begdate,enddate)
ac1,ac2,money,roi0=backtestMSA_Strategy(investment,account1,account2,position,df1,df2)
eval_Position(market1,market2,investment,ac1,ac2,money)
eval_Roi(fsym,tsym,market1,market2,roi0) 

#价差性价比最高的市场：Bitstamp  primexbt
market1 = "Bitstamp"
market2 = "primexbt"
df1,df2=evalSpread_in2Markets(fsym,tsym,market1,market2,begdate,enddate)
ac1,ac2,money,roi0=backtestMSA_Strategy(investment,account1,account2,position,df1,df2)
eval_Position(market1,market2,investment,ac1,ac2,money)
eval_Roi(fsym,tsym,market1,market2,roi0) 

#价差性风险最低的市场：Bitstamp    Kraken
market1 = "Bitstamp"
market2 = "Kraken"
df1,df2=evalSpread_in2Markets(fsym,tsym,market1,market2,begdate,enddate)
ac1,ac2,money,roi0=backtestMSA_Strategy(investment,account1,account2,position,df1,df2)
eval_Position(market1,market2,investment,ac1,ac2,money)
eval_Roi(fsym,tsym,market1,market2,roi0) 