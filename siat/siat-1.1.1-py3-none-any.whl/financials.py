# -*- coding: utf-8 -*-
"""
本模块功能：计算财务报表比例，应用层
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年9月8日
最新修订日期：2020年9月15日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
#本模块的公共引用
from siat.common import *
from siat.financial_statements import *
from siat.grafix import *
#==============================================================================
if __name__ == '__main__':
    tickers=['AAPL','MSFT']
    items=['Current Ratio','Quick Ratio']
    datatag=False
    power=0
    zeroline=False
    twinx=False

def compare_history(tickers,items, \
                    datatag=False,power=0,zeroline=False,twinx=False):
    """
    功能：比较多个股票的时序数据，绘制折线图
    datatag=False: 不将数值标记在图形旁
    zeroline=False：不绘制水平零线
    twinx=False：单纵轴
    """
    #检查股票个数
    ticker_num=1
    if isinstance(tickers,list): 
        if len(tickers) >= 1: ticker1=tickers[0]
        if len(tickers) >= 2: 
            ticker2=tickers[1]
            ticker_num=2
        if len(tickers) == 0: 
            print("#Error(): no stock code found",tickers)
            return None,None
    else:
        ticker1=tickers

    #检查指标个数
    item_num=1
    if isinstance(items,list): 
        if len(items) >= 1: item1=items[0]
        if len(items) >= 2: 
            item2=items[1]
            item_num=2
        if len(items) == 0: 
            print("#Error(): no analytical item found",items)
            return None,None
    else:
        item1=items
    
    #判断比较模式
    if (ticker_num == 1) and (item_num == 1): mode='T1I1'
    if (ticker_num == 1) and (item_num == 2): mode='T1I2'
    if (ticker_num == 2): mode='T2I1'
    
    #检查指标是否支持
    itemlist=[
        #短期偿债能力
        'Current Ratio','Quick Ratio','Cash Ratio','Cash Flow Ratio', \
        #长期偿债能力
        'Debt to Asset','Equity to Asset','Equity Multiplier','Debt to Equity', \
        'Debt to Tangible Net Asset','Debt Service Coverage','Times Interest Earned', \
        #营运能力
        'Inventory Turnover','Receivable Turnover','Current Asset Turnover', \
        'Fixed Asset Turnover','Total Asset Turnover', \
        #盈利能力
        'Operating Margin','Gross Margin','Profit Margin', \
        'Net Profit on Costs','ROA','ROIC','ROE', \
        #股东持股
        'Payout Ratio','Cashflow per Share','CFPS','Dividend per Share','DPS', \
        'Net Asset per Share','BasicEPS','DilutedEPS', \
        #发展潜力
        'Revenue Growth','Capital Accumulation','Total Asset Growth','PPE Residual' \
        ]
    
    if item1 not in itemlist:
        print("#Error(compare_history): unsupported item for",item1)
        print("*** Supported items are as follows:\n",itemlist)
        return None,None    
    if mode=='T1I2':
        if item2 not in itemlist:
            print("#Error(compare_history): unsupported item for",item2)
            print("*** Supported items are as follows:\n",itemlist)
            return None,None    
    
    #抓取数据
    info1=get_financial_rates(ticker1)
    cols1=['ticker','endDate','periodType',item1]
    df1=info1[cols1]
    
    if mode == 'T1I2':
        ticker2=ticker1
        cols2=['ticker','endDate','periodType',item2]
        df2=info1[cols2]
    
    if mode == 'T2I1':
        item2=item1
        info2=get_financial_rates(ticker2)
        df2=info2[cols1]

    #绘图：T1I1，单折线
    if mode == 'T1I1':
        df=df1
        colname=item1
        collabel=item1
        ylabeltxt=''
        titletxt=ticker1+": 业绩历史"
        import datetime; today=datetime.date.today()
        footnote="数据来源: 雅虎财经, "+str(today)
        
        plot_line(df,colname,collabel,ylabeltxt,titletxt,footnote, \
                  datatag=datatag,power=power,zeroline=zeroline)
        return df1,None

    #绘图：T1I2，单股票双折线
    if mode == 'T1I2':
        colname1=item1
        label1=item1
        colname2=item2
        label2=item2
        ylabeltxt=''
        titletxt=ticker1+": 业绩历史对比"
        import datetime; today=datetime.date.today()
        footnote="数据来源: 雅虎财经, "+str(today)
        
        plot_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=power,zeroline=zeroline,twinx=twinx)
        return df1,df2

    #绘图：T2I1，双股票双折线
    if mode == 'T2I1':
        #日期可能不一致，并表
        import pandas as pd
        df=pd.merge(df1,df2,how="outer",on="endDate")
        #df=df.fillna(method='ffill').fillna(method='bfill')
        df.dropna(inplace=True)
        dfx=df[['ticker_x','endDate','periodType_x',item1+'_x']]
        dfx=dfx.rename(columns={'ticker_x':'ticker','periodType_x':'periodType',item1+'_x':item1})
        dfx['date']=dfx['endDate']
        dfx.set_index('date',inplace=True)
        
        dfy=df[['ticker_y','endDate','periodType_y',item1+'_y']]
        dfy=dfy.rename(columns={'ticker_y':'ticker','periodType_y':'periodType',item1+'_y':item1})
        dfy['date']=dfy['endDate']
        dfy.set_index('date',inplace=True)
        
        colname1=item1
        label1=item1
        colname2=item2
        label2=item2
        ylabeltxt=''
        titletxt=ticker1+"与"+ticker2+": 业绩历史对比"
        import datetime; today=datetime.date.today()
        footnote="数据来源: 雅虎财经, "+str(today)
        
        plot_line2(dfx,ticker1,colname1,label1, \
               dfy,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=power,zeroline=zeroline,twinx=twinx)    
    
        return df1,df2    
    
if __name__ == '__main__':
    df1,df2=compare_history(tickers,items)
    
#==============================================================================
if __name__ == '__main__':
    tickers=['AAPL','MSFT','WMT']
    itemk='Current Ratio'
    itemk='Employees'
    
    tickers=['W','WMT']
    itemk='Debt to Equity'
    datatag=True
    tag_offset=0.01

def compare_snapshot(tickers,itemk,datatag=True,tag_offset=0.01,graph=True):
    """
    功能：比较多个股票的快照数据，绘制水平柱状图
    itemk需要通过对照表转换为内部的item
    datatag=True: 将数值标记在图形旁
    tag_offset=0.01：标记的数值距离图形的距离，若不理想可以手动调节，可为最大值1%-5%
    """
    #检查股票代码列表
    if not isinstance(tickers,list): 
        print("#Error(compare_snapshot): need more stock codes in",tickers)
        return None
    if len(tickers) < 2:
        print("#Error(compare_snapshot): need more stock codes in",tickers)
        return None
    
    #检查指标
    if isinstance(itemk,list): 
        print("#Error(compare_snapshot): only 1 item allowed here",itemk)
        return None    
    
    itemdict={
        #员工与ESG
        'Employees':'fullTimeEmployees', \
        'Total ESG':'totalEsg','Environment Score':'environmentScore', \
        'Social Score':'socialScore','Governance Score':'governanceScore', \
        #偿债能力
        'Current Ratio':'currentRatio','Quick Ratio':'quickRatio', \
        'Debt to Equity':'debtToEquity', \
        #盈利能力
        'EBITDA Margin':'ebitdaMargins','Operating Margin':'operatingMargins', \
        'Gross Margin':'grossMargins','Profit Margin':'profitMargins', \
        'ROA':'returnOnAssets','ROE':'returnOnEquity', \
        #股东持股
        'Held Percent Insiders':'heldPercentInsiders', \
        'Held Percent Institutions':'heldPercentInstitutions', \
        #股东回报
        'Payout Ratio':'payoutRatio','Revenue per Share':'revenuePerShare', \
        'Cashflow per Share':'totalCashPerShare', \
        'Dividend Rate':'dividendRate','TTM Dividend Rate':'trailingAnnualDividendRate', \
        'Dividend Yield':'dividendYield', \
        'TTM Dividend Yield':'trailingAnnualDividendYield', \
        '5-Year Avg Dividend Yield':'fiveYearAvgDividendYield', \
        'Trailing EPS':'trailingEps','Forward EPS':'forwardEps', \
        #发展潜力
        'Revenue Growth':'revenueGrowth','Earnings Growth':'earningsGrowth', \
        'Earnings Quarterly Growth':'earningsQuarterlyGrowth', \
        'EV to Revenue':'enterpriseToRevenue','EV to EBITDA':'enterpriseToEbitda', \
        #市场看法
        'Current Price':'currentPrice','Price to Book':'priceToBook', \
        'TTM Price to Sales':'priceToSalesTrailing12Months', \
        'beta':'beta','52-Week Change':'52WeekChange', \
        'Trailing PE':'trailingPE','Forward PE':'forwardPE', \
        'PEG':'pegRatio'
        }
    itemlist=list(itemdict.keys())
    if itemk not in itemlist:
        print("#Error(compare_snapshot): unsupported rate for",itemk)
        print("*** Supported rates are as follows:\n",itemlist)
        return None

    item=itemdict[itemk]
    import pandas as pd
    import siat.stock_base as sb
    df=pd.DataFrame(columns=('ticker','item','value','name'))
    for t in tickers:
        try:
            info=stock_info(t)
        except:
            print("#Error(compare_snapshot): stock info not available for",t)
            continue
        if (info is None) or (len(info)==0):
            print("#Error(compare_snapshot): failed to get info for",t,"\b, try later!")
            continue
        try:
            value=info[info.index == item]['Value'][0]
        except:
            print("#Error(compare_snapshot): failed to get info of",item,"for",t)
            continue
        """
        name=info[info.index == 'shortName']['Value'][0]
        name1=name.split(' ',1)[0]  #取空格分隔字符串的第一个单词
        name2=name1.split(',',1)[0]
        name3=name2.split('.',1)[0]
        """
        name=sb.codetranslate(t)
        row=pd.Series({'ticker':t,'item':item,'value':value,'name':name})
        df=df.append(row,ignore_index=True)         
    
    if len(df) == 0:
        print("#Error(compare_snapshot): stock info not found in",tickers)
        return None
    
    #处理小数点
    try:
        df['value']=round(df['value'],3)    
    except:
        pass
    df.sort_values(by='value',ascending=False,inplace=True)
    df['key']=df['name']
    df.set_index('key',inplace=True)    
    
    #绘图
    if graph:
        colname='value'
        titletxt="企业横向比较: 业绩快照"
        import datetime; today=datetime.date.today()
        footnote=itemk+" -->"+ \
            "\n数据来源: 雅虎财经, "+str(today)
        plot_barh(df,colname,titletxt,footnote,datatag=datatag,tag_offset=tag_offset)
    
    return df

if __name__ == '__main__':
    df=compare_snapshot(tickers,itemk)
    
#==============================================================================
#==============================================================================
#==============================================================================
if __name__ == '__main__':
    fsdf=get_financial_statements('AAPL')
    fst=fsdf.T  #查看科目名称更加方便

def get_PE(fsdf):
    """
    功能：计算PE
    """
    dateymd=lambda x:x.strftime('%Y-%m-%d') 
    fsdf['endDate']=fsdf['asOfDate'].apply(dateymd)
    
    #获得各个报表的日期范围，适当扩大日期范围以规避非交易日
    start=min(list(fsdf['endDate']))
    fromdate=date_adjust(start,adjust=-30)
    end=max(list(fsdf['endDate']))
    todate=date_adjust(end,adjust=30)

    #获取股价
    ticker=list(fsdf['ticker'])[0]
    import siat.security_prices as ssp
    prices=ssp.get_price(ticker, fromdate, todate)
    if prices is None:
        print("#Error(get_PE): retrieving stock price failed for",ticker,fromdate,todate,"\b, recovering...")
        import time; time.sleep(5)
        prices=ssp.get_price(ticker, fromdate, todate)
        if prices is None: 
            print("#Error(get_PE): failed retrieving stock price, retrying stopped")
            import numpy as np
            fsdf['BasicPE']=np.nan
            fsdf['DilutedPE']=np.nan
            return fsdf
    
    prices['datedt']=prices.index.date
    datecvt=lambda x: str(x)[0:10]
    prices['Date']=prices['datedt'].apply(datecvt)

    #报表日期列表
    datelist_fs=list(fsdf['endDate'])
    #价格日期列表    
    datelist_price=list(prices['Date'])
    date_price_min=min(datelist_price)
    date_price_max=max(datelist_price)
    
    #股价列表
    pricelist=list(prices['Close'])
    
    import pandas as pd
    pricedf=pd.DataFrame(columns=('endDate','actualDate','Price'))
    for d in datelist_fs:
        found=False
        d1=d
        if d in datelist_price:
            found=True
            pos=datelist_price.index(d)
            p=pricelist[pos]
        else:
            while (d1 >= date_price_min) and not found:
                d1=date_adjust(d1,adjust=-1)
                if d1 in datelist_price:
                    found=True
                    pos=datelist_price.index(d1)
                    p=pricelist[pos]
            while (d1 <= date_price_max) and not found:
                d1=date_adjust(d1,adjust=1)
                if d1 in datelist_price:
                    found=True
                    pos=datelist_price.index(d1)
                    p=pricelist[pos]            
        #记录股价
        row=pd.Series({'endDate':d,'actualDate':d1,'Price':p})
        pricedf=pricedf.append(row,ignore_index=True)

    #合成表
    fsdf1=pd.merge(fsdf,pricedf,on='endDate')
    fsdf1['BasicPE']=fsdf1['Price']/fsdf1['BasicEPS']
    fsdf1['DilutedPE']=fsdf1['Price']/fsdf1['DilutedEPS']

    return fsdf1

if __name__ == '__main__':
    fsdf1=get_PE(fsdf)

#==============================================================================
if __name__ == '__main__':
    fsdf=get_financial_statements('AAPL')
    fst=fsdf.T  #查看科目名称更加方便

def calc_DebtToAsset(fsdf):
    """
    功能：计算资产负债率
    """
    
    fsdf1=fsdf.copy()
    
    #计算Debt to Asset
    try:
        fsdf1['Debt to Asset']=round(fsdf1['TotalLiabilities']/fsdf1['TotalAssets'],4)
    except:
        print("#Error(get_DebtToAsset): failed in calculating DebtToAsset")
    
    #计算Debt to Equity
    try:
        fsdf1['Debt to Equity']=round(fsdf1['TotalLiabilities']/fsdf1['TotalEquities'],4)    
    except:
        print("#Error(get_DebtToAsset): failed in calculating DebtToEquity")    
    
    return fsdf1

if __name__ == '__main__':
    fsdf1=get_DebtToAsset(fsdf)


#==============================================================================
if __name__ == '__main__':
    fsdf=get_financial_statements('AAPL')
    fst=fsdf.T  #查看科目名称更加方便

def calc_fin_rates(fsdf):
    """
    功能：基于财报计算各种指标
    """
    #####前后填充缺失值
    fs = fsdf.fillna(method='ffill').fillna(method='bfill')
    
    #短期偿债能力指标
    #流动比率：流动资产 / 流动负债
    fs['Current Ratio']=round(fs['CurrentAssets']/fs['CurrentLiabilities'],2)
    #速动比率：（流动资产-存货） / 流动负债
    fs['Quick Ratio']=round((fs['CurrentAssets']-fs['Inventory'])/fs['CurrentLiabilities'],2)
    #现金比率: （现金+现金等价物） / 流动负债
    fs['Cash Ratio']=round(fs['CashAndCashEquivalents']/fs['CurrentLiabilities'],2)
    #现金流量比率：经营活动现金流量 / 流动负债
    fs['Cash Flow Ratio']=round(fs['OperatingCashFlow']/fs['CurrentLiabilities'],2)
    
    #####长期偿债能力指标
    #资产负债率：负债总额 / 资产总额
    fs['Debt to Asset']=round(fs['TotalLiabilities']/fs['TotalAssets'],2)
    #股东权益比率：股东权益总额 / 资产总额
    fs['Equity to Asset']=round(fs['TotalEquities']/fs['TotalAssets'],2)
    #权益乘数：资产总额 / 股东权益总额
    fs['Equity Multiplier']=round(fs['TotalAssets']/fs['TotalEquities'],2)
    #负债股权比率：负债总额 / 股东权益总额
    fs['Debt to Equity']=round(fs['TotalLiabilities']/fs['TotalEquities'],2)
    #有形净值债务率：负债总额 / （股东权益-无形资产净额）
    fs['netIntangibleAsset']=fs['TotalAssets']-fs['NetTangibleAssets']
    fs['Debt to Tangible Net Asset']=round(fs['TotalLiabilities']/(fs['TotalEquities']-fs['netIntangibleAsset']),2)
    #偿债保障比率：负债总额 / 经营活动现金净流量
    fs['Debt Service Coverage']=round(fs['TotalLiabilities']/fs['OperatingCashFlow'],2)
    #利息保障倍数：（税前利润+利息费用）/ 利息费用
    fs['Times Interest Earned']=round(fs['PretaxIncome']/fs['InterestExpense']+1,2)
    
    #营运能力指标
    #存货周转率：销售成本 / 平均存货
    fs['avgInventory']=(fs['Inventory']+fs['Inventory'].shift(1))/2.0  
    fs['Inventory Turnover']=round(fs['CostOfRevenue']/fs['avgInventory'],2)
    #应收账款周转率：赊销收入净额 / 平均应收账款余额    
    fs['avgReceivables']=(fs['AccountsReceivable']+fs['AccountsReceivable'].shift(1))/2.0  
    fs['Receivable Turnover']=round(fs['OperatingRevenue']/fs['avgReceivables'],2)
    #流动资产周转率：销售收入 / 平均流动资产余额
    fs['avgCurrentAsset']=(fs['CurrentAssets']+fs['CurrentAssets'].shift(1))/2.0  
    fs['Current Asset Turnover']=round(fs['OperatingRevenue']/fs['avgCurrentAsset'],2)
    #固定资产周转率：销售收入 / 平均固定资产净额
    fs['avgPPE']=(fs['NetPPE']+fs['NetPPE'].shift(1))/2.0  
    fs['Fixed Asset Turnover']=round(fs['OperatingRevenue']/fs['avgPPE'],2)
    #总资产周转率：销售收入 / 平均资产总额
    fs['avgTotalAsset']=(fs['TotalAssets']+fs['TotalAssets'].shift(1))/2.0  
    fs['Total Asset Turnover']=round(fs['OperatingRevenue']/fs['avgTotalAsset'],2)
    
    #主营业务利润率=主营业务利润/主营业务收入
    fs['Operating Margin']=round(fs['OperatingIncome']/fs['OperatingRevenue'],4)
    
    #发展潜力指标
    #营业收入增长率：本期营业收入增长额 / 上年同期营业收入总额
    fs['Revenue Growth']=round(fs['OperatingRevenue'].pct_change(),2)
    #资本积累率：本期所有者权益增长额 / 年初所有者权益
    fs['Capital Accumulation']=round(fs['TotalEquities'].pct_change(),2)
    #总资产增长率：本期总资产增长额 / 年初资产总额    
    fs['Total Asset Growth']=round(fs['TotalAssets'].pct_change(),2)
    #固定资产成新率：平均固定资产净值 / 平均固定资产原值。又称“固定资产净值率”或“有用系数”
    fs['avgNetPPE']=(fs['NetPPE']+fs['NetPPE'].shift(1))/2.0
    fs['avgGrossPPE']=(fs['GrossPPE']+fs['GrossPPE'].shift(1))/2.0
    fs['PPE Residual']=round(fs['avgNetPPE']/fs['avgGrossPPE'],2)
    
    #其他指标

    #盈利能力指标
    #资产报酬率（息前税后）：利润总额+利息支出 / 平均资产总额        
    fs['Return on Asset']=round((fs['NetIncome']+fs['InterestExpense'])/fs['avgTotalAsset'],2)
    fs['ROA']=fs['Return on Asset']
    #（投入）资本回报率（Return on Invested Capital，简称ROIC）
    #ROIC=NOPLAT(息前税后经营利润)/IC(投入资本)
    #NOPLAT=EBIT×(1－T)=(营业利润+财务费用－非经常性投资损益) ×(1－所得税率)
    #IC=有息负债+净资产－超额现金－非经营性资产
    fs['Return on Invested Capital']=(fs['OperatingIncome']+fs['InterestExpense'])*(1-fs['TaxRateForCalcs'])/fs['InvestedCapital']
    fs['Return on Invested Capital']=round(fs['Return on Invested Capital'],2)
    fs['ROIC']=fs['Return on Invested Capital']
    #净资产报酬率：净利润 / 平均净资产    
    fs['avgTotalEquity']=(fs['TotalEquities']+fs['TotalEquities'].shift(1))/2.0  
    fs['Return on Net Asset']=round(fs['NetIncome']/fs['avgTotalEquity'],2)
    #股东权益报酬率：净利润 / 平均股东权益总额
    fs['Return on Equity']=fs['Return on Net Asset']
    fs['ROE']=fs['Return on Equity']
    #毛利率：销售毛利 / 销售收入净额    
    fs['Gross Margin']=round(fs['GrossProfit']/fs['TotalRevenue'],2)
    #销售净利率：净利润 / 销售收入净额
    fs['Profit Margin']=round(fs['NetIncome']/fs['TotalRevenue'],2)
    #成本费用净利率：净利润 / 成本费用总额
    fs['Net Profit on Costs']=round(fs['NetIncome']/fs['CostOfRevenue'],2)
    #股利发放率：每股股利 / 每股利润   
    fs['Payout Ratio']=round(fs['CashDividendsPaid']/fs['NetIncome'],2)

    ###每股指标，受EPS可用性影响    
    #每股利润：（净利润-优先股股利） / 加权流通在外股数。基本EPS
    #注意：流通股股数=期初commonStock-treasuryStock,加本年增加的股数issuanceOfStock*月份占比-本年减少的股数repurchaseOfStock*月份占比
    import numpy as np
    fs['outstandingStock']=np.floor(fs['NetIncomeCommonStockholders']/fs['BasicEPS'])
    #每股现金流量：（经营活动现金净流量-优先股股利） / 流通在外股数
    fs['Cashflow per Share']=round(fs['OperatingCashFlow']/fs['outstandingStock'],2)
    fs['CFPS']=fs['Cashflow per Share']
    #每股股利：（现金股利总额-优先股股利） /流通在外股数    
    fs['Dividend per Share']=round(fs['CashDividendsPaid']/fs['outstandingStock'],2)
    fs['DPS']=fs['Dividend per Share']
    #每股净资产：股东权益总额 / 流通在外股数  
    fs['Net Asset per Share']=round(fs['CommonStockEquity']/fs['outstandingStock'],2)
    
    #市盈率：每股市价 / 每股利润，依赖EPS反推出的流通股数量
    #fs=get_PE(fs)
    dateymd=lambda x:x.strftime('%Y-%m-%d') 
    fs['endDate']=fs['asOfDate'].apply(dateymd)
    
    fs['date']=fs['endDate']
    fs.set_index('date',inplace=True)    
    
    return fs
    
    
if __name__ == '__main__':
    fs=calc_fin_rates(fsdf)

#==============================================================================
if __name__ == '__main__':
    ticker='AAPL'

def get_financial_rates(ticker):
    """
    功能：获得股票的财务报表和财务比率
    财务报表：资产负债表，利润表，现金流量表
    财务比率：短期还债能力，长期还债能力，营运能力，盈利能力，发展能力
    返回：报表+比率    
    """
    print("\nAnalyzing financial rates of",ticker,"\b, it may take time......")
    
    #抓取股票的财务报表
    try:
        fsdf=get_financial_statements(ticker)
    except:
        print("......Failed to get financial statements of",ticker,"\b, recovering")
        import time; time.sleep(5)
        try:
            fsdf=get_financial_statements(ticker)
        except:
            print("......Failed to get financial statements of",ticker,"\b!")
            print("......If the stock code",ticker,"\b is correct, please try a few minutes later.")
        return None
        
    #抓取股票的稀释后EPS，计算财务比率
    fsr=calc_fin_rates(fsdf)
    """
    try:
        fsr=calc_fin_rates(fsdf)
    except:
        print("......Failed to calculate some financial rates of",ticker,"\b!")
        return None
    """
    #整理列名：将股票代码、截止日期、报表类型排在开头
    cols=list(fsr)
    cols.remove('endDate')
    cols.remove('ticker')
    cols.remove('periodType')
    fsr2=fsr[['ticker','endDate','periodType']+cols]
    
    return fsr2

"""
短期偿债能力分析：
1、流动比率，计算公式： 流动资产 / 流动负债
2、速动比率，计算公式： （流动资产-存货） / 流动负债
3、现金比率，计算公式： （现金+现金等价物） / 流动负债
4、现金流量比率，计算公式： 经营活动现金流量 / 流动负债

