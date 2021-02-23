# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Estimator o-- EstPlot

@author: tadahaya

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# abstract class
class EstPlot():
    def __init__(self):
        pass

    def plot(self):
        raise NotImplementedError        

# concrete class
class ScreePlot(EstPlot):
    def plot(self,true_contr,rand_contr,fontsize=12,color="royalblue",markersize=8,
             linewidth=2,xlabel="factors",ylabel="eigen value",title="",
             focus=5,fileout="",dpi=100,figsize=(),**kwargs):
        """
        visualize a result of parallel analysis

        Parameters
        ----------
        res: dataframe
            a result file of enrichment analysis
            
        """
        x = np.arange(1,len(true_contr) + 1,1).astype(int)
        if len(figsize) > 0:
            fig = plt.figure(figsize=figsize)
        else:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        if len(xlabel) > 0:
            ax.set_xlabel(xlabel,fontsize=fontsize)
        if len(ylabel) > 0:
            ax.set_ylabel(ylabel,fontsize=fontsize)
        if len(title) > 0:
            ax.set_title(title,fontsize=fontsize)
        ax.tick_params(labelsize=fontsize)
        if len(rand_contr)!=0:
            ax.plot(x,rand_contr,marker="o",markersize=markersize,
                    linewidth=linewidth,color="grey",markerfacecolor="grey",
                    markeredgecolor="grey",label="null")
        ax.plot(x,true_contr,marker="o",markersize=markersize,
                linewidth=linewidth,color=color,markerfacecolor=color,
                markeredgecolor=color,label="data")
        ax.legend(loc="best",fontsize=fontsize)
        if len(fileout) > 0:
            plt.savefig(fileout,bbox_inches="tight",dpi=dpi)
        plt.tight_layout()
        plt.show()


# concrete class
class AccPlot(EstPlot):
    def plot(self,contribution,nfactor=None,fontsize=12,color="royalblue",markersize=8,
             linewidth=2,xlabel="factors",ylabel="cumulative contribution",title="",
             focus=5,fileout="",dpi=100,figsize=(),**kwargs):
        """
        visualize cumulative contribution
            
        """
        x = np.arange(1,len(contribution) + 1,1).astype(int)
        total_contr = np.sum(contribution)
        contribution = contribution/total_contr
        acc = 0.0
        y = []
        for v in contribution:
            acc += v
            y.append(acc)
        if len(figsize) > 0:
            fig = plt.figure(figsize=figsize)
        else:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        if len(xlabel) > 0:
            ax.set_xlabel(xlabel,fontsize=fontsize)
        if len(ylabel) > 0:
            ax.set_ylabel(ylabel,fontsize=fontsize)
        if len(title) > 0:
            ax.set_title(title,fontsize=fontsize)
        ax.tick_params(labelsize=fontsize)
        ax.plot(x,y,marker="o",markersize=markersize,
                linewidth=linewidth,color=color,markerfacecolor=color,
                markeredgecolor=color,label="contribution")
        if nfactor is not None:
            ax.vlines(nfactor,min(y),max(y),linestyle='dashed',linewidth=linewidth,
                      color="grey",label="nfactor: {}".format(nfactor))
        ax.legend(loc="best",fontsize=fontsize)
        if len(fileout) > 0:
            plt.savefig(fileout,bbox_inches="tight",dpi=dpi)
        plt.tight_layout()
        plt.show()
