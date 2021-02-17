import pandas as pd
import numpy as np
import copy
from collections import Counter, defaultdict
import time
import scipy.stats as stats
from astropy.stats import bayesian_blocks
import sys


def Read_sample():
    url = 'https://raw.githubusercontent.com/matnado/TemporalBackbone/main/TemporalBackbone/Sample.csv'
    return pd.read_csv(url, error_bad_lines=False)

def Temporal_Backbone(dataold, I_min = 60.*60.*24., is_directed=True, Bonferroni = True, alpha = 0.01):
    '''
    Find the backbone in temporal networks where node vary their properties over time. 
    The methodology is first introduced in 
    Nadini, M., Bongiorno, C., Rizzo, A., & Porfiri, M. (2020). Detecting network backbones against time variations in node properties. Nonlinear Dynamics, 99(1), 855-878.
    
    Then was deemed as appropriate for large temporal networks, having a good trade-off between false positives and false negatives. See
    Nadini, M., Rizzo, A., & Porfiri, M. (2020). Reconstructing irreducible links in temporal networks: which tool to choose depends on the network size. Journal of Physics: Complexity, 1(1), 015001.
    
    For sparse networks, the computational time is O(N_E T^2), where N_E are the number unique edges in the network and T the number of time steps.
    For sparse networks (like most of the large networks), the computational time is O(N T^2)
    
    Input: 
    - pandas dataframe with three columns (order is important): node1, node2, time
    - Minimum length of the interval (time step is taken from the data): default 1 day
    - whether the network is directed or not: default True
    - whether to use the Bonferroni correction: default True
    - threshold to determine the significance of a link: default 0.01
    
    Output:
    - list with the significant links    
    '''
    
    data = copy.deepcopy(dataold)
    
    labels = data.columns# first index is node1, second node2, and third time
    if len(labels)>3:
        sys.exit('Make sure that the order of the pandas dataframe is\n node1, node2, and time\n')
    
    data = transform_time(data, labels, I_min)
    
    if is_directed==True: return compute_weEADM_directed(data, labels, alpha, Bonferroni)
    else: return compute_weEADM_undirected(data, labels, alpha, Bonferroni)

def Bayesian(time): 
    '''
    Find the interval partition
    '''
    I = bayesian_blocks(time, p0=0.01) #Interval partition
    I = np.ceil(I).astype(int)
    Intervals = list(zip(I[:-1],I[1:]) )
    if Intervals[-1][0]==Intervals[-1][1]:
        del Intervals[-1]
    I_number = len(Intervals)
    Intervals_list = [interval[0] for interval in Intervals]+[Intervals[-1][1]]
    return Intervals_list, I_number


def filter_links(alpha, Bonferroni, weEADM, observed_weight):
    '''
    Filter links according to the null model. 
    Links with only one interaction are automatically discarded because they cannot be significant
    '''
    observed_weight_reduced, weEADM_reduced = {}, {}
    for i,j in observed_weight:
        if observed_weight[i,j]>1: 
            observed_weight_reduced[i,j], weEADM_reduced[i,j] = observed_weight[i,j], weEADM[i,j]

    if Bonferroni==True:
        nl = len(weEADM)
        thr = alpha/nl
    else: thr = alpha
        
    return [(i,j) for i,j in weEADM_reduced if stats.poisson.sf(observed_weight_reduced[i,j]-1,weEADM_reduced[i,j])<thr]


def compute_weEADM_directed(data, labels, alpha, Bonferroni):
    '''
    Find backbone in directed network
    '''
    weEADM = {}#expected weigth according to the null model
    observed_weight = {}
    
    Intervals_list, I_number = Bayesian(data[labels[2]].to_list())

    observed_weight = data.groupby([labels[0], labels[1]])[labels[2]].count().to_dict()
    weEADM = {(source,dest):0. for source,dest in observed_weight}
    
    data['bins'] = pd.cut(data[labels[2]], bins=Intervals_list)
    tot_links = data.groupby(['bins'])[labels[2]].count().to_dict()
    out_strength_nodes = data[['bins', labels[0]]].groupby(['bins'])[labels[0]].apply(lambda x:list(x)).to_dict()
    in_strength_nodes=data[['bins',labels[1]]].groupby(['bins'])[labels[1]].apply(lambda x:list(x)).to_dict()
    
    for interval in tot_links:
        edges = {}
        dict_out_strength, dict_in_strength = Counter(out_strength_nodes[interval]), Counter(in_strength_nodes[interval])
        for i in range(len(out_strength_nodes[interval])):
            edges[(out_strength_nodes[interval][i], in_strength_nodes[interval][i])]=None
            
        for (source, dest) in edges:
            weEADM[(source,dest)] += (dict_out_strength[source]*dict_in_strength[dest])/float(tot_links[interval])
    
    return filter_links(alpha, Bonferroni, weEADM, observed_weight) 


def compute_weEADM_undirected(data, labels, alpha, Bonferroni):
    '''
    Find backbone in undirected network
    '''
    
    weEADM = {}#expected weigth according to the null model
    observed_weight = {}
    
    Intervals_list, I_number = Bayesian(data[labels[2]].to_list())

    observed_weight = data.groupby([labels[0], labels[1]])[labels[2]].count().to_dict()
    weEADM = {(source,dest):0. for source,dest in observed_weight}
    
    data['bins'] = pd.cut(data[labels[2]], bins=Intervals_list)
    tot_links = data.groupby(['bins'])[labels[2]].count().to_dict()
    strength_nodes = data[['bins', labels[0]]].groupby(['bins'])[labels[0]].apply(lambda x:list(x)).to_dict()
    supp = data[['bins',labels[1]]].groupby(['bins'])[labels[1]].apply(lambda x:list(x)).to_dict()
    
    for interval in tot_links:
        edges = {}
        for i in range(len(strength_nodes[interval])):
            if strength_nodes[interval][i]<supp[interval][i]: edges[(strength_nodes[interval][i], supp[interval][i])]=None
            else: edges[(supp[interval][i], strength_nodes[interval][i])]=None
                
        strength_nodes[interval]+=supp[interval]
        dict_strength = Counter(strength_nodes[interval])
            
        for (source, dest) in edges:
            weEADM[(source,dest)] += (dict_strength[source]*dict_strength[dest])/float(2*tot_links[interval])
    
    return filter_links(alpha, Bonferroni, weEADM, observed_weight) 


def transform_time(data, labels, I_min):
    '''
    Transform the time series in time steps of equal length. 
    '''
    
    try:
        dtype = data[labels[2]].unique().dtype
        data[labels[2]] = pd.to_datetime(data[labels[2]],unit=dtype)#[0].timestamp()
        data[labels[2]] = [time.timestamp() for time in data[labels[2]].to_list()]
    except:
        print('Time is assumed to be in seconds\n')
        
    min_time = np.min(data[labels[2]])-I_min/2.
    data[labels[2]] = data[labels[2]]-min_time
    data[labels[2]] = data[labels[2]]/I_min
    data[labels[2]] = data[labels[2]].astype(int)  
    return data