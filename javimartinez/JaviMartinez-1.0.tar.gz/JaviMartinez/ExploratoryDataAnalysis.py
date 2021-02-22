import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pylab
import warnings
warnings.filterwarnings("ignore")

def all_functions():
    print("-sturges():\tColumn\n")
    print("-missing_data():\tdf, table, percentage, count, size\n")
    print("-value_counts():\tcolumn, table, percentage, count, size\n")
    print("-outliers():\tdf, variable, table, limits, method (std,IQR,IQR3)\n")
    print("-distribution_diag():\tdf, variable, size\n")
    print("-correlation():\tdf, variable\n")


def sturges(x):
    import numpy as np
    N=len(x)
    sturges=int(np.ceil(1+np.log2(N)))
    return sturges

def missing_data(df, table=True, percentage=False, count=False, size=(10,6)):
    
    total=df.isna().sum().sort_values(ascending=False)
    percent=df.isna().mean().sort_values(ascending=False)*100
    final=pd.concat([total, percent], axis=1, keys=['Total','Percent'])
    
    if(percentage):
        plt.figure(figsize=size)
        fig=final.Percent.plot.bar()
        plt.title("Missing Data Percentage",fontsize=20)
        plt.ylabel("Percentage",fontsize=15)
        plt.xlabel("Columns",fontsize=15)
        fig.axhline(y=5, color='red')
        plt.xticks(fontsize=14)
    
    
    
    if(count):
        plt.figure(figsize=size)
        fig=final.Total.plot.bar()
        plt.title("Total Missing Data",fontsize=20)
        plt.ylabel("Missing Data",fontsize=15)
        plt.xlabel("Columns",fontsize=15)
        plt.xticks(fontsize=14)
        
    if(table==True):
        return final


def value_counts(column, table=True, percentage=False, count=False, size=(10,6)):
    
    total=column.value_counts()
    percent=column.value_counts()/len(column)*100
    final=pd.concat([total, percent], axis=1, keys=['Total','Percent'])
    
    if(percentage):
        plt.figure(figsize=size)
        fig=final.Percent.plot.bar()
        plt.title("Percentage of values",fontsize=20)
        plt.ylabel("Percentage",fontsize=15)
        fig.axhline(y=5, color='red')
        plt.xticks(fontsize=14)
    
    
    
    if(count):
        plt.figure(figsize=size)
        fig=final.Total.plot.bar()
        plt.title("Value count",fontsize=20)
        plt.ylabel("Count",fontsize=15)
        plt.xticks(fontsize=14)
        
    if(table==True):
        return final


def outliers(df, variable, method='IQR', limits=True, table=False):
    if(method=='std'):
        upper_boundary = df[variable].mean() + 3 * df[variable].std()
        lower_boundary = df[variable].mean() - 3 * df[variable].std()
        if(limits):
            print("MIN: {}\nMAX: {}".format(lower_boundary,upper_boundary))
        if(table):
            outliers=df.loc[(df[variable]<lower_boundary)|(df[variable]>upper_boundary),]
            return outliers
    
    if(method=='IQR'):
        IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)
        lower_boundary = df[variable].quantile(0.25) - (IQR * 1.5)
        upper_boundary = df[variable].quantile(0.75) + (IQR * 1.5)
        if(limits):
            print("MIN: {}\nMAX: {}".format(lower_boundary,upper_boundary))
        if(table):
            outliers=df.loc[(df[variable]<lower_boundary)|(df[variable]>upper_boundary),]
            return outliers
    
    if(method=='IQR3'):
        IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)
        lower_boundary = df[variable].quantile(0.25) - (IQR * 3)
        upper_boundary = df[variable].quantile(0.75) + (IQR * 3)
        if(limits):
            print("MIN: {}\nMAX: {}".format(lower_boundary,upper_boundary))
        if(table):
            outliers=df.loc[(df[variable]<lower_boundary)|(df[variable]>upper_boundary),]
            return outliers
    

def distribution_diag(df, variable, size=(20,5)):
    plt.figure(figsize=size)

    plt.subplot(1, 3, 1)
    sns.distplot(df[variable], bins=sturges(df[variable]))
    mean=df[variable].mean()
    median=df[variable].median()
    plt.axvline(mean, color='r', linestyle='dashed',alpha=0.4)
    plt.axvline(median, color='k', linestyle='dashed',alpha=0.4)
    plt.title('Histogram')

    plt.subplot(1, 3, 2)
    stats.probplot(df[variable], dist="norm", plot=plt)
    plt.ylabel('{} quantiles'.format(variable))
    plt.title('Probability Plot')

    plt.subplot(1, 3, 3)
    sns.boxplot(y=df[variable])
    plt.title('Boxplot')

    plt.show


def correlation(df,variable):
    corr=df.corr()
    x=corr[[variable]].sort_values(by=variable,ascending=False)\
    .style.background_gradient()
    return x


def corr_plot(x):
    corr=x.corr()
    mask = np.triu(np.ones_like(corr, dtype=np.bool))
    f, ax = plt.subplots(figsize=(12,6))
    cmap = sns.color_palette("PRGn",10)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1,vmin=-1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5},annot=True)
    plt.show()

