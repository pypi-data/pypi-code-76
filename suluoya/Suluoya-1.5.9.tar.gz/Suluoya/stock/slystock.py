import pandas as pd
from tqdm import tqdm
from tqdm import trange
import numpy as np
import random
import scipy.optimize as sco
import os
from .getstock import getstock


class slystock(object):
    def __init__(self, names=None,
                start_date='2020-12-01', 
                end_date='2020-12-31',
                frequency="w"):
        print('initializing...')
        print('Please make sure that all of the stocks are in the market!')
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.gs = getstock(names=names,
                        start_date=start_date, 
                        end_date=end_date,
                        frequency=frequency)
        self.names = names
        self.combinations = self.gs.combine
        self.information = self.gs.stock_data
        self.codes = self.information[0]
        self.stock_pair = self.information[1]
        self.stock_data = self.information[2]

    def correlation(self, x, y):
        if type(x) == list:
            x = np.array(x)
        if type(y) == list:
            y = np.array(y)
        return (np.dot([xi - np.mean(x) for xi in x], [yi - np.mean(y) for yi in y])/(len(x)-1))/((x.std())*(y.std()))

    def weight(self, lists=['A', 'B', 'C'], mode='dict'):
        if mode == 'dict':
            weights = np.random.dirichlet(np.ones(len(lists)), size=1)[0]
            rand = {}
            for i in range(0, len(lists)):
                rand[lists[i]] = weights[i]
            return rand
        elif mode == 'list':
            weights = np.random.dirichlet(np.ones(len(lists)), size=1)[0]
            rand = {}
            for i in range(0, len(lists)):
                rand[lists[i]] = weights[i]
            return list(rand.values())

    def sharp(self, weights=[], stock_list=[], no_risk_rate=0.45/5200):
        if weights == []:
            weights = len(self.names) * [1. / len(self.names), ]
        if stock_list == []:
            stock_list = self.names
        df_temp = self.stock_data
        df_temp = df_temp[['pctChg', 'name']]
        df = df_temp[['name']]
        df['pctChg'] = df_temp['pctChg'].astype('float')
        del df_temp
        covs = []
        for i in range(0, len(stock_list)):
            for j in stock_list[i:]:
                if stock_list[i] != j:
                    covs.append([stock_list[i], j])
        for i in covs:
            x = list(df[df['name'] == i[0]]['pctChg'])
            y = list(df[df['name'] == i[1]]['pctChg'])
            i.append(self.correlation(x, y))
        dic = {}
        rate = 0
        risk = 0
        c = 0
        rand = {}
        for i in stock_list:
            rand[i] = weights[c]
            c += 1
        for i in stock_list:
            data = list(df[df['name'] == i]['pctChg'])
            Mean = np.mean(data)
            Std = np.std(data)
            weight = rand[i]
            rate += Mean*weight
            risk += (weight*Std)**2
            dic[i] = weight*Std
        for i in covs:
            risk += 2*i[2]*dic[i[0]]*dic[i[1]]
        sharp = (rate-no_risk_rate)/risk
        return {'sharp': sharp, 'rate': rate, 'risk': risk, 'weight': rand}

    def max_sharp(self, weights, *args):
        print('iterating...')
        stock_list = args[0]
        print('weights:', weights)
        return -self.sharp(weights=weights, stock_list=stock_list)['sharp']

    def Markowit(self, stock_list=[], accurate=True, number=500, no_risk_rate=0.45/5200):
        if stock_list == []:
            stock_list = self.names
        if accurate == True:
            print('building a portfolio...')
            opts = sco.minimize(fun=self.max_sharp,
                                x0=len(stock_list) * [1. / len(stock_list), ],
                                method='SLSQP',
                                args=(stock_list,),
                                bounds=tuple((0, 1)
                                            for x in range(len(stock_list))),
                                constraints={'type': 'eq',
                                            'fun': lambda x: np.sum(x) - 1}
                                )
            count = 0
            result = {}
            ans = list(opts['x'])
            for i in stock_list:
                result[i] = ans[count]
                count += 1
            return [result, -opts['fun']]
        else:
            print('building a portfolio...')
            lists = []
            for i in trange(number):
                weights = self.weight(lists=stock_list, mode='list')
                sharp = self.sharp(
                    weights=weights, stock_list=stock_list, no_risk_rate=0.45/5200)
                lists.append(list(sharp.values()))
            df = pd.DataFrame(
                lists, columns=['sharp', 'rate', 'risk', 'weight'])
            df = df.sort_values('sharp', ascending=False)
            return df

    def portfolio(self, accurate=False, number=500, no_risk_rate=0.45/5200):
        if accurate == False:
            zuhe = self.combinations
            zuhe = zuhe[zuhe['amount'] > 1]
            try:
                os.makedirs('./all')
            except:
                pass
            for i, j in zuhe.iterrows():
                file = str(j[0]).replace('[', '').replace(']', '')
                print('calculating', file, '...')
                df = self.Markowit(
                    stock_list=j[0], accurate=False, number=number)
                df.to_csv(f'all\\{file}.csv', index=False, encoding='utf8')
            path = './all'
            filenames = os.listdir(path)
            result = pd.DataFrame()
            for i in filenames:
                df = pd.read_csv(path+'/'+i)
                max_sharp = df.iloc[0]
                result[i.replace('.csv', '')] = max_sharp
            result = result.T
            result = result.sort_values('sharp', ascending=False)
            result.to_csv('result.csv')
            return result.iloc[0]['weight']  # 最佳投资组合
        else:
            zuhe = self.combinations
            zuhe = zuhe[zuhe['amount'] > 1]
            result = []
            for i, j in zuhe.iterrows():
                file = str(j[0]).replace('[', '').replace(']', '')
                print('calculating', file, '...')
                result.append(self.Markowit(stock_list=j[0], accurate=True))
            df = pd.DataFrame(result, columns=['weights', 'sharp'])
            df = df.sort_values('sharp', ascending=False)
            return df
    def save_result(self):
        df=self.portfolio(accurate=True)
        df.to_csv('result.csv',index=False,encoding='utf8')
        return df
    
    def quit(self):
        self.gs.quit()