长期偿债能力分析：
1、资产负债率，计算公式： 负债总额 / 资产总额
2、股东权益比率，计算公式： 股东权益总额 / 资产总额
3、权益乘数，计算公式： 资产总额 / 股东权益总额
4、负债股权比率，计算公式： 负债总额 / 股东权益总额
5、有形净值债务率，计算公式： 负债总额 / （股东权益-无形资产净额）
6、偿债保障比率，计算公式： 负债总额 / 经营活动现金净流量
7、利息保障倍数，计算公式： （税前利润+利息费用）/ 利息费用

营运分析
1、存货周转率，计算公式： 销售成本 / 平均存货
2、应收账款周转率，计算公式： 赊销收入净额 / 平均应收账款余额
3、流动资产周转率，计算公式： 销售收入 / 平均流动资产余额
4、固定资产周转率，计算公式： 销售收入 / 平均固定资产净额
5、总资产周转率，计算公式： 销售收入 / 平均资产总额

盈利分析
1、资产报酬率，计算公式： 利润总额+利息支出 / 平均资产总额
2、净资产报酬率，计算公式： 净利润 / 平均净资产
3、股东权益报酬率，计算公式： 净利润 / 平均股东权益总额
4、毛利率，计算公式： 销售毛利 / 销售收入净额
5、销售净利率，计算公式： 净利润 / 销售收入净额
6、成本费用净利率，计算公式： 净利润 / 成本费用总额
7、每股利润，计算公式： （净利润-优先股股利） / 流通在外股数
8、每股现金流量，计算公式： （经营活动现金净流量-优先股股利） / 流通在外股数
9、每股股利，计算公式： （现金股利总额-优先股股利） /流通在外股数
10、股利发放率，计算公式： 每股股利 / 每股利润
11、每股净资产，计算公式： 股东权益总额 / 流通在外股数
12、市盈率，计算公式： 每股市价 / 每股利润
13、主营业务利润率=主营业务利润/主营业务收入*100%

