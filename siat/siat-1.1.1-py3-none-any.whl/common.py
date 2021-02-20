# -*- coding: utf-8 -*-
"""
本模块功能：SIAT公共基础函数
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2019年7月16日
最新修订日期：2020年3月28日
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
def ectranslate(eword):
    """
    翻译英文专业词汇至中文，便于显示或绘图时输出中文而不是英文。
    输入：英文专业词汇。输出：中文专业词汇
    """
    import pandas as pd
    ecdict=pd.DataFrame([
        ['High','最高价'],['Low','最低价'],['Open','开盘价'],['Close','收盘价'],
        ['Volume','成交量'],['Adj Close','调整收盘价'],['Daily Ret','日收益率'],
        ['Daily Ret%','日收益率%'],['Daily Adj Ret','调整日收益率'],
        ['Daily Adj Ret%','调整日收益率%'],['log(Daily Ret)','对数日收益率'],
        ['log(Daily Adj Ret)','对数调整日收益率'],['Weekly Ret','周收益率'],
        ['Weekly Ret%','周收益率%'],['Weekly Adj Ret','周调整收益率'],
        ['Weekly Adj Ret%','周调整收益率%'],['Monthly Ret','月收益率'],
        ['Monthly Ret%','月收益率%'],['Monthly Adj Ret','月调整收益率'],
        ['Monthly Adj Ret%','月调整收益率%'],['Quarterly Ret','季度收益率'],
        ['Quarterly Ret%','季度收益率%'],['Quarterly Adj Ret','季度调整收益率'],
        ['Quarterly Adj Ret%','季度调整收益率%'],['Annual Ret','年收益率'],
        ['Annual Ret%','年收益率%'],['Annual Adj Ret','年调整收益率'],
        ['Annual Adj Ret%','年调整收益率%'],['Exp Ret','持有收益率'],
        ['Exp Ret%','持有收益率%'],['Exp Adj Ret','持有调整收益率'],
        ['Exp Adj Ret%','持有调整收益率%'],
        
        ['Weekly Price Volatility','周股价波动风险'],
        ['Weekly Adj Price Volatility','周调整股价波动风险'],
        ['Monthly Price Volatility','月股价波动风险'],
        ['Monthly Adj Price Volatility','月调整股价波动风险'],
        ['Quarterly Price Volatility','季股价波动风险'],
        ['Quarterly Adj Price Volatility','季调整股价波动风险'],
        ['Annual Price Volatility','年股价波动风险'],
        ['Annual Adj Price Volatility','年调整股价波动风险'],  
        ['Exp Price Volatility','持有股价波动风险'], 
        ['Exp Adj Price Volatility','持有调整股价波动风险'],
        
        ['Weekly Ret Volatility','周收益率波动风险'],
        ['Weekly Ret Volatility%','周收益率波动风险%'],
        ['Weekly Adj Ret Volatility','周调整收益率波动风险'],
        ['Weekly Adj Ret Volatility%','周调整收益率波动风险%'],
        ['Monthly Ret Volatility','月收益率波动风险'],
        ['Monthly Ret Volatility%','月收益率波动风险%'],
        ['Monthly Adj Ret Volatility','月调整收益波动风险'],
        ['Monthly Adj Ret Volatility%','月调整收益波动风险%'],
        ['Quarterly Ret Volatility','季收益率波动风险'],
        ['Quarterly Ret Volatility%','季收益率波动风险%'],
        ['Quarterly Adj Ret Volatility','季调整收益率波动风险'],
        ['Quarterly Adj Ret Volatility%','季调整收益率波动风险%'],
        ['Annual Ret Volatility','年收益率波动风险'],
        ['Annual Ret Volatility%','年收益率波动风险%'],
        ['Annual Adj Ret Volatility','年调整收益率波动风险'], 
        ['Annual Adj Ret Volatility%','年调整收益率波动风险%'], 
        ['Exp Ret Volatility','持有收益率波动风险'], 
        ['Exp Ret Volatility%','持有收益率波动风险%'],
        ['Exp Adj Ret Volatility','持有调整收益率波动风险'],        
        ['Exp Adj Ret Volatility%','持有调整收益率波动风险%'],
        
        ['Weekly Ret LPSD','周收益率波动损失风险'],
        ['Weekly Ret LPSD%','周收益率波动损失风险%'],
        ['Weekly Adj Ret LPSD','周调整收益率波动损失风险'],
        ['Weekly Adj Ret LPSD%','周调整收益率波动损失风险%'],
        ['Monthly Ret LPSD','月收益率波动损失风险'],
        ['Monthly Ret LPSD%','月收益率波动损失风险%'],
        ['Monthly Adj Ret LPSD','月调整收益波动损失风险'],
        ['Monthly Adj Ret LPSD%','月调整收益波动损失风险%'],
        ['Quarterly Ret LPSD','季收益率波动损失风险'],
        ['Quarterly Ret LPSD%','季收益率波动损失风险%'],
        ['Quarterly Adj Ret LPSD','季调整收益率波动损失风险'],
        ['Quarterly Adj Ret LPSD%','季调整收益率波动损失风险%'],
        ['Annual Ret LPSD','年收益率波动损失风险'],
        ['Annual Ret LPSD%','年收益率波动损失风险%'],
        ['Annual Adj Ret LPSD','年调整收益率波动损失风险'], 
        ['Annual Adj Ret LPSD%','年调整收益率波动损失风险%'], 
        ['Exp Ret LPSD','持有收益率波动损失风险'], 
        ['Exp Ret LPSD%','持有收益率波动损失风险%'],
        ['Exp Adj Ret LPSD','持有调整收益率波动损失风险'],        
        ['Exp Adj Ret LPSD%','持有调整收益率波动损失风险%'],
        
        ['roll_spread','罗尔价差比率'],['amihud_illiquidity','阿米胡德非流动性'],
        ['ps_liquidity','P-S流动性'],    
        
        ['Gross Domestic Product','国内生产总值'],['GNI','国民生产总值'],    
        
        ['zip','邮编'],['sector','领域'],['fullTimeEmployees','全职员工数'],
        ['longBusinessSummary','业务介绍'],['city','城市'],['phone','电话'],
        ['state','州/省'],['country','国家/地区'],['companyOfficers','高管'],
        ['website','官网'],['address1','地址1'],['industry','行业'],
        ['previousClose','上个收盘价'],['regularMarketOpen','正常市场开盘价'],
        ['twoHundredDayAverage','200天均价'],['fax','传真'], 
        ['trailingAnnualDividendYield','年化股利率TTM'],
        ['payoutRatio','股息支付率'],['volume24Hr','24小时交易量'],
        ['regularMarketDayHigh','正常市场日最高价'],
        ['averageDailyVolume10Day','10天平均日交易量'],['totalAssets','总资产'],
        ['regularMarketPreviousClose','正常市场上个收盘价'],
        ['fiftyDayAverage','50天平均股价'],
        ['trailingAnnualDividendRate','年化每股股利金额TTM'],['open','当日开盘价'],
        ['averageVolume10days','10日平均交易量'],['expireDate','失效日'],
        ['yield','收益率'],['dividendRate','每股股利金额'],
        ['exDividendDate','股利除息日'],['beta','贝塔系数'],
        ['startDate','开始日期'],['regularMarketDayLow','正常市场日最低价'],
        ['priceHint','价格提示'],['currency','交易币种'],
        ['trailingPE','市盈率TTM'],['regularMarketVolume','正常市场交易量'],
        ['marketCap','市值'],['averageVolume','平均交易量'],
        ['priceToSalesTrailing12Months','市销率TTM'],['dayLow','当日最低价'],
        ['ask','卖出价'],['askSize','卖出价股数'],['volume','当日交易量'],
        ['fiftyTwoWeekHigh','52周最高价'],['forwardPE','预期市盈率'],
        ['fiveYearAvgDividendYield','5年平均股利率'],
        ['fiftyTwoWeekLow','52周最低价'],['bid','买入价'],
        ['tradeable','今日是否可交易'],['dividendYield','股利率'],
        ['bidSize','买入价股数'],['dayHigh','当日最高价'],
        ['exchange','交易所'],['shortName','简称'],['longName','全称'],
        ['exchangeTimezoneName','交易所时区'],
        ['exchangeTimezoneShortName','交易所时区简称'],['quoteType','证券类别'],
        ['symbol','证券代码'],['messageBoardId','证券留言板编号'],
        ['market','证券市场'],['annualHoldingsTurnover','一年內转手率'],
        ['enterpriseToRevenue','企业价值/销售收入'],['beta3Year','3年贝塔系数'],
        ['profitMargins','净利润率'],['enterpriseToEbitda','企业价值/EBITDA'],
        ['52WeekChange','52周股价变化率'],['morningStarRiskRating','晨星风险评级'],
        ['forwardEps','预期每股收益'],['revenueQuarterlyGrowth','季营收增长率'],
        ['sharesOutstanding','流通在外股数'],['fundInceptionDate','基金成立日'],
        ['annualReportExpenseRatio','年报费用比率'],['bookValue','每股净资产'],
        ['sharesShort','卖空股数'],['sharesPercentSharesOut','卖空股数/流通股数'],
        ['lastFiscalYearEnd','上个财年截止日期'],
        ['heldPercentInstitutions','机构持股比例'],
        ['netIncomeToCommon','归属普通股股东净利润'],['trailingEps','每股收益TTM'],
        ['lastDividendValue','上次股利价值'],
        ['SandP52WeekChange','标普指数52周变化率'],['priceToBook','市净率'],
        ['heldPercentInsiders','内部人持股比例'],['priceToBook','市净率'],
        ['nextFiscalYearEnd','下个财年截止日期'],
        ['mostRecentQuarter','上个财季截止日期'],['shortRatio','空头净额比率'],
        ['sharesShortPreviousMonthDate','上月做空日期'],
        ['floatShares','可交易股数'],['enterpriseValue','企业价值'],
        ['threeYearAverageReturn','3年平均回报率'],['lastSplitDate','上个拆分日期'],
        ['lastSplitFactor','上次拆分比例'],
        ['earningsQuarterlyGrowth','季盈余增长率'],['dateShortInterest','做空日期'],
        ['pegRatio','市盈率与增长比率'],['shortPercentOfFloat','空头占可交易股票比例'],
        ['sharesShortPriorMonth','上月做空股数'],
        ['fiveYearAverageReturn','5年平均回报率'],['regularMarketPrice','正常市场价'],
        ['logo_url','商标图标网址'],     ['underlyingSymbol','曾用代码'],     
        ['timeZoneShortName','时区简称'],['timeZoneFullName','时区全称'],
        ['exchangeName','交易所名称'],['currentPrice','当前价格'],
        ['ratingYear','评估年度'],['ratingMonth','评估月份'],
        ['currencySymbol','币种符号'],['recommendationKey','投资建议'],
        ['totalInsiderShares','内部人持股数'],['financialCurrency','财报币种'],
        ['currentRatio','流动比率'],['quickRatio','速动比率'],
        ['debtToEquity','负债-权益比'],['ebitdaMargins','EBITDA利润率'],
        ['operatingMargins','经营利润率'],['grossMargins','毛利润率'],
        ['returnOnAssets','ROA'],['returnOnEquity','ROE'],
        ['revenuePerShare','每股销售收入'],['totalCashPerShare','每股总现金'],
        ['revenueGrowth','销售收入增长率'],['earningsGrowth','盈余增长率'],
        ['totalDebt','总负债'],['totalRevenue','总销售收入'],
        ['grossProfits','毛利润'],['ebitda','EBITDA'],
        ['operatingCashflow','经营现金流'],['freeCashflow','自由现金流'],
        ['totalCash','总现金流'],
        
        ['overallRisk','总风险指数'],
        ['boardRisk','董事会风险指数'],['compensationRisk','薪酬风险指数'],
        ['shareHolderRightsRisk','股东风险指数'],['auditRisk','审计风险指数'],
        
        ['totalEsg','ESG总分数'],['esgPerformance','ESG业绩评价'],
        ['peerEsgScorePerformance','ESG同业分数'],['environmentScore','环保分数'],
        ['peerEnvironmentPerformance','环保同业分数'],['socialScore','社会责任分数'],
        ['peerSocialPerformance','社会责任同业分数'],['governanceScore','公司治理分数'],
        ['peerGovernancePerformance','公司治理同业分数'],['peerGroup','同业分组'],
        ['relatedControversy','相关焦点'],['Social Supply Chain Incidents','供应链事件'],
        ['Customer Incidents','客户相关事件'],['Business Ethics Incidents','商业道德事件'],
        ['Product & Service Incidents','产品与服务相关事件'],
        ['Society & Community Incidents','社会与社区相关事件'],
        ['Employee Incidents','雇员相关事件'],['Operations Incidents','运营相关事件'],
        ['peerCount','同业个数'],['percentile','同业所处分位数'],  
        
        ['ESGscore','ESG风险'],['ESGpercentile','ESG风险行业分位数%'],
        ['ESGperformance','ESG风险评价'],['EPscore','环保风险'],
        ['EPpercentile','环保风险分位数%'],['CSRscore','社会责任风险'],
        ['CSRpercentile','社会责任风险分位数%'],['CGscore','公司治理风险'],
        ['CGpercentile','公司治理风险分位数%'],
        ['Peer Group','业务分类'],['Count','数目'],          
        
        ], columns=['eword','cword'])

    try:
        cword=ecdict[ecdict['eword']==eword]['cword'].values[0]
    except:
        #未查到翻译词汇，返回原词
        cword=eword
   
    return cword

if __name__=='__main__':
    eword='Exp Adj Ret'
    print(ectranslate('Annual Adj Ret%'))
    print(ectranslate('Annual*Adj Ret%'))


#==============================================================================
def codetranslate(code):
    """
    翻译证券代码为证券名称。
    输入：证券代码。输出：证券名称
    """
    import pandas as pd
    codedict=pd.DataFrame([
        ['000002.SZ','万科地产A股'],['600266.SS','北京城建A股'],
        ['600519.SS','贵州茅台A股'],['601398.SS','工商银行A股'],
        ['601939.SS','建设银行A股'],['601288.SS','农业银行A股'],
        ['601988.SS','中国银行A股'],['601857.SS','中国石油A股'],
        ['000651.SZ','格力电器A股'],['000333.SZ','美的集团A股'],
        
        ['000300.SS','沪深300指数'],['399300.SS','沪深300指数'],
        ['000001.SS','上证综合指数'],['399001.SZ','深证成分指数'],
        ['000016.SS','上证50指数'],['000132.SS','上证100指数'],
        ['000133.SS','上证150指数'],['000010.SS','上证180指数'],
        ['000688.SS','科创板50指数'],['000043.SS','上证超大盘指数'],
        ['000044.SS','上证中盘指数'],['000046.SS','上证中小盘指数'],
        ['000045.SS','上证小盘指数'],['000004.SS','上证工业指数'],
        ['000005.SS','上证商业指数'],['000006.SS','上证地产指数'],
        ['000007.SS','上证公用指数'],['000038.SS','上证金融指数'],
        ['000057.SS','上证全指成长指数'],['000058.SS','上证全指价值指数'],
        ['000019.SS','上证治理指数'],['000048.SS','上证责任指数'],
        
        ['000002.SS','上证A股指数'],['000003.SS','上证B股指数'],
        ['399107.SZ','深证A股指数'],['399108.SZ','深证B股指数'],
        ['399106.SZ','深证综合指数'],['399004.SZ','深证100指数'],
        ['399012.SZ','创业板300指数'],
        
        ['399232.SZ','深证采矿业指数'],['399233.SZ','深证制造业指数'],
        ['399234.SZ','深证水电煤气指数'],['399236.SZ','深证批发零售指数'],
        ['399237.SZ','深证运输仓储指数'],['399240.SZ','深证金融业指数'],
        ['399241.SZ','深证房地产指数'],['399244.SZ','深证公共环保指数'],
        
        ['000903.SS','中证100指数'],['399903.SZ','中证100指数'],
        ['000904.SS','中证200指数'],['399904.SZ','中证200指数'],
        ['000905.SS','中证500指数'],['399905.SZ','中证500指数'],
        ['000907.SS','中证700指数'],['399907.SZ','中证700指数'],
        ['000906.SS','中证800指数'],['399906.SZ','中证800指数'],
        ['000852.SS','中证1000指数'],['399852.SZ','中证1000指数'],
        ['000985.SS','中证全指指数'],['399985.SZ','中证全指指数'],
        
        ['000012.SS','上证国债指数'],['000013.SS','上证企业债指数'],
        ['000022.SS','上证公司债指数'],['000061.SS','上证企债30指数'],
        ['000116.SS','上证信用债100指数'],['000101.SS','上证5年期信用债指数'],
        
        ["510050.SS",'上证50ETF基金'],['510880.SS','上证红利ETF基金'],
        ["510180.SS",'上证180ETF基金'],['159901.SZ','深证100ETF基金'],
        ["159902.SZ",'深证中小板ETF基金'],['159901.SZ','深证100ETF基金'],
        ["SPY",'SPDR SP500 ETF'],['SPYD','SPDR SP500 Div ETF'],
        ["SPYG",'SPDR SP500 Growth ETF'],['SPYV','SPDR SP500 Value ETF'],
        ["VOO",'Vanguard SP500 ETF'],['VOOG','Vanguard SP500 Growth ETF'],
        ["VOOV",'Vanguard SP500 Value ETF'],['IVV','iShares SP500 ETF'],        
        ["DGT",'SPDR Global Dow ETF'],['ICF','iShares C&S REIT ETF'], 
        ["FRI",'FT S&P REIT Index Fund'],
        
        ["HG=F",'COMEX Copper Future'],["CL=F",'NYM Crude Oil Future'],
        ["S=F",'CBT Soybean Future'],["C=F",'CBT Corn Future'],
        ["ES=F",'CME SP500 Future'],["YM=F",'CBT DJI Future'],
        ["NQ=F",'CME NASDAQ100 Future'],["RTY=F",'Russell 2K Future'],
        ["ZB=F",'US T-Bond Future'],["ZT=F",'2y US T-Note Future'],
        ["ZF=F",'5y US T-Note Future'],["ZN=F",'10y US T-Note Future'],        

        ['^GSPC','标普500指数'],['^DJI','道琼斯工业指数'],
        ['WISGP.SI','富时新加坡指数'], ['^STI','新加坡海峡时报指数'],
        ['^IXIC','纳斯达克综合指数'],['^FTSE','英国富时100指数'],
        ['FVTT.FGI','富时越南指数'],['^RUT','罗素2000指数'],
        ['^HSI','恒生指数'],['^N225','日经225指数'],
        ['WIKOR.FGI','富时韩国指数'],['^KS11','韩国综合指数'],
        ['^KOSPI','韩国综合指数'],['^BSESN','印度孟买敏感指数'],
        ['^FCHI','法国CAC40指数'],['^GDAXI','德国DAX30指数'], 
        ['IMOEX.ME','MOEX俄罗斯指数'], 
        
        ['^HSCE','恒生H股指数'],['^HSNC','恒生工商业指数'],['^HSNU','恒生公用行业指数'], 
        ['^TWII','台湾加权指数'], 
        
        ['^IRX','三个月美债利率'],['^FVX','五年美债利率'],
        ['^TNX','十年期美债利率'],['^TYX','三十年美债利率'],
        
        ['AAPL','苹果'],['MSFT','微软'],['AMZN','亚马逊'],['JD','京东美股'],
        ['FB','脸书'],['BABA','阿里巴巴美股'],['PTR','中石油美股'],
        ['ZM','ZOOM'],['C','花旗集团'],['F','福特汽车'],['GOOG','谷歌'],
        ['KO','可口可乐'],['PEP','百事可乐'],['IBM','国际商用机器'],
        ['HPQ','惠普'],['BA','波音'],['GM','通用汽车'],['INTC','英特尔'],
        ['AMD','超威半导体'],['NVDA','英伟达'],['PFE','辉瑞制药'],
        ['BILI','哔哩哔哩'],['TAL','好未来'],['EDU','新东方'],['VIPS','唯品会'],
        ['SINA','新浪网'],['BIDU','百度'],['NTES','网易'],['PDD','拼多多'],
        ['COST','好事多'],['WMT','沃尔玛'],['DIS','迪士尼'],['GS','高盛'],
        ['QCOM','高通'],['BAC','美国银行'],['TWTR','推特'],
        ['JPM','摩根大通'],['WFC','富国银行'],['GS','高盛集团'],['MS','摩根示丹利'],
        ['USB','美国合众银行'],['TD','道明银行'],['PNC','PNC金融'],['BK','纽约梅隆银行'],
        ['SLB','斯伦贝谢'],['COP','康菲石油'],['HAL','哈里伯顿'],['OXY','西方石油'],
        ['FCX','自由港矿业'],        

        ['Vipshop','唯品会'],['Amazon','亚马逊'],['Alibaba','阿里巴巴美股'],
        ['eBay','易贝'],['Pinduoduo','拼多多'],
        ['Apple','苹果'],['Berkshire','伯克希尔'],['Microsoft','微软'],
        ['LLY','礼来制药'],['Eli','礼来制药'],
        ['JNJ','强生制药'],['Johnson','强生制药'],
        ['VRTX','福泰制药'],['Vertex','福泰制药'],
        ['PFE','辉瑞制药'],['Pfizer','辉瑞制药'],
        ['MRK','默克制药'],['Merck','默克制药'],
        ['NVS','诺华制药'],['Novartis','诺华制药'],
        ['AMGN','安进制药'],['Amgen','安进制药'],
        ['SNY','赛诺菲制药'],['Sanofi','赛诺菲制药'],
        ['NBIX','神经分泌生物'],['Neurocrine','神经分泌生物'],
        ['REGN','再生元制药'],['Regeneron','再生元制药'],
        ['PRGO','培瑞克制药'],['Perrigo','培瑞克制药'],
        
        ['BAC','美国银行'],['Bank of America Corporation','美国银行'],
        ['JPM','摩根大通'],['JP Morgan Chase & Co','摩根大通'],
        ['WFC','富国银行'],
        ['MS','摩根示丹利'],['Morgan Stanley','摩根示丹利'],
        ['USB','美国合众银行'],['U','美国合众银行'],
        ['TD','道明银行'],['Toronto Dominion Bank','道明银行'],
        ['PNC','PNC金融'],['PNC Financial Services Group','PNC金融'],
        ['BK','纽约梅隆银行'],['The Bank of New York Mellon Cor','纽约梅隆银行'],    
        ['IEMG','iShares核心MSCI新兴市场ETF'],
        
        ['0700.HK','港股腾讯控股'],['9988.HK','阿里巴巴港股'],
        ['1810.HK','港股小米'],['0992.HK','港股联想'],['1398.HK','工商银行港股'],
        ['0939.HK','建设银行港股'],['1288.HK','农业银行港股'],
        ['3988.HK','中国银行港股'],['0857.HK','中国石油港股'],
        ['0005.HK','港股汇丰控股'],['2888.HK','港股渣打银行'],
        
        ['0700.HK','腾讯港股'],['TENCENT','腾讯控股'],
        ['9988.HK','阿里巴巴港股'],['BABA-SW','阿里巴巴港股'],
        ['9618.HK','京东港股'],['JD-SW','京东港股'],
        ['1810.HK','港股小米'],['0992.HK','港股联想'],['LENOVO GROUP','联想集团'],
        ['1398.HK','工商银行港股'],['ICBC','中国工商银行'],
        ['0939.HK','建设银行港股'],['CCB','中国建设银行'],
        ['1288.HK','农业银行港股'],['ABC','中国农业银行'],
        ['3988.HK','中国银行港股'],['BANK OF CHINA','中国银行'],
        ['0857.HK','中国石油港股'],['PETROCHINA','中国石油'],
        ['0005.HK','港股汇丰控股'],['HSBC HOLDINGS','汇丰控股'],
        ['2888.HK','港股渣打银行'],['STANCHART','渣打银行'],        
        ['2801.HK','iShares核心MSCI中国指数ETF'],
        
        ['6758.T','日股索尼'],['4911.T','日股资生堂'],['8306.T','三菱日联金融'],
        ['7203.T','日股丰田汽车'],['7267.T','日股本田汽车'],
        ['7201.T','日股日产汽车'],['8411.T','日股瑞穗金融'],['7182.T','日本邮政银行'],
        ['1605.T','国际石油开发帝石'],['5020.T','JXTG能源'],['5713.T','住友金属矿山'],
        ['4452.T','日股花王'],['9983.T','日股优衣库'],['7453.T','日股无印良品'],
        ['8306.T','三菱日联金融'],['MITSUBISHI UFJ FINANCIAL GROUP','三菱日联金融'],
        ['8411.T','日股瑞穗金融'],['MIZUHO FINANCIAL GROUP','瑞穗金融'],
        ['7182.T','日本邮政银行'],['JAPAN POST BANK CO LTD','日本邮政银行'],        
        
        ['TCS.NS','印度股塔塔咨询'],
        
        ['005930.KS','韩股三星电子'],['245710.KS','KINDEX越南VN30指数ETF'],
        
        ['UBSG.SW','瑞士股瑞银'],['UG.PA','法国股标致雪铁龙'],
        ['DAI.DE','德国股奔驰汽车'],['BMW.DE','德国股宝马汽车'],
        
        ['2330.TW','台积电'],['2317.TW','鸿海精密'],
        ['2474.TW','可成科技'],['3008.TW','大立光'],['2454.TW','联发科']        
        
        ], columns=['code','codename'])

    try:
        codename=codedict[codedict['code']==code]['codename'].values[0]
    except:
        #未查到翻译词汇，返回原词
        codename=code
   
    return codename

if __name__=='__main__':
    code='GOOG'
    print(codetranslate('000002.SZ'))
    print(codetranslate('9988.HK'))

#==============================================================================
def tickertranslate(code):
    """
    套壳函数
    输入：证券代码。输出：证券名称
    """
    codename=codetranslate(code)
    return codename

if __name__=='__main__':
    code='GOOG'
    print(tickertranslate('000002.SZ'))
    print(tickertranslate('9988.HK'))

#==============================================================================
#==============================================================================
def ticker_check(ticker, source="yahoo"):
    """
    检查证券代码，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码ticker，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #测试用，完了需要注释掉
    #ticker="600519.sh"
    #source="yahoo"
    
    #将字母转为大写
    ticker1=ticker.upper()
    #截取字符串最后2/3位
    suffix2=ticker1[-2:]
    suffix3=ticker1[-3:]
    
    #判断是否大陆证券
    if suffix3 in ['.SH', '.SS', '.SZ']:
        prc=True
    else: prc=False

    #根据数据源的格式修正大陆证券代码
    if (source == "yahoo") and (suffix3 in ['.SH']):
        ticker1=ticker1.replace(suffix3, '.SS')        
    if (source == "tushare") and (suffix3 in ['.SS']):
        ticker1=ticker1.replace(suffix3, '.SH')  

    #若为港交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共7位
    if suffix3 in ['.HK']:
        ticker1=ticker1[-7:]     

    #若为东交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共6位
    if suffix2 in ['.T']:
        ticker1=ticker1[-6:]  
    
    #返回：是否大陆证券，基于数据源/交易所格式修正后的证券代码
    return prc, ticker1        

