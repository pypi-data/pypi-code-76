# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os; os.chdir("S:/siat")
from siat.bond import *

#==============================================================================
ibbi=interbank_bond_issue_detail('2012-1-1', '2020-12-31')
ibbim=interbank_bond_issue_monthly(ibbi,'2019-1-1', '2020-12-31')


#==============================================================================
if __name__=='__main__':
    search_bond_index_china(keystr='国债') 
    
    bond_index_china('中债-综合指数','2020-1-1','2021-2-8')
    bond_index_china('中债-国债总指数','2020-1-1','2021-2-8')
    bond_index_china('中债-交易所国债指数','2020-1-1','2021-2-8')    
    bond_index_china('中债-银行间国债指数','2010-1-1','2021-2-8')
    bond_index_china('中债-银行间债券总指数','2020-1-1','2021-2-8')
    
    bond_index_china('中债-5年期国债指数','2020-1-1','2021-2-8')
    bond_index_china('中债-0-3个月国债指数','2020-1-1','2021-2-8')




#==============================================================================
import os; os.chdir("S:/siat")
from siat.stock import *

compare_security(["FRI","^GSPC"],"Exp Adj Ret%","2010-1-1","2020-6-30")

compare_security(["FRI","^GSPC"],"Exp Adj Ret Volatility%","2010-1-1","2020-6-30")

compare_security(["ICF","^DJI"],"Exp Adj Ret%","2010-1-1","2020-6-30")

compare_security(["ICF","^DJI"],"Exp Adj Ret Volatility%","2010-1-1","2020-6-30")



info=stock_price("510050.SS","2020-4-1","2020-6-30")
info=stock_price("510210.SS","2020-4-1","2020-6-30")

compare_security(["510210.SS","000001.SS"],"Close","2020-4-1","2020-6-30",twinx=True)

compare_security(["510210.SS","000001.SS"],"Close","2015-7-1","2020-6-30",twinx=True)

compare_security(["SPY","^GSPC"],"Exp Ret%","2010-1-1","2020-6-30")

compare_security(["VOO","^GSPC"],"Exp Ret%","2010-1-1","2020-6-30")

compare_security(["IVV","^GSPC"],"Exp Ret%","2010-1-1","2020-6-30")

compare_security(["SPY","^GSPC"],"Exp Ret Volatility%","2010-1-1","2020-6-30")

compare_security(["VOO","^GSPC"],"Exp Ret Volatility%","2010-1-1","2020-6-30")

compare_security(["IVV","^GSPC"],"Exp Ret Volatility%","2010-1-1","2020-6-30")

compare_security(["SPY","SPYD"],"Exp Ret%","2019-1-1","2020-6-30")

compare_security(["SPY","SPYG"],"Exp Ret%","2019-1-1","2020-6-30")

compare_security(["SPY","SPYV"],"Exp Ret%","2019-1-1","2020-6-30")


compare_security(["SPY","SPYD"],"Exp Ret Volatility%","2019-1-1","2020-6-30")

compare_security(["SPY","SPYG"],"Exp Ret Volatility%","2019-1-1","2020-6-30")

compare_security(["SPY","SPYV"],"Exp Ret Volatility%","2019-1-1","2020-6-30")



fsym = "ETH"; tsym = "USD"
begdate="2020-03-01"; enddate="2020-05-31"
markets=fetchCrypto_Exchange(fsym,tsym)
cp=fetchCrypto_Price_byExchList(fsym,tsym,markets,begdate,enddate)
dist1,dist2=calcSpread_in2Markets(cp)
print("Average inter-market spread:", dist1)
print("Inter-market spread volatility:", dist2)
