# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Decomposition analysis of Profile data (DePro)

@author: tadahaya
"""
import pandas as pd
import numpy as np
from copy import deepcopy

from .data import Data
from .preprocess.preprocessor import PreProcess,DEG
from .estimator.estimator import Estimator
from .decomposer.decomposer import Decomposer
from .decomposer.ex_decomposer import ExDecomposer
from .plot.plot import RadarChart

# organizer
class Depro():
    def __init__(self):
        self.data = Data()
        self.__prep = PreProcess()
        self.__deg = DEG()
        self.__estr = Estimator()
        self.__deco = Decomposer()
        self.__xdeco = ExDecomposer()

    ### data control ###
    def set_data(self,data):
        """ set a data to be analyzed """
        self.data.set_data(data)

    def get_data(self):
        """ get data """
        return self.data.get_data()

    def get_processed(self):
        """ get processed data """
        return self.data.get_processed()

    def get_decomposed(self):
        """ get processed data """
        return self.data.get_decomposed()

    def get_state(self,show=False):
        """ get states of analysis """
        dic = self.data.get_state()
        if show:
            for k,v in dic.items():
                print("{0}: {1}".format(k,v))
        return dic

    ### preprocessing ###
    def preprocess(self,mirror=True,alpha=0.05,sphere=True,**kwargs):
        """
        data preprocessing

        Parameters
        ----------
        mirror: boolean
            indicate whether mirror data is employed
            for setting the centroid of novel space to the data origin

        alpha: float
            indicate SG test criteria

        show: boolean
            whether details are shown or not

        sphere: boolean
            whether normalization of samples with L2 norm

        """
        data = self.data.get_data()
        X = data["X"]
        Xpro = self.__prep.preprocess(X,mirror=mirror,sphere=sphere,alpha=alpha,**kwargs)
        self.data.set_processed("X",Xpro)
        if mirror:
            self.data.update_state(key="mirror",value=True)
            outs = self.__prep.get_outliers()
            self.data.set_processed("outlier",outs)
            if len(outs) > 0:
                print(">> {} samples below are excluded from the mirror".format(len(outs)))
                samples = data["columns"]
                for v in outs:
                    print("- {}".format(samples[v]))
        else:
            self.data.update_state(key="mirror",value=False)
        if sphere:
            self.data.update_state(key="sphere",value=True)
        else:
            self.data.update_state(key="sphere",value=False)


    ### estimate the factor No. ###
    def estimate(self,method="parallel",scree_plot=False,**kwargs):
        """
        data preprocessing

        Parameters
        ----------
        method: str
            indicate the estimation method for determining the No. of important factors
            "accumulation", "parallel", "smc", or "map"
            note that "smc" is a quite heavy process

        """
        X = self.data.get_data()["X"] # in estimation, z is simply calculated from raw without considering mirror  
        sphere = self.get_state()["sphere"]
        if sphere:
            X = X/self.data.get_data()["ts"]
        if method=="parallel":
            self.__estr.to_parallel()
            self.data.update_state(key="estimator",value="parallel")
            Z = X.T
        elif method=="smc":
            self.__estr.to_smc()
            self.data.update_state(key="estimator",value="smc")
            Z = _normal(X.T)
        elif method=="map":
            self.__estr.to_map()
            self.data.update_state(key="estimator",value="map")
            Z = _normal(X.T)
        elif method=="accumulation":
            self.__estr.to_accumulation()
            self.data.update_state(key="estimator",value="accumulation")
            Z = X.T
        else:
            raise KeyError("!! Wrong method: choose 'accumulation', 'parallel', 'smc', 'mapc', or 'accumulation' !!")
        nfactor = self.__estr.get_nfactor(Z,**kwargs)
        self.data.set_nfactor(nfactor)
        if scree_plot:
            try:
                self.__estr.scree_plot(**kwargs)
            except NotImplementedError:
                pass
        return nfactor


    ### decomposition ###
    def decompose(self,initialize="principal_component",rotate="varimax",nfactor=None,**kwargs):
        """
        calculation

        Parameters
        ----------
        initialize: str
            indicate the initial method for preparing factors
            "principal_component"

        rotation: str
            indicate the rotation method for reducing the features consisting axes
            "varimax" or "optimax"
            "", False, or None means no rotation (equals to conventional PCA)
        
        """
        ### initialize
        if initialize=="principal_component":
            self.__deco.to_pc()
            self.data.update_state(key="initializer",value="principal_component")
        else:
            raise KeyError("!! Wrong method: choose 'principal_component' !!")

        ### rotate
        if rotate=="varimax":
            self.__deco.to_varimax()
            self.data.update_state(key="rotator",value="varimax")
            rotate = True
        elif rotate=="promax":
            raise NotImplementedError
            # self.__deco.to_promax()
            # self.data.update_state(key="rotator",value="promax")
            # rotate = True
        else:
            print("!! No rotation: indicate 'varimax' or 'promax' when rotation is necessary !!")
            rotate = False
            self.data.update_state(key="rotator",value=None)
        X = self.data.get_processed()["X"]
        if nfactor is None:
            nfactor = self.data.get_nfactor()
        L,F,C = self.__deco.decompose(data=X,nfactor=nfactor,rotate=rotate,**kwargs)
        state = self.get_state()
        if state["mirror"]:
            d = self.data.get_data()
            X = d["X"]
            nsample = X.shape[1]
            L = L[:,:nsample]
            C = C[:nsample]
            if state["sphere"]:
                ts = d["ts"]
                X = X/ts
            F = L.T.dot(X)
        label = _prep_label(F.shape[1],len(C))
        L = pd.DataFrame(L,index=self.data.data["index"],columns=label)
        F = pd.DataFrame(F,index=label,columns=self.data.data["columns"])
        self.data.set_decomposed("loading",L)
        self.data.set_decomposed("fscore",F)
        self.data.set_decomposed("contribution",C)
        return L,F,C


    def _logical_conf(self):
        """ reconstruct data for confirmation of calculation """
        deco = self.data.get_decomposed()
        raw = self.data.get_data()
        pro = self.data.get_processed()
        L = deco["loading"].values
        F = deco["fscore"].values
        ts = deco["ts"]
        state = self.get_state()
        if state["rotator"] is None:
            centroid = np.c_[np.mean(pro["X"],axis=1)]
            recX = L.dot(F) + centroid
        elif state["rotator"]=="promax":
            raise NotImplementedError
        else:
            recX = L.dot(F)
            if not state["mirror"]:
                centroid = np.c_[np.mean(pro["X"],axis=1)]
                recX = recX + centroid
        if state["sphere"]:
            recX = recX.dot(np.diag(ts))
        del deco,L,F,ts,pro
        rec = pd.DataFrame(recX,index=raw["index"],columns=raw["columns"])
        rdata = pd.DataFrame(raw["X"],index=raw["index"],columns=raw["columns"])
        return rec,rdata


    ### decomposition of external data ###
    def prep_deg(self,data,**kwargs):
        """
        convert dataframe into dict of tags

        Parameters
        ----------
        data: dataframe
            feature x sample matrix
            In the default setting, log2 expression matrix is assumed
            If the data is already response profiles, use raw=False option

        fold: float
            determine threshold of outliers

        method: str
            "std" or "iqr"

        nmin,nmax: int
            indicate the minimum and maximum No. of genes in each tag
        
        raw: boolean
            indicates whether raw data is set or not
            if True, the data will be converted before tag making

        sep: str, default "_"
            separator for sample name
            
        position: int, default 0
            indicates position of sample name such as drug

        control: str
            indicates the control column name

        """
        idx = list(data.index)
        if self.data.decomposed["loading"] is not None:
            temp = list(self.data.decomposed["loading"].index)
            idx = sorted(list(set(idx) & set(temp)))
        elif self.data.data["index"] is not None:
            temp = self.data.data["index"]
            idx = sorted(list(set(idx) & set(temp)))
        else:
            print("!! CAUTION: DEG preparation is done without merging reference data !!")
        data = data.loc[idx,:]
        return self.__deg.func(data,**kwargs)


    def decompose_ex(self,deg=dict(),loading=None,**kwargs):
        """
        decompose the external data based on decomposed effects
        
        Parameters
        ----------
        deg: dict
            a dictionary like {term:tuples of up/down tags}
            the terms correspond to chemicals of interest

        trim: boolean
            whether loading is trimmed based on the indicated key

        key: str
            indicates the keyword for trimming

        species: str
            indicates the species to be analyzed

        """
        if len(deg.keys())==0:
            raise ValueError("!! Indicate DEG to be analyzed !!")
        if loading is None:
            self.__xdeco.set_loading(self.get_decomposed()["loading"],**kwargs)
        else:
            self.__xdeco.set_loading(loading,**kwargs)
        self.__xdeco.set_deg(deg)
        res = self.__xdeco.decompose()
        return res


    ### visualization ###
    def plot(self,score=None,focus=[],absolute=False,overlay=False,color="mediumblue",
             n_labeled=None,plot_all=False,figsize=None,savefig="",dpi=100,**kwargs):
        """
        plot scores as a radarchart
        
        Parameters
        ----------
        score: dataframe
            data to be visualized (contracted x samples)
            Both results of decompose() and decompose_ex() can be applied

        absolute: boolean
            indicates whether data is converted into absolute values before visualization

        focus: list
            a list of sample names to be visualized

        overlay: boolean
            whether plots are overlaid or not

        color: str or list
            indicates the color of plot

        n_labeled: int
            indicates the No. of labels to be plotted

        plot_all: boolean
            whether all samples are visualized or not

        limit: tuple
            determine min and max values of plot: (min,max)
        
        color: str
            determine the color of plot
        
        figsize: tupple
            determine figsize
        
        markersize: int
            determine size of markers
            
        labelsize: int
            determine size of axis-labels
            
        ticksize: int
            deterimne font size of polar axis
                        
        axes_label: boolean
            whether labels of axes are neeeded
        
        alpha: float, default 0.25
            indicates transparency
            
        savefig: str
            path for exported file
            
        """    
        if score is None:
            raise ValueError("!! Indicate score such as responase score !!")
        if len(focus)==0:
            focus = list(score.columns)
            if len(focus) > 10:
                if plot_all==False:
                    raise ValueError("!! Too many samples: turn on plot_all to plot all data !!")
        feature = list(score.index)
        abs_score = np.abs(score)
        if absolute:
            score = abs_score
        if overlay:
            if type(color)!=list:
                color = []
            dat = RadarChart()
            axes = []
            for i,f in enumerate(focus):
                if len(color)==0:
                    color = [""]*len(focus)
                else:
                    div,mod = divmod(len(focus),len(color))
                    color = color*div + color[:mod]
                temp = score[f].values
                temp2 = abs_score[f].sort_values(ascending=False)
                if n_labeled is None:
                    l2d = dat.plot(values=temp,features=feature,label=f,color=color[i],**kwargs)
                else:
                    shown = list(temp2.index)[:n_labeled]
                    feature2 = [v if v in shown else "" for v in feature]
                    l2d = dat.plot(values=temp,features=feature2,label=f,color=color[i],**kwargs)
                axes.append(l2d)
            dat.close(savefig=savefig,dpi=dpi,handles=axes,labels=focus)
        else:
            if type(color)!=str:
                raise TypeError("!! Color should be string when overlay is False !!")
            for f in focus:
                if figsize is None:                
                    figsize = (4,6) # hard coding to align the sizes of plots
                dat = RadarChart(figsize=figsize)
                temp = score[f].values
                temp2 = abs_score[f].sort_values(ascending=False)
                if n_labeled is None:
                    dat.plot(values=temp,features=feature,label=f,color=color,**kwargs)
                else:
                    shown = list(temp2.index)[:n_labeled]
                    feature2 = [v if v in shown else "" for v in feature]
                    dat.plot(values=temp,features=feature2,label=f,color=color,**kwargs)
                dat.close(savefig,dpi)


def _normal(X):
    return (X - np.mean(X,axis=0))/np.std(X,axis=0)


def _prep_label(n_total,n_focus):
    label = []
    ap = label.append
    for i in range(n_total):
        if i < n_focus:
            ap("P{}V".format(i + 1))
        else:
            ap("P{}".format(i + 1))
    return label


