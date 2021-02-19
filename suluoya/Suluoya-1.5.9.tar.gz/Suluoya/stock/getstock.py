import pandas as pd
import baostock as bs
from tqdm import tqdm
from itertools import combinations
class getstock(object):
    def __init__(self, names=None,
                start_date='2020-12-01', end_date='2020-12-31', 
                frequency="w"):
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        if type(names) == str:
            self.names = [names]
        elif type(names) == list:
            self.names = names
        self.bs = bs
        
    @property
    def stock_pair(self):
        print('getting stock pair...')
        lists = []
        for i in tqdm(self.names):
            rs = self.bs.query_stock_industry()
            rs = self.bs.query_stock_basic(code_name=i)
            industry_list = []
            while (rs.error_code == '0') & rs.next():
                industry_list.append(rs.get_row_data())
            info = pd.DataFrame(industry_list, columns=rs.fields)
            lists.append(info)
        df=pd.concat(lists)    
        stocks = {}
        for i, j in df[['code', 'code_name']].iterrows():
            stocks[j[1]] = j[0]
        return stocks

    @property
    def stock_data(self, info="date,code,open,close,volume,amount,adjustflag,turn,pctChg",
                start_date='2020-12-01', end_date='2020-12-31', frequency="w"):
        self.bs.login()
        stock_pair=self.stock_pair
        codes = list(stock_pair.values())
        Name={}
        for i,j in stock_pair.items():
            Name[j]=i
        lists = []
        print('getting stock data...')
        for i in tqdm(codes):
            rs = bs.query_history_k_data_plus(i, info,
                                            start_date=self.start_date, end_date=self.end_date,
                                            frequency=self.frequency, adjustflag="3")
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            result['name'] = Name[i]
            lists.append(result)
        df=pd.concat(lists)
        return codes, stock_pair, df
    @property
    def combine(self):
        print('building a combinations...')
        results = []
        for j in range(1, len(self.names)+1):
            for i in combinations(self.names, j):
                result = []
                result.append(list(i))
                result.append(j)
                results.append(result)
        return pd.DataFrame(results, columns=['group', 'amount'])
    def quit(self):
        self.bs.logout()