发展分析
1、营业增长率，计算公式： 本期营业增长额 / 上年同期营业收入总额
2、资本积累率，计算公式： 本期所有者权益增长额 / 年初所有者权益
3、总资产增长率，计算公式： 本期总资产增长额 / 年初资产总额
4、固定资产成新率，计算公式： 平均固定资产净值 / 平均固定资产原值
"""
#==============================================================================
#==============================================================================
#==============================================================================
#####以上的指标为时间序列；以下的指标为非时间序列，类似于快照信息
#==============================================================================
if __name__=='__main__':
    symbol='AAPL'
    symbol='BABA'

def stock_info(symbol):
    """
    功能：返回静态信息
    """
    DEBUG=False
    print("...Searching for information of",symbol,"\b, please wait...")
    
    from yahooquery import Ticker
    stock = Ticker(symbol)

    """
    Asset Profile:
    Head office address/zip/country, Officers, Employees, industry/sector, phone/fax,
    web site,
    Risk ranks: auditRisk, boardRisk, compensationRisk, overallRisk, shareHolderRightRisk,
    compensationRisk: 薪酬风险。Jensen 及 Meckling (1976)的研究指出薪酬與管理者的風險承擔
    具有關連性，站在管理者的立場來看，創新支出的投入使管理者承受更大的薪酬風險(compensation risk)，
    管理者自然地要求更高的薪酬來補貼所面臨的風險，因此企業創新投資對管理者薪酬成正相關。
    boardRisk: 董事会风险
    shareHolderRightRisk：股权风险
    """
    adict=stock.asset_profile
    keylist=list(adict[symbol].keys())
    import pandas as pd    
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=ainfo.copy()


    """
    ESG Scores: Risk measurements
    peerGroup, ratingYear, 
    environmentScore, governanceScore, socialScore, totalEsg
    dict: peerEnvironmentPerformance, peerGovernancePerformance, peerSocialPerformance, 
    peerEsgScorePerformance
    """
    adict=stock.esg_scores
    try:    #一些企业无此信息
        keylist=list(adict[symbol].keys())
        aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
        ainfo=aframe.T
        info=pd.concat([info,ainfo])
    except:
        pass

    """
    Financial Data: TTM???
    currentPrice, targetHighPrice, targetLowPrice, targetMeanPrice, targetMedianPrice, 
    currentRatio, debtToEquity, earningsGrowth, ebitda, ebitdaMargins, financialCurrency,
    freeCashflow, grossMargins, grossProfits, 
    operatingCashflow, operatingMargins, profitMargins,
    quickRatio, returnOnAssets, returnOnEquity, revenueGrowth, revenuePerShare, 
    totalCash, totalCashPerShare, totalDebt, totalRevenue, 
    """
    adict=stock.financial_data
    keylist=list(adict[symbol].keys())
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=pd.concat([info,ainfo])    
    

    """
    Key Statistics: TTM???
    52WeekChang, SandP52WeekChang, beta, floatShares, sharesOutstanding, 
    bookValue, earningsQuarterlyGrowth, enterpriseToEbitda, enterpriseToRevenue,
    enterpriseValue, netIncomeToCommon, priceToBook, profitMargins, 
    forwardEps, trailingEps,
    heldPercentInsiders, heldPercentInstitutions, 
    lastFiscalYearEnd, lastSplitDate, lastSplitFactor, mostRecentQuarter, nextFiscalYearEnd,
    """
    adict=stock.key_stats
    keylist=list(adict[symbol].keys())
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=pd.concat([info,ainfo]) 
    
    
    """
    Price Information:
    currency, currencySymbol, exchange, exchangeName, shortName, 
    longName, 
    marketCap, marketState, quoteType, 
    regularMarketChange, regularMarketChangPercent, regularMarketHigh, regularMarketLow, 
    regularMarketOpen, regularMarketPreviousClose, regularMarketPrice, regularMarketTime,
    regularMarketVolume, 
    """
    adict=stock.price
    keylist=list(adict[symbol].keys())
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=pd.concat([info,ainfo]) 
    

    """
    Quote Type:
    exchange, firstTradeDateEpocUtc(上市日期), longName, quoteType(证券类型：股票), 
    shortName, symbol(当前代码), timeZoneFullName, timeZoneShortName, underlyingSymbol(原始代码), 
    """
    adict=stock.quote_type
    keylist=list(adict[symbol].keys())
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=pd.concat([info,ainfo]) 
    

    """
    Share Purchase Activity
    period(6m), totalInsiderShares
    """
    adict=stock.share_purchase_activity
    keylist=list(adict[symbol].keys())
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=pd.concat([info,ainfo]) 


    """
    # Summary detail
    averageDailyVolume10Day, averageVolume, averageVolume10days, beta, currency, 
    dayHigh, dayLow, fiftyDayAverage, fiftyTwoWeekHigh, fiftyTwoWeekLow, open, previousClose, 
    regularMarketDayHigh, regularMarketDayLow, regularMarketOpen, regularMarketPreviousClose, 
    regularMarketVolume, twoHundredDayAverage, volume, 
    forwardPE, marketCap, priceToSalesTrailing12Months, 
    dividendRate, dividendYield, exDividendDate, payoutRatio, trailingAnnualDividendRate,
    trailingAnnualDividendYield, trailingPE, 
    """
    adict=stock.summary_detail
    keylist=list(adict[symbol].keys())
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=pd.concat([info,ainfo]) 

    
    """
    summary_profile
    address/city/country/zip, phone/fax, sector/industry, website/longBusinessSummary, 
    fullTimeEmployees, 
    """
    adict=stock.summary_profile
    keylist=list(adict[symbol].keys())
    aframe=pd.DataFrame.from_dict(adict, orient='index', columns=keylist)
    ainfo=aframe.T
    info=pd.concat([info,ainfo]) 
    

    # 清洗数据项目
    info.sort_index(inplace=True)   #排序
    info.dropna(inplace=True)   #去掉空值
    #去重
    info['Item']=info.index
    info.drop_duplicates(subset=['Item'],keep='last',inplace=True)
    
    #删除不需要的项目
    delrows=['adult','alcoholic','animalTesting','ask','askSize','bid','bidSize', \
             'catholic','coal','controversialWeapons','furLeather','gambling', \
                 'gmo','gmtOffSetMilliseconds','militaryContract','messageBoardId', \
                     'nuclear','palmOil','pesticides','tobacco','uuid','maxAge']
    for r in delrows:
       info.drop(info[info['Item']==r].index,inplace=True) 
    
    #修改列名
    info.rename(columns={symbol:'Value'}, inplace=True) 
    del info['Item']
    
    return info


if __name__=='__main__':
    info=stock_info('AAPL')
    info=stock_info('BABA')

#==============================================================================
if __name__=='__main__':
    info=stock_info('AAPL')

def stock_basic(info):
    
    wishlist=['symbol','shortName','sector','industry', \
              
              #公司名称，业务
              'underlyingSymbol','longName', \
              
              #公司地址，网站
              'address1','address2','city','state','country','zip','phone','fax', \
              'timeZoneShortName','timeZoneFullName','website', \
              
              #员工人数
              'fullTimeEmployees', \
              
              #上市与交易所
              'exchange','exchangeName','quoteType', \
              
              #其他
              'beta','currency','currentPrice','marketCap','trailingPE', \
                  
              'ratingYear','ratingMonth']
        
    #按照wishlist的顺序从info中取值
    rowlist=list(info.index)
    import pandas as pd
    info_sub=pd.DataFrame(columns=['Item','Value'])
    infot=info.T
    for w in wishlist:
        if w in rowlist:
            v=infot[w][0]
            s=pd.Series({'Item':w,'Value':v})
            info_sub=info_sub.append(s,ignore_index=True) 
    
    return info_sub

if __name__=='__main__':
    basic=stock_basic(info)    

#==============================================================================
if __name__=='__main__':
    info=stock_info('AAPL')

def stock_officers(info):
    
    wishlist=['symbol','shortName','sector','industry', \
              
              #公司高管
              'currency','companyOfficers', \
              
              ]
        
    #按照wishlist的顺序从info中取值
    rowlist=list(info.index)
    import pandas as pd
    info_sub=pd.DataFrame(columns=['Item','Value'])
    infot=info.T
    for w in wishlist:
        if w in rowlist:
            v=infot[w][0]
            s=pd.Series({'Item':w,'Value':v})
            info_sub=info_sub.append(s,ignore_index=True) 
    
    return info_sub

if __name__=='__main__':
    sub_info=stock_officers(info)    

#==============================================================================
def stock_risk_general(info):
    
    wishlist=['symbol','shortName','sector','industry', \
              
              'overallRisk','boardRisk','compensationRisk', \
              'shareHolderRightsRisk','auditRisk', \
                  
              'ratingYear','ratingMonth']
        
    #按照wishlist的顺序从info中取值
    rowlist=list(info.index)
    import pandas as pd
    info_sub=pd.DataFrame(columns=['Item','Value'])
    infot=info.T
    for w in wishlist:
        if w in rowlist:
            v=infot[w][0]
            s=pd.Series({'Item':w,'Value':v})
            info_sub=info_sub.append(s,ignore_index=True) 
    
    return info_sub

if __name__=='__main__':
    risk_general=stock_risk_general(info)    

#==============================================================================
def stock_risk_esg(info):
    
    wishlist=['symbol','shortName','sector','industry', \
            
              'totalEsg','esgPerformance','peerEsgScorePerformance', \
              'environmentScore','peerEnvironmentPerformance', \
              'socialScore','peerSocialPerformance', \
              'governanceScore','peerGovernancePerformance', \
              'peerGroup','relatedControversy','peerCount','percentile', \
                
              'ratingYear','ratingMonth']
        
    #按照wishlist的顺序从info中取值
    rowlist=list(info.index)
    import pandas as pd
    info_sub=pd.DataFrame(columns=['Item','Value'])
    infot=info.T
    for w in wishlist:
        if w in rowlist:
            v=infot[w][0]
            s=pd.Series({'Item':w,'Value':v})
            info_sub=info_sub.append(s,ignore_index=True) 
    
    return info_sub

if __name__=='__main__':
    risk_esg=stock_risk_esg(info)  
    
#==============================================================================
def stock_fin_rates(info):
    
    wishlist=['symbol','shortName','sector','industry', \
              
              'financialCurrency', \
              
              #偿债能力
              'currentRatio','quickRatio','debtToEquity', \
                  
              #盈利能力
              'ebitdaMargins','operatingMargins','grossMargins','profitMargins', \
                  
              #股东回报率
              'returnOnAssets','returnOnEquity', \
              'dividendRate','trailingAnnualDividendRate','trailingEps', \
              'payoutRatio','revenuePerShare','totalCashPerShare', \
              
              #业务发展能力
              'revenueGrowth','earningsGrowth','earningsQuarterlyGrowth', \
              'enterpriseToRevenue','enterpriseToEbitda', \
                
              'ratingYear','ratingMonth']
        
    #按照wishlist的顺序从info中取值
    rowlist=list(info.index)
    import pandas as pd
    info_sub=pd.DataFrame(columns=['Item','Value'])
    infot=info.T
    for w in wishlist:
        if w in rowlist:
            v=infot[w][0]
            s=pd.Series({'Item':w,'Value':v})
            info_sub=info_sub.append(s,ignore_index=True) 
    
    return info_sub

if __name__=='__main__':
    fin_rates=stock_fin_rates(info) 

#==============================================================================
def stock_fin_statements(info):
    
    wishlist=['symbol','shortName','sector','industry', \
              
              'financialCurrency','lastFiscalYearEnd','mostRecentQuarter','nextFiscalYearEnd', \
              
              #资产负债
              'enterpriseValue','totalDebt','marketCap', \
                  
              #利润表
              'totalRevenue','grossProfits','ebitda','netIncomeToCommon', \
                  
              #现金流量
              'operatingCashflow','freeCashflow','totalCash', \
              
              #股票数量
              'sharesOutstanding','floatShares','totalInsiderShares', \
                
              'ratingYear','ratingMonth']
        
    #按照wishlist的顺序从info中取值
    rowlist=list(info.index)
    import pandas as pd
    info_sub=pd.DataFrame(columns=['Item','Value'])
    infot=info.T
    for w in wishlist:
        if w in rowlist:
            v=infot[w][0]
            s=pd.Series({'Item':w,'Value':v})
            info_sub=info_sub.append(s,ignore_index=True) 
    
    return info_sub

if __name__=='__main__':
    fin_statements=stock_fin_statements(info) 

#==============================================================================
def stock_market_rates(info):
    
    wishlist=['symbol','shortName','sector','industry', \
              
              'currency','currencySymbol', \
              
              #市场观察
              'priceToBook','priceToSalesTrailing12Months','recommendationKey', \
              
              #市场风险与收益
              'beta','52WeekChange','SandP52WeekChange', \
              'trailingEps','forwardEps','trailingPE','forwardPE','pegRatio', \
              
              #分红
              'dividendYield','fiveYearAvgDividendYield','trailingAnnualDividendYield', \
                  
              #持股
              'heldPercentInsiders','heldPercentInstitutions', \
              
              #股票流通
              'sharesOutstanding','totalInsiderShares','floatShares', \
              'sharesPercentSharesOut','shortPercentOfFloat','shortRatio', \
                
              'ratingYear','ratingMonth']
        
    #按照wishlist的顺序从info中取值
    rowlist=list(info.index)
    import pandas as pd
    info_sub=pd.DataFrame(columns=['Item','Value'])
    infot=info.T
    for w in wishlist:
        if w in rowlist:
            v=infot[w][0]
            s=pd.Series({'Item':w,'Value':v})
            info_sub=info_sub.append(s,ignore_index=True) 
    
    return info_sub

if __name__=='__main__':
    market_rates=stock_market_rates(info) 

#==============================================================================
if __name__=='__main__':
    ticker='AAPL'
    info_type='fin_rates' 

def get_stock_profile(ticker,info_type='basic'):
    """
    功能：抓取和获得股票的信息
    basic: 基本信息
    fin_rates: 财务比率快照
    fin_statements: 财务报表快照
    market_rates: 市场比率快照
    risk_general: 一般风险快照
    risk_esg: 可持续发展风险快照（有些股票无此信息）
    """
    #print("\nSearching for snapshot info of",ticker,"\b, please wait...")

    typelist=['basic','officers','fin_rates','fin_statements','market_rates','risk_general','risk_esg','all']    
    if info_type not in typelist:
        print("#Sorry, info_type not supported for",info_type)
        print("Supported info_type:\n",typelist)
        return None

    info=stock_info(ticker)
    name=info.T['shortName'][0]
    
    if info_type in ['basic','all']:
        sub_info=stock_basic(info)
        titletxt="***** "+name+": Basic Information *****"        
        printdf(sub_info,titletxt)
    
    if info_type in ['officers','all']:
        sub_info=stock_officers(info)
        titletxt="***** "+name+": Company Senior Management *****"        
        printdf(sub_info,titletxt)    
    
    if info_type in ['fin_rates','all']:
        sub_info=stock_fin_rates(info)
        titletxt="***** "+name+": Fundamental Rates *****"        
        printdf(sub_info,titletxt)
    
    if info_type in ['fin_statements','all']:
        sub_info=stock_fin_statements(info)
        titletxt="***** "+name+": Financial Statements *****"        
        printdf(sub_info,titletxt)
    
    if info_type in ['market_rates','all']:
        sub_info=stock_market_rates(info)
        titletxt="***** "+name+": Market Rates *****"        
        printdf(sub_info,titletxt)
    
    if info_type in ['risk_general','all']:
        sub_info=stock_risk_general(info)
        titletxt="***** "+name+": Risk General *****"+ \
            "\n(Bigger number means higher risk)"
        printdf(sub_info,titletxt)
    
    if info_type in ['risk_esg','all']:
        sub_info=stock_risk_esg(info)
        if len(sub_info)==0:
            print("#Error(get_stock_profile): esg info not available for",ticker)
        else:
            titletxt="***** "+name+": Sustainability Risk *****"+ \
                "\n(Smaller number means less risky)"
            printdf(sub_info,titletxt)
    
    return info

if __name__=='__main__':
    info=get_stock_profile(ticker,info_type='basic')
    info=get_stock_profile(ticker,info_type='officers')
    info=get_stock_profile(ticker,info_type='fin_rates')
    info=get_stock_profile(ticker,info_type='fin_statements')
    info=get_stock_profile(ticker,info_type='market_rates')
    info=get_stock_profile(ticker,info_type='risk_general')
    info=get_stock_profile(ticker,info_type='risk_esg')

#==============================================================================
if __name__=='__main__':
    ticker='AAPL'
    info=stock_info(ticker)
    sub_info=stock_officers(info)
    titletxt="***** "+ticker+": Snr Management *****"

def printdf(sub_info,titletxt):
    """
    功能：整齐显示股票信息快照
    """
    print("\n"+titletxt)
    
    maxlen=0
    for index,row in sub_info.iterrows():
        if len(row['Item']) > maxlen: maxlen=len(row['Item'])

    for index,row in sub_info.iterrows():
        
        #特殊打印：高管信息
        if row['Item']=="companyOfficers":
            print_companyOfficers(sub_info)
            continue
        
        #特殊打印：ESG同行状况
        peerlist=["peerEsgScorePerformance","peerEnvironmentPerformance", \
                 "peerSocialPerformance","peerGovernancePerformance"]
        if row['Item'] in peerlist:
            print_peerPerformance(sub_info,row['Item'])
            continue

        #特殊打印：ESG Social风险内容
        if row['Item']=="relatedControversy":
            print_controversy(sub_info,row['Item'])
            continue

        thislen=maxlen-len(row['Item'])
        print(row['Item'],'.'*thislen,'\b:',row['Value'])
    
    import datetime
    today=datetime.date.today()
    print("*** Source: Yahoo Finance,",today)
    
    return

if __name__=='__main__':
    printdf(sub_info,titletxt)

#==============================================================================
if __name__=='__main__':
    info=stock_info('AAPL')
    sub_info=stock_officers(info)

def print_companyOfficers(sub_info):
    """
    功能：打印公司高管信息
    """
    item='companyOfficers'
    itemtxt='Company officers:'
    key1='name'
    key2='title'
    key3='yearBorn'
    key4='age'
    key6='totalPay'
    key7='fiscalYear'
    currency=list(sub_info[sub_info['Item'] == 'currency']['Value'])[0]
    alist=list(sub_info[sub_info['Item'] == item]['Value'])[0]
    
    print(itemtxt)
    for i in alist:
        print(' '*4,i[key1])
        print(' '*8,i[key2],'\b,',i[key4],'years old (born',i[key3],'\b)')
        print(' '*8,'Total paid',currency+str(format(i[key6],',')),'@'+str(i[key7]))
        
    return

if __name__=='__main__':
    print_companyOfficers(sub_info)

#==============================================================================
if __name__=='__main__':
    info=stock_info('AAPL')
    sub_info=stock_risk_esg(info)
    item="peerEsgScorePerformance"

def print_peerPerformance(sub_info,item):
    """
    功能：打印ESG信息
    """
    maxlen=0
    for index,row in sub_info.iterrows():
        if len(row['Item']) > maxlen: maxlen=len(row['Item'])
    thislen=maxlen-len(item)+2
    itemtxt=item+'.'*thislen+'\b:'
    
    key1='min'
    key2='avg'
    key3='max'
    i=list(sub_info[sub_info['Item'] == item]['Value'])[0]
    
    print(itemtxt)
    print(' '*4,key1+':',i[key1],'\b,',key2+':',round(i[key2],2),'\b,',key3+':',i[key3])
        
    return

if __name__=='__main__':
    print_peerPerformance(sub_info,item)

#==============================================================================
if __name__=='__main__':
    info=stock_info('AAPL')
    sub_info=stock_risk_esg(info)
    item='relatedControversy'

def print_controversy(sub_info,item):
    """
    功能：打印ESG Social风险内容
    """
    maxlen=0
    for index,row in sub_info.iterrows():
        if len(row['Item']) > maxlen: maxlen=len(row['Item'])
    thislen=maxlen-len(item)+2
    itemtxt=item+'.'*thislen+'\b:'
    
    alist=list(sub_info[sub_info['Item'] == item]['Value'])[0]
    
    print(itemtxt)
    for i in alist:
        print(' '*4,i)
        
    return

if __name__=='__main__':
    print_controversy(sub_info,item)

#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