#测试各种情形
if __name__=='__main__':
    prc, ticker=ticker_check("600519.sh","yahoo")
    print(prc,ticker)
    print(ticker_check("600519.SH","yahoo"))    
    print(ticker_check("600519.ss","yahoo"))    
    print(ticker_check("600519.SH","tushare"))    
    print(ticker_check("600519.ss","tushare"))    
    print(ticker_check("000002.sz","tushare"))
    print(ticker_check("000002.sz","yahoo"))
    print(ticker_check("00700.Hk","yahoo"))
    print(ticker_check("99830.t","yahoo"))

#==============================================================================
def tickers_check(tickers, source="yahoo"):
    """
    检查证券代码列表，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码列表tickers，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：证券代码列表，字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #检查列表是否为空
    if tickers[0] is None:
        print("*** 错误#1(tickers_check)，空的证券代码列表:",tickers)
        return None         
    
    tickers_new=[]
    for t in tickers:
        _, t_new = ticker_check(t, source=source)
        tickers_new.append(t_new)
    
    #返回：基于数据源/交易所格式修正后的证券代码
    return tickers_new

#测试各种情形
if __name__=='__main__':
    tickers=tickers_check(["600519.sh","000002.sz"],"yahoo")
    print(tickers)
#==============================================================================
def check_period(fromdate, todate):
    """
    功能：根据开始/结束日期检查日期与期间的合理性
    输入参数：
    fromdate：开始日期。格式：YYYY-MM-DD
    enddate：开始日期。格式：YYYY-MM-DD
    输出参数：
    validity：期间合理性。True-合理，False-不合理
    start：开始日期。格式：datetime类型
    end：结束日期。格式：datetime类型
    """
    import pandas as pd
    
    #测试开始日期的合理性
    try:
        start=pd.to_datetime(fromdate)
    except:
        print("*** 错误#1(check_period)，无效的日期:",fromdate)
        return None, None, None         
    
    #测试结束日期的合理性
    try:
        end=pd.to_datetime(todate)
    except:
        print("*** 错误#2(check_period)，无效的日期:",todate)
        return None, None, None          
    
    #测试日期期间的合理性
    if start > end:
        print("*** 错误#3(check_period)，无效的日期期间: 从",fromdate,"至",todate)
        return None, None, None     

    return True, start, end

if __name__ =="__main__":
    check_period('2020-1-1','2020-2-4')
    check_period('2020-1-1','2010-2-4')

#==============================================================================
def date_adjust(basedate, adjust=0):
    """
    功能：将给定日期向前或向后调整特定的天数
    输入：基础日期，需要调整的天数。
    basedate: 基础日期。
    adjust：需要调整的天数，负数表示向前调整，正数表示向后调整。
    输出：调整后的日期。
    """
    #检查基础日期的合理性
    import pandas as pd    
    try:
        bd=pd.to_datetime(basedate)
    except:
        print("*** 错误#1(date_adjust)，无效的日期:",basedate)
        return None

    #调整日期
    from datetime import timedelta
    nd = bd+timedelta(days=adjust)    
    
    #重新提取日期
    newdate=nd.date()   
    return str(newdate)
 
if __name__ =="__main__":
    basedate='2020-3-17' 
    adjust=-365    
    newdate = date_adjust(basedate, adjust)
    print(newdate)    

#==============================================================================
def decompose_portfolio(portfolio):
    """
    功能：将一个投资组合字典分解为股票代码列表和份额列表
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合
    输出：市场，市场指数，股票代码列表和份额列表
    """
    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    
    #从字典中提取信息
    keylist=list(portfolio.keys())
    scope=portfolio[keylist[0]][0]
    mktidx=portfolio[keylist[0]][1]
    
    slist=[]
    plist=[]
    for key,value in portfolio.items():
        slist=slist+[key]
        plist=plist+[value]
    stocklist=slist[1:]    
    portionlist=plist[1:]

    return scope,mktidx,stocklist,portionlist    

if __name__=='__main__':
    portfolio1={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    scope,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio1)
    _,_,tickerlist,sharelist=decompose_portfolio(portfolio1)


#==============================================================================
def calc_monthly_date_range(start,end):
    """
    功能：返回两个日期之间各个月份的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个月份的开始和结束日期元组对列表
    """
    #测试用
    #start='2019-01-05'
    #end='2019-06-25'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当月的结束日期
    syear=startdate.year
    smonth=startdate.month
    import calendar
    sdays=calendar.monthrange(syear,smonth)[1]
    from datetime import date
    slastday=pd.to_datetime(date(syear,smonth,sdays))

    if slastday > enddate: slastday=enddate
    
    #加入第一月的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束月的开始和结束日期
    eyear=enddate.year
    emonth=enddate.month
    efirstday=pd.to_datetime(date(eyear,emonth,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个月份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(months=+1)
    while next < efirstday:
        nyear=next.year
        nmonth=next.month
        nextstart=pd.to_datetime(date(nyear,nmonth,1))
        ndays=calendar.monthrange(nyear,nmonth)[1]
        nextend=pd.to_datetime(date(nyear,nmonth,ndays))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(months=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_monthly_date_range('2019-01-01','2019-06-30')
    mdp2=calc_monthly_date_range('2000-01-01','2000-06-30')   #闰年
    mdp3=calc_monthly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)


#==============================================================================
def calc_yearly_date_range(start,end):
    """
    功能：返回两个日期之间各个年度的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个年度的开始和结束日期元组对列表
    """
    #测试用
    #start='2013-01-01'
    #end='2019-08-08'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当年的结束日期
    syear=startdate.year
    from datetime import date
    slastday=pd.to_datetime(date(syear,12,31))

    if slastday > enddate: slastday=enddate
    
    #加入第一年的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束年的开始和结束日期
    eyear=enddate.year
    efirstday=pd.to_datetime(date(eyear,1,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个年份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(years=+1)
    while next < efirstday:
        nyear=next.year
        nextstart=pd.to_datetime(date(nyear,1,1))
        nextend=pd.to_datetime(date(nyear,12,31))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(years=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_yearly_date_range('2013-01-05','2019-06-30')
    mdp2=calc_yearly_date_range('2000-01-01','2019-06-30')   #闰年
    mdp3=calc_yearly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)

#==============================================================================

def sample_selection(df,start,end):
    """
    功能：根据日期范围start/end选择数据集df的子样本，并返回子样本
    """
    flag,start2,end2=check_period(start,end)
    df_sub=df[df.index >= start2]
    df_sub=df_sub[df_sub.index <= end2]
    
    return df_sub
    
if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    market,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio)
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(tickerlist,sharelist,start,end)
    start2='2020-1-10'; end2='2020-3-18'
    df_sub=sample_selection(pfdf,start2,end2)    
    
#==============================================================================
def init_ts():
    """
    功能：初始化tushare pro，登录后才能下载数据
    """
    import tushare as ts
    #设置token
    token='49f134b05e668d288be43264639ac77821ab9938ff40d6013c0ed24f'
    pro=ts.pro_api(token)
    
    return pro
#==============================================================================
def convert_date_ts(y4m2d2):
    """
    功能：日期格式转换，YYYY-MM-DD-->YYYYMMDD，用于tushare
    输入：日期，格式：YYYY-MM-DD
    输出：日期，格式：YYYYMMDD
    """
    import pandas as pd
    try: date1=pd.to_datetime(y4m2d2)
    except:
        print("Error #1(convert_date_tushare): invalid date:",y4m2d2)
        return None 
    else:
        date2=date1.strftime('%Y')+date1.strftime('%m')+date1.strftime('%d')
    return date2

if __name__ == '__main__':
    convert_date_ts("2019/11/1")
#==============================================================================
def gen_yearlist(start_year,end_year):
    """
    功能：产生从start_year到end_year的一个年度列表
    输入参数：
    start_year: 开始年份，字符串
    end_year：截止年份
    输出参数：
    年份字符串列表    
    """
    #仅为测试使用，完成后应注释掉
    #start_year='2010'
    #end_year='2019'    
    
    import numpy as np
    start=int(start_year)
    end=int(end_year)
    num=end-start+1    
    ylist=np.linspace(start,end,num=num,endpoint=True)
    
    yearlist=[]
    for y in ylist:
        yy='%d' %y
        yearlist=yearlist+[yy]
    #print(yearlist)
    
    return yearlist

if __name__=='__main__':
    yearlist=gen_yearlist('2013','2019')
#==============================================================================
def print_progress_bar(current,startnum,endnum):
    """
    功能：打印进度数值，每个10%打印一次，不换行
    """
    for i in [9,8,7,6,5,4,3,2,1]:
        if current == int((endnum - startnum)/10*i)+1: 
            print(str(i)+'0%',end=' '); break
        elif current == int((endnum - startnum)/100*i)+1: 
            print(str(i)+'%',end=' '); break
    if current == 2: print('0%',end=' ')

if __name__ =="__main__":
    startnum=2
    endnum=999
    L=range(2,999)
    for c in L: print_progress_bar(c,startnum,endnum)

#==============================================================================
def save_to_excel(df,filedir,excelfile,sheetname="Sheet1"):
    """
    函数功能：将df保存到Excel文件。
    如果目录不存在提示出错；如果Excel文件不存在则创建之文件并保存到指定的sheet；
    如果Excel文件存在但sheet不存在则增加sheet并保存df内容，原有sheet内容不变；
    如果Excel文件和sheet都存在则追加df内容到已有sheet的末尾
    输入参数：
    df: 数据框
    filedir: 目录
    excelfile: Excel文件名，不带目录，后缀为.xls或.xlsx
    sheetname：Excel文件中的sheet名
    输出：
    保存df到Excel文件
    无返回数据
    
    注意：如果df中含有以文本表示的数字，写入到Excel会被自动转换为数字类型保存。
    从Excel中读出后为数字类型，因此将会与df的类型不一致
    """

    #检查目录是否存在
    import os
    try:
        os.chdir(filedir)
    except:
        print("Error #1(save_to_excel): folder does not exist")        
        print("Information:",filedir)  
        return
                
    #取得df字段列表
    dflist=df.columns
    #合成完整的带目录的文件名
    filename=filedir+'/'+excelfile
    
    import pandas as pd
    try:
        file1=pd.ExcelFile(excelfile)
    except:
        #不存在excelfile文件，直接写入
        df.to_excel(filename,sheet_name=sheetname, \
                       header=True,encoding='utf-8')
        print("***Results saved in",filename,"@ sheet",sheetname)
        return
    else:
        #已存在excelfile文件，先将所有sheet的内容读出到dict中        
        dict=pd.read_excel(file1, None)
    file1.close()
    
    #获得所有sheet名字
    sheetlist=list(dict.keys())
    
    #检查新的sheet名字是否已存在
    try:
        pos=sheetlist.index(sheetname)
    except:
        #不存在重复
        dup=False
    else:
        #存在重复，合并内容
        dup=True
        #合并之前可能需要对df中以字符串表示的数字字段进行强制类型转换.astype('int')
        df1=dict[sheetlist[pos]][dflist]
        dfnew=pd.concat([df1,df],axis=0,ignore_index=True)        
        dict[sheetlist[pos]]=dfnew
    
    #将原有内容写回excelfile    
    result=pd.ExcelWriter(filename)
    for s in sheetlist:
        df1=dict[s][dflist]
        df1.to_excel(result,s,header=True,index=True,encoding='utf-8')
    #写入新内容
    if not dup: #sheetname未重复
        df.to_excel(result,sheetname,header=True,index=True,encoding='utf-8')
    try:
        result.save()
        result.close()
    except:
        print("Error #2(save_to_excel): writing file permission denied")
        print("Information:",filename)  
        return
    print("***Results saved in",filename,"@ sheet",sheetname)
    return       
#==============================================================================
def set_df_period(df,df_min,df_max):
    """
    功能： 去掉df中日期范围以外的记录
    """
    df1=df[df.index >= df_min]
    df2=df1[df1.index <= df_max]
    return df2

if __name__=='__main__':
    import siat.security_prices as ssp
    df=ssp.get_price('AAPL','2020-1-1','2020-1-31')    
    df_min,df_max=get_df_period(df)    
    df2=set_df_period(df,df_min,df_max)

#==============================================================================
def sigstars(p_value):
    """
    功能：将p_value转换成显著性的星星
    """
    if p_value >= 0.1: 
        stars="   "
        return stars
    if 0.1 > p_value >= 0.05:
        stars="*  "
        return stars
    if 0.05 > p_value >= 0.01:
        stars="** "
        return stars
    if 0.01 > p_value:
        stars="***"
        return stars

#==============================================================================

def regparms(results):
    """
    功能：将sm.OLS回归结果生成数据框，包括变量名称、系数数值、t值、p值和显著性星星
    """
    import pandas as pd
    #取系数
    params=results.params
    df_params=pd.DataFrame(params)
    df_params.columns=['coef']
    
    #取t值
    tvalues=results.tvalues
    df_tvalues=pd.DataFrame(tvalues)
    df_tvalues.columns=['t_values']

    #取p值
    pvalues=results.pvalues
    df_pvalues=pd.DataFrame(pvalues)
    df_pvalues.columns=['p_values']            

    #生成星星
    df_pvalues['sig']=df_pvalues['p_values'].apply(lambda x:sigstars(x))
    
    #合成
    parms1=pd.merge(df_params,df_tvalues, \
                    how='inner',left_index=True,right_index=True)
    parms2=pd.merge(parms1,df_pvalues, \
                    how='inner',left_index=True,right_index=True)

    return parms2
#==============================================================================
if __name__=='__main__':
    txt='QDII-指数'

def strlen(txt):
    """
    功能：计算中英文混合字符串的实际长度
    """
    lenTxt = len(txt) 
    lenTxt_utf8 = len(txt.encode('utf-8')) 
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)    

    return size

#==============================================================================

def sort_pinyin(hanzi_list): 
    """
    功能：对列表中的中文字符串按照拼音升序排序
    """
    from pypinyin import lazy_pinyin       
    hanzi_list_pinyin=[]
    hanzi_list_pinyin_alias_dict={}
    
    for single_str in hanzi_list:
        py_r = lazy_pinyin(single_str)
        # print("整理下")
        single_str_py=''
        for py_list in py_r:
            single_str_py=single_str_py+py_list
        hanzi_list_pinyin.append(single_str_py)
        hanzi_list_pinyin_alias_dict[single_str_py]=single_str
    
    hanzi_list_pinyin.sort()
    sorted_hanzi_list=[]
    
    for single_str_py in hanzi_list_pinyin:
        sorted_hanzi_list.append(hanzi_list_pinyin_alias_dict[single_str_py])
    
    return sorted_hanzi_list


#==============================================================================
def get_start_date(end_date,pastyears=1):
    """
    输入参数：一个日期，年数
    输出参数：几年前的日期
    start_date, end_date是datetime类型
    """

    import pandas as pd
    try:
        end_date=pd.to_datetime(end_date)
    except:
        print("#Error(): invalid date,",end_date)
        return None
    
    from datetime import datetime,timedelta
    start_date=datetime(end_date.year-pastyears,end_date.month,end_date.day)
    start_date=start_date-timedelta(days=1)
    # 日期-1是为了保证计算收益率时得到足够的样本数量
    return start_date
    
#==============================================================================
def get_ip():
    """
    功能：获得本机计算机名和IP地址    
    """
    #内网地址
    import socket
    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)
    
    #公网地址

    return hostname,internal_ip

if __name__=='__main__':
    get_ip()
#==============================================================================
def check_date(adate):
    """
    功能：检查一个日期是否为有效日期
    输入参数：一个日期
    输出：合理日期为True，其他为False
    """
    #仅为测试使用，测试完毕需要注释掉
    #adate='2019-6-31'

    result=True
    import pandas as pd
    try:    
        bdate=pd.to_datetime(adate)
    except:
        print("Error #1(check_date): Date invalid")
        print("Variable(s):",adate)
        result=False
        
    return result

if __name__ =="__main__":
    print(check_date('2019-6-31'))


#==============================================================================
def check_start_end_dates(start,end):
    """
    功能：检查一个期间的开始/结束日期是否合理
    输入参数：开始和结束日期
    输出：合理为True，其他为False
    """
    #仅为测试使用，测试完毕需要注释掉
    #adate='2019-6-31'

    if not check_date(start):
        print("Error #1(check_start_end_dates): invalid start date")
        print("Variable(s):",start)
        return False

    if not check_date(end):
        print("Error #2(check_start_end_dates): invalid end date")
        print("Variable(s):",end)
        return False       
    
    if start > end:
        print("Error #3(check_start_end_dates): irrational start/end dates")
        print("Variable(s): from",start,"to",end)
        return False
        
    return True

if __name__ =="__main__":
    print(check_start_end_dates('2019-1-1','2019-8-18'))

#==============================================================================
if __name__=='__main__':
    txt="上市公司/家"        
        
def hzlen(txt):
    """
    功能：计算含有汉字的字符串的长度
    """
    #strlen=int((len(txt.encode('utf-8')) - len(txt)) / 2 + len(txt))
    #strlen=int((len(txt.encode('gb18030')) - len(txt)) / 2 + len(txt))
    
    import unicodedata
    #Unicode字符有不同的类别
    txtlist=list(unicodedata.category(c) for c in txt)
    strlen=0
    for t in txtlist:
        #类别Lo表示一个非拉丁文字
        if t == 'Lo':
            strlen=strlen+2
        else:
            strlen=strlen+1
    
    return strlen

#==============================================================================
def int10_to_date(int10):
    """
    功能：将10位数字的时间戳转换为日期。
    输入：10位数字的时间戳int10。
    返回：日期字符串。
    """
    import time
    tupTime = time.localtime(int10)
    y4m2d2 = time.strftime("%Y-%m-%d", tupTime)    
    return y4m2d2

if __name__ =="__main__":
    int10=9876543210
    print(int10_to_date(int10))    
#==============================================================================
def equalwidth(string,maxlen=20):
    """
    输入：字符串，中英文混合
    输出：设定等宽度，自动补齐
    """
    reallen=hzlen(string)
    if maxlen < reallen:
        maxlen = reallen
    return string+'.'*(maxlen-reallen)+'：'

if __name__ =="__main__":
    equalwidth("中文1英文abc",maxlen=20)
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
