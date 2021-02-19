#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 11:38:04 2021

@author: zhaoyang
"""

import pandas as pd
import numpy as np
import seaborn as sns
import math
from sklearn import preprocessing
from sklearn.decomposition import PCA
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo

import warnings
warnings.filterwarnings('ignore')


#psi计算公式

def CalcBinPSI(x):
    if x.countRatio2 ==0 and x.countRatio1 == 0:
        PSI = 0
    elif x.countRatio1 == 0:
        PSI = 0.05
    else:
        PSI = (x.countRatio2 - x.countRatio1)*np.log(x.countRatio2*1.0 / x.countRatio1)
    return PSI

class Feature_Evalution:
    
    def __init__(self,data,exclude_cols,label):

        self.data = data
        self.exclude_cols = exclude_cols
        self.label =label


    def gen_lambda(self,binning):
        temp = binning
        lambda_list = []
        for i in range(len(temp)):
            if i==0:
                lambda_list = 'lambda x: %d if (x<=%f)'%(temp.loc[i,'coarse_bin'],temp.loc[i,'ub'])
            elif i!=len(binning)-1:
                lambda_list = lambda_list + ' else %d if (x>%f) & (x<=%f)'%(temp.loc[i,'coarse_bin'],temp.loc[i,'lb'],temp.loc[i,'ub'])
            else:
                lambda_list = lambda_list + ' else %d if (x>%f) else np.nan'%(temp.loc[i,'coarse_bin'],temp.loc[i,'lb'])
        return lambda_list


    def cut_bin(self):
        
        # 剔除非数值型变量 
        var_types = self.data.drop(self.exclude_cols,axis=1).dtypes.reset_index()
        var_types.columns = ['var','type'] #float64, int64, object
        numeric_col = var_types[(var_types['type']=='float64')|(var_types['type']=='int64')]['var'].tolist()
        exclude_cols_new = self.exclude_cols + var_types[var_types['type']=='object']['var'].tolist()
        
        # 分箱后的data
        data_coarse_bin = self.data[exclude_cols_new]
        
        # 对数值型变量依次进行分箱处理
        for col in numeric_col:
            if len(data[col].unique())<10:
                data_coarse_bin[col] =self.data[col]
            else:
                split_values = self.data[col].quantile(np.linspace(0.05,0.95,num=9)).reset_index()[col].unique()
                binning = pd.DataFrame({'lb':[-99999]+split_values.tolist(),'ub':split_values.tolist()+[99999]}).reset_index()
                binning.rename(columns={'index':'coarse_bin'},inplace=True)
                binning['var'] = col
                binning = binning[['var','coarse_bin','lb','ub']]
                lambda_list = self.gen_lambda(binning)
                data_coarse_bin[col] = list(map(eval(lambda_list),data[col]))
        return data_coarse_bin

    def IV(self):
        data_new = self.cut_bin()
        IV_list=[]
        calc_cols=data_new.drop(self.exclude_cols,axis=1).columns.values
        for col in calc_cols:
            Xvar = data_new[col]
            Yvar = data_new[label]
            N_0  = np.sum(Yvar==0)
            N_1 = np.sum(Yvar==1)
            N_0_group = np.zeros(np.unique(Xvar).shape)
            N_1_group = np.zeros(np.unique(Xvar).shape)
            for i in range(len(np.unique(Xvar))):
                N_0_group[i] = Yvar[(Xvar == np.unique(Xvar)[i]) & (Yvar == 0)].count()
                N_1_group[i] = Yvar[(Xvar == np.unique(Xvar)[i]) & (Yvar == 1)].count()
            iv = np.sum((N_0_group/N_0 - N_1_group/N_1) * np.log((0.0000000000001+N_0_group/N_0)/(0.0000000000001+N_1_group/N_1)))
            IV_list.append(iv)
        return  IV_list

    #####1.1 Gini计算
    
    def Gini(self):
        gini_list=[]
        calc_cols=self.data.drop(self.exclude_cols,axis=1).columns.values
        data_new = self.cut_bin()
        for col in calc_cols: 
            label_col=self.label
            temp = data_new[[col,label_col]].reset_index().groupby([col,label_col]).agg({'index':'count'}).reset_index()
            temp.columns = [col,label_col,'num']
            temp_wide = temp.pivot_table(index=col,columns=label_col,values='num').reset_index()
            temp_wide.columns = [col,'count0','count1']
            temp_wide['count0'] = temp_wide['count0'].apply(lambda x: 0 if math.isnan(x) else x)
            temp_wide['count1'] = temp_wide['count1'].apply(lambda x: 0 if math.isnan(x) else x)
            temp_wide['pct0'] = temp_wide['count0'].apply(lambda x: x/temp_wide['count0'].sum())
            pct0_list = temp_wide['pct0'].tolist()

            cum_pct0 = np.cumsum(sorted(np.append(pct0_list, 0)))
            sum_pct0 = cum_pct0[-1]
            xarray = np.array(range(0, len(cum_pct0))) / np.float(len(cum_pct0)-1)
            yarray = cum_pct0 / sum_pct0
            B = np.trapz(y=yarray, x=xarray)
            A = 0.5 - B
            gini = A / (A+B)
            gini_list.append(gini)
        return gini_list


    ####1.3 卡方计算
    
    def select_chi2(self):
        from sklearn.feature_selection import SelectKBest
        from sklearn.feature_selection import chi2
        gini_list=[]
        cols=self.data.drop(self.exclude_cols,axis=1).columns.values
        x = self.data[cols]
        y = self.data[self.label]
        chi2,p=chi2(x, y)
        return chi2


    ### 1.4 最大信息系数评估
    def mine(self):
        from minepy import MINE
        mine = MINE(alpha=0.6, c=15)
        mic_scores = []
        calc_cols=data.drop(self.exclude_cols,axis=1).columns.values
        data_new = self.cut_bin()
        x = self.data[calc_cols]
        y = self.data[self.label]
        for i in range(x.shape[1]):
            mine.compute_score(x.iloc[:,i], y)
            m = mine.mic()
            mic_scores.append(m)
        return mic_scores



    ##############2. 基于学习模型特征重要性评估###############

    ###2.1 随机森林
    
    def select_rf(self):

        from sklearn.ensemble import RandomForestClassifier 
        data_new=self.data.drop(self.exclude_cols,axis=1)
        cols=data_new.columns.tolist()
        x = self.data[cols]
        y = self.data[self.label]
        rfmodel = RandomForestClassifier(random_state=0)
        rfmodel = rfmodel.fit(x, y)
        return rfmodel.feature_importances_


    ##2.2 特征稳定性评估
    
    def select_Lasso(self):
        
        from stability_selection import RandomizedLasso
        data_new=self.data.drop(self.exclude_cols,axis=1)
        cols=data_new.columns.tolist()
        x = self.data[cols]
        y = self.data[self.label]
        rlasso = RandomizedLasso(alpha=0.025)
        rlasso.fit(x, y)
        return rlasso.coef_

    ##2.3 递归特征消除排序

    def select_rfe(self):

        from sklearn.feature_selection import RFE
        from sklearn.linear_model import LinearRegression
        data_new=self.data.drop(self.exclude_cols,axis=1)
        cols=data_new.columns.tolist()
        x = self.data[cols]
        y = self.data[self.label]
        lr = LinearRegression()

        rfe = RFE(lr, n_features_to_select=1)
        rfe.fit(x,y)
        return rfe.ranking_



    ##############3. 结果汇总，特征排序###############
    
    def feature_importance(self,methods):
        result = pd.DataFrame()
        exclude_cols.append(self.label)
        result['feature'] = self.data.drop(exclude_cols,axis=1).columns.values.tolist()
        result['rank_sum'] = 0
        if 'iv' in methods:        
            result['IV'] = self.IV()
            result['IV_rank'] = result['IV'].rank(ascending=False)
            result['rank_sum'] =result['rank_sum']+result['IV_rank']
        if 'gini' in methods:        
            result['Gini'] = self.Gini()
            result['Gini_rank'] = result['Gini'].rank(ascending=True)
            result['rank_sum'] =result['rank_sum']+result['Gini_rank']
        if 'chi2' in methods:
            result['chi2'] = self.select_chi2()
            result['chi2_rank'] = result['chi2'].rank(ascending=False)
            result['rank_sum'] =result['rank_sum']+result['chi2_rank']
        if 'mic' in methods:
            result['mic'] = self.mine()
            result['mic_rank'] = result['mic'].rank(ascending=False)
            result['rank_sum'] =result['rank_sum']+result['mic_rank']
        if 'rf' in methods:
            result['rf'] = self.select_rf()
            result['rf_rank'] = result['rf'].rank(ascending=False)
            result['rank_sum'] =result['rank_sum']+result['rf_rank']
        if 'Lasso' in methods:
            result['Lasso'] = self.select_Lasso()
            result['Lasso_rank'] = result['Lasso'].rank(ascending=False)
            result['rank_sum'] =result['rank_sum']+result['Lasso_rank']
        if 'rfe' in methods:
            result['rfe'] = self.select_rfe()
            result['rank_sum'] =result['rank_sum']+result['rfe']
        return result


    ###################################特征聚类#####################################

    # 特征相关系数

    def corr_analysis(self):
        exclude_cols.append(self.label)
        xnames = self.data.drop(self.exclude_cols,axis=1).columns.values.tolist()
        corr = self.data[xnames].corr()
        return corr

    # 数据预处理
    
    def data_preprocessing(self):
        
        minmax = preprocessing.MinMaxScaler()
        exclude_cols.append(self.label)
        xnames = self.data.drop(self.exclude_cols,axis=1).columns.values.tolist()
        data_minmax = minmax.fit_transform(self.data[xnames])

        return data_minmax

    
    # 测试数据集是否适合做PCA或因子分析
    
    def adequacy_test(self):
        data_minmax = self.data_preprocessing()
        chi_square_value,p_value=calculate_bartlett_sphericity(data_minmax)
        if p_value <= 0.05:
            print('The p_value of Bartlett Test is {0} and the data is suitable to apply factor analysis'.format(p_value))
            result1 = True
        else:
            print('The p_value of Bartlett Test is {0} and the data is not suitable to apply factor analysis'.format(p_value))
            result1 = False

        kmo_all,kmo_model=calculate_kmo(data_minmax)
        if kmo_model >= 0.6:
            print('The KMO value is {0} and the data is suitable to apply factor analysis'.format(kmo_model))
            result2 = True
        else:
            print('The KMO value is {0} and the data is not suitable to apply factor analysis'.format(kmo_model))
            result2 = False
        result = result1 or result2
        return result

    # 利用sklearn PCA确定因子个数，控制最大个数
    
    def factor_num_calc(self,threshold=0.8,max_factor_num=20):
        pca = PCA(threshold)
        data_minmax = self.data_preprocessing()
        pca.fit(data_minmax)
        n_components = pca.n_components_
        print('The number of principal components is at least {0} to ensure 80% explained variance ratio'.format(n_components))
        factor_num = min(n_components,max_factor_num)
        return factor_num
    
    

    ### 进行因子分析，并统计特征分类情况

    def variable_cluster(self,method='minres',rotation='varimax',threshold=0.8,max_factor_num=20): 
        data_minmax = self.data_preprocessing()
        print('Adequacy Test Result: \n')
        result = self.adequacy_test()
        print('\nDetermine the Number of Factors: \n')
        factor_num = self.factor_num_calc(threshold,max_factor_num) #确定因子个数

        fa = FactorAnalyzer(n_factors = factor_num, method = method, rotation=rotation)
        fa.fit(data_minmax) #因子分析

        factor_columns = [''.join(['group',str(i+1)]) for i in range(factor_num)]
        df_cm = pd.DataFrame(np.abs(fa.loadings_), columns=factor_columns)
        df_cm['factor_index'] = np.argmax(np.abs(fa.loadings_),axis=1) #根据因子载荷矩阵对特征分类

        return df_cm,factor_num

        ### 特征分类具体结果输出

    def feature_group(self,threshold=0.8,max_factor_num=20,n_col=4):
        df_cm,factor_num = self.variable_cluster(threshold=threshold,max_factor_num=max_factor_num)
        empty = 0
        feature_classify = {}
        for num in range(factor_num):
            content = df_cm[df_cm['factor_index']==num].index.tolist()
            rows = math.ceil(len(content)/n_col)
            if rows==0:
                empty += 1
                continue
            tmp = 0
            a = []
            for i in range(rows):   
                for j in range(n_col):
                    if tmp==len(content):
                        continue
                    a.append(content[tmp])
                    tmp += 1
                feature_classify[num+1-empty] = a
                if tmp==len(content):
                    break
        # 输出结果为dataframe
        feature_classify_df = pd.DataFrame()
        for k in feature_classify.keys():
            feature_classify_df = pd.concat([feature_classify_df,pd.DataFrame({k:feature_classify[k]})],axis=1)
        return feature_classify_df 


    # 生成lambda表达式，将连续变量粗分成约若干等份

    def gen_lambda_stability(self,binning,abnormal_values):
        temp = binning
        lambda_list = []
        for i in range(len(temp)):
            if i==0:
                lambda_list = 'lambda x: 0 if (x in %s) else %d if (x<=%f)'%(abnormal_values,temp.loc[i,'coarse_bin']+1,temp.loc[i,'ub'])
            elif i!=len(binning)-1:
                lambda_list = lambda_list + ' else %d if (x>%f) & (x<=%f)'%(temp.loc[i,'coarse_bin']+1,temp.loc[i,'lb'],temp.loc[i,'ub'])
            else:
                lambda_list = lambda_list + ' else %d if (x>%f) else np.nan'%(temp.loc[i,'coarse_bin']+1,temp.loc[i,'lb'])
        return lambda_list

    ##对于unique values>=5(可调整)的数值型变量，粗分成约5等份,异常值单独分箱

    def coarse_bin_stability(self,datevar,time_train,time_valid_start,time_valid_end,abnormal_values,bin_num=5):
        
        df_train=self.data[self.data[datevar]==time_train]
        df_valid=self.data[(self.data[datevar]>=time_valid_start)&(self.data[datevar]<=time_valid_end)]
        var_types = df_train.drop(self.exclude_cols,axis=1).dtypes.reset_index()
        var_types.columns = ['var','type'] #float64, int64, object
        numeric_column = var_types[(var_types['type']=='float64')|(var_types['type']=='int64')]['var'].tolist()
        exclude_cols_new = exclude_cols + var_types[var_types['type']=='object']['var'].tolist()
        df_train_coarse_bin = df_train[exclude_cols_new]
        df_valid_coarse_bin = df_valid[exclude_cols_new]
    #     coarse_bin_record = pd.DataFrame(columns=['var','coarse_bin','lb','ub']) ##记录各变量的binning区间
        for var in numeric_column: 
            if len(df_train[var].unique()) < bin_num:
    #             print('No coarse binning for numeric variable %s as its unique values is less than 10'%(var))
                df_train_value=list(df_train[var].unique())
                lambda_list_train=[]
                if len(df_train_value)==1:
                    lambda_list_train = 'lambda x: 0 if (x not in %s) else 1 if (x==%f) else np.nan'%(df_train_value,df_train_value[0])
                else:
                    for i in range(len(df_train_value)):
                        if i==0:
                            lambda_list_train = 'lambda x: 0 if (x not in %s) else %d if (x==%f)'%(df_train_value,i+1,df_train_value[i])
                        elif i!=len(df_train_value)-1:
                            lambda_list_train = lambda_list_train + ' else %d if (x==%f)'%(i+1,df_train_value[i])
                        else:
                            lambda_list_train = lambda_list_train + ' else %d if (x==%f) else np.nan'%(i+1,df_train_value[i])
                df_train_coarse_bin[var] = list(map(eval(lambda_list_train),df_train[var]))
                df_valid_coarse_bin[var] = list(map(eval(lambda_list_train),df_valid[var]))
            else:
                df_train_noabn=df_train[~df_train[var].isin(abnormal_values)]
                split_values = df_train_noabn[var].quantile(np.linspace(0.1,0.9,num=bin_num)).reset_index()[var].unique()
    #             print('Conduct coarse binning based on decile for numeric variable %s'%(var))
                binning = pd.DataFrame({'lb':[-99999]+split_values.tolist(),'ub':split_values.tolist()+[99999]}).reset_index()
                binning.rename(columns={'index':'coarse_bin'},inplace=True)
                binning['var'] = var
                binning = binning[['var','coarse_bin','lb','ub']]
    #             coarse_bin_record = pd.concat([coarse_bin_record,binning],ignore_index=True)
                lambda_list = self.gen_lambda_stability(binning,abnormal_values)
                df_train_coarse_bin[var] = list(map(eval(lambda_list),df_train[var]))
                df_valid_coarse_bin[var] = list(map(eval(lambda_list),df_valid[var]))
    #     return data_coarse_bin,coarse_bin_record
        return df_train_coarse_bin,df_valid_coarse_bin

    ##计算两个数据集的psi

    def calc_psi(self,datevar,time_train,time_valid_start,time_valid_end,abnormal_values,bin_num=5):
        df_train_coarse_bin,df_valid_coarse_bin=self.coarse_bin_stability(datevar,time_train,time_valid_start,time_valid_end,abnormal_values,bin_num)
        h=[]
        for col in df_train_coarse_bin.columns:
            if col not in self.exclude_cols:
                df_train_bin_cnt=df_train_coarse_bin.groupby(col).size().reset_index().rename(columns={col:'bin',0:'count1'})
                df_train_bin_cnt['countRatio1']=df_train_bin_cnt['count1']/(df_train_coarse_bin[col].count())
                df_valid_bin_cnt=df_valid_coarse_bin.groupby(col).size().reset_index().rename(columns={col:'bin',0:'count2'})
                df_valid_bin_cnt['countRatio2']=df_valid_bin_cnt['count2']/(df_valid_coarse_bin[col].count())
                binInfo=pd.merge(df_train_bin_cnt,df_valid_bin_cnt,on='bin',how='inner')
                psi = sum(binInfo.apply(CalcBinPSI, axis=1))
                col_psi=[col,psi]
                h.append(col_psi)
        return pd.DataFrame(h,columns=['feature','psi'])


    ##计算多个数据集的psi的统计指标：最大／最小／平均／标准差，总体psi 

    def calc_stat_psi(self,datevar,time_train,time_valid_start,time_valid_end,abnormal_values,bin_num=5):
        df_train=self.data[self.data[datevar]==time_train]
        df_valid=self.data[(self.data[datevar]>=time_valid_start)&(self.data[datevar]<=time_valid_end)]
        dp_psiinfo=pd.DataFrame(columns=['date','feature','psi'])
        datelist=list(df_valid[datevar].unique())
        for date_str in datelist:
            dp_day=self.calc_psi(datevar,time_train,date_str,date_str,abnormal_values,bin_num)
            dp_day['date']=date_str
            dp_psiinfo=dp_psiinfo.append(dp_day)
        dp_calcindex=dp_psiinfo.groupby('feature').agg({'psi':['max','min','mean','std']}).reset_index()
        psi_res=pd.DataFrame(columns=['feature','max_psi','min_psi','mean_psi','std_psi'])
        psi_res['feature']=dp_calcindex['feature']
        psi_res['max_psi']=dp_calcindex['psi']['max']
        psi_res['min_psi']=dp_calcindex['psi']['min']
        psi_res['mean_pi']=dp_calcindex['psi']['mean']
        psi_res['std_psi']=dp_calcindex['psi']['std']
        return psi_res

    ##结果合并

    def feature_stability(self,datevar,time_train,time_valid_start,time_valid_end,abnormal_values,bin_num=5):
        psi_all=self.calc_psi(datevar,time_train,time_valid_start,time_valid_end,abnormal_values,bin_num)
        psi_stat=self.calc_stat_psi(datevar,time_train,time_valid_start,time_valid_end,abnormal_values,bin_num)
        psi_res=pd.merge(psi_all,psi_stat,on='feature',how='inner')
        return psi_res