#################################
# Copyright 2020 OTICS Advanced Analytics Inc.
############################################

import numpy as np
import pandas as pd
import numpy as np
from scipy import stats
import numpy_indexed as npi
import sys
import math
from functools import reduce
from itertools import chain
import csv
from scipy.stats import kstest, norm
from statsmodels.stats.diagnostic import lilliefors
import random
import maads
import json
import ast
#from statsmodels.stats import shapiro
#from scipy import stats

#import plot

def getdata(idxall,df,cols,filename,headers):
    maindata=[]

    rows=0
    with open(filename, 'w') as myfile:
      # write headers
      rb=[] 
      for h in headers:
          rb.append(h)
      buf=",".join(rb)    
      myfile.write(buf + "\n")
      
          
      for idx in idxall:
        rb=[]      
        for c in range(cols):
          d=df.iloc[idx,c]
          rb.append(d)
       # print(rb)  
        buf=','.join(map(str, rb)) 
      #  print(buf)
        myfile.write(buf + "\n")
        rows+=1

      return rows

def balancebigdata(csvpath,numbins,maxrows,tofile,bincutoff,distcutoff,skipcols=0):
        binsarr=list()
        colind=0
        bucketlist=[]

        try:
          df=pd.read_csv(csvpath)
          df=df.drop_duplicates()
        except Exception as e:
          print("ERROR: reading file: %s" % e)
          return

        headers = df.columns
        bestvars=[]
        vardetails=[]
        countallocv=[]
        countsv=[]
        lmv=[]
        countalloc=[]
        binsv=[]

#        print(headers)

 #       print(len(df))
        jbuf=""
        for column in df:
          if colind>skipcols-1: # skip col=0   
              try:    
                cols=df[column].drop_duplicates().to_numpy()
                cnts, bins = np.histogram(cols, bins=numbins)
                bins=[round(b,3) for b in bins]
                ind = np.digitize(cols, bins)
                stat,bincut,distcut,mybins,share,cntsv,means,lm=countnumbuckets(ind,column,bins,bincutoff,numbins,cnts,distcutoff)
                #print("share:",share)
                sharearr=[round(s,3) for s in share]
              #  jbuf=column+":{'CountAllocation':"+str(sharearr) + "},{'Counts':"+str(cntsv)+"},{'Lilliefors-Statistics':"+str(round(lm[0],3))+'}'
                countallocv="CountAlloc:"+str(list(sharearr))
                countsv="BinCounts:"+str(list(cntsv))
                lmv="Lilliefors:"+str(round(lm[0],3))
                binsv="Bins:"+str(list(mybins))
                
                vardetails.append([column,countsv,countallocv,binsv,lmv]) 
                if stat==1:
                  d=equal_bin(cols,numbins,cnts,bins,ind)
                  bucketlist.append(d)
                  bestvars.append([column,bincut,distcut])
              except Exception as e:
                print("ERROR: reading columns: %s" % e)
                continue
              
          colind+=1
        try:
          idx,lil,mk=mergelists(bucketlist,numbins,maxrows)
        except Exception as e:
          print("ERROR: merging lists: %s" % e)
          return
        try:
        #  print(vardetails)  
          rc=getdata(mk,df,colind,tofile,headers)
       #   jbuf+="]"
          jsonstr=str({'Bins':list(bins), 'OptimizedCounts':list(idx),'OriginalCounts':list(cnts),'Lilliefors-Statistic':round(lil[0],3),'Numbins':numbins+1,
                       'Maxrows':maxrows,'Bincutoff':bincutoff,\
              'Distcutoff':distcutoff,'OriginalDataSize':len(df),'BalancedDataSize':rc,'BestVariables':bestvars,'InputFile':csvpath,'OutputFile':tofile,
                       'VariableDetails':vardetails})

          json_string = json.dumps(ast.literal_eval(jsonstr))
          print(json_string, "\nFile Output Complete")
        except Exception as e:
          print("ERROR: analysing data : %s" % e)
          return
        

# see which variables have the best distribution of buckets
def getlillie(share):
    return lilliefors(share)

def countnumbuckets(inds,colname,bins,bincutoff,numbins,cnts,distcutoff):
        np.set_printoptions(threshold=sys.maxsize)

     #   print(colname,inds)
        mybins = list(set(inds))
        thresh=len(mybins)/(numbins+1)
        share=cnts/sum(cnts)

        means=sum(share)/len(share)
        lm=getlillie(share)
        
        #print(mybins)
        #print(share)
        #print(cnts)

        #print(means)
        #print(lm)
        
        if thresh >= bincutoff and lm[0]<=distcutoff:
                return 1,round(thresh,3),round(lm[0],3),mybins,share,cnts,means,lm
        else:
             #   print("Bad bins:",mybins,colname,len(mybins),thresh,cnts,share,means)
                return 0,round(thresh,3),round(lm[0],3),mybins,share,cnts,means,lm


def getrowsfrombuckets(drows,mpall):
        a=1
        mk=[]
        #print(len(drows),len(mpall))
        for r,m in zip(drows,mpall):
             #print(m)   
             mk+=random.sample(m, r)
             #mk.append(val)
        ms=set(mk)     
        return ms
                
        
def equal_bin(data, numbins,cnts,bins,out):
   np.set_printoptions(threshold=sys.maxsize)   
    # parameter q specifies the number of bins
#   out,bins = pd.cut(data, q, labels=False, retbins=True, right=False)
#   print(out) # contains bin indices for data
#   print("Orginal:",obins,cnt/len(out))
   totdata=[]
  # totdatall=[]
   bucketindexes=[]
   arrindices=[]
   d=[]


   #get indices of data in buckets
   k=0            
   for i in out:
       bucketindexes.append([k,i])
       k+=1

   #print(bucketindexes)
   d=[]
   d2=[]
   bc=1# bucket count
   for nb in range(numbins+1):
     totitems=0
     barr=[]
    # print("NB:",nb,bc)
     for ir in bucketindexes:
#        if totitems<nb and bc==ir[1]:
#        print(ir)
        if bc==ir[1]:
          barr.append(ir[0])    
          totitems+=1 
     bc+=1
     d.append(barr)

 #  print("BARR DATA:",bc)
#   print(len(d))
  
   return d  

def merge(lsts):
    sets = [set(lst) for lst in lsts if lst]
    merged = True
    while merged:
        merged = False
        results = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = True
                    common |= x
            results.append(common)
        sets = results
    return list(sets[0])

def mergelists(dall,numbins,maxrows):
   mainlist=[]
   mlist=[]
   mainmp=[]
   mpall=[]
   mpallset=[]
   dlens=[]
   dlenshare=[]
   drows=[]
   for i in range(numbins+1):
     d=[]      
#     mpallset=[]
#     dlens=[]
     dlenshare=[]
     for di in dall: #list of variables-each variable has buckets
         #d.append(set(di[i]))
         d+=set(di[i])  #merge it
     mp=set(d)
     mpall+=mp
     mpallset.append(mp)
     dlens.append(len(mp))
     mainmp.append(mp)
   dlenshare=[d/sum(dlens) for d in dlens]
   drows=[int(dr*maxrows) for dr in dlenshare ]
   mk=getrowsfrombuckets(drows,mpallset)
   sharemk=[m/sum(mk) for m in mk]
   lil=getlillie(sharemk)
   
   
   return drows,lil,mk
        
def intersect(dall,numbins,maxrows):

#   len(dall)
   mainlist=[]
   for i in range(numbins+1):
     d=[]      
     for di in dall: #list of variables-each variable has buckets
         d.append(di[i])

     mp=list(set(chain.from_iterable(d)))
     mainlist.append(mp)
   mk=list(reduce(set.intersection, [set(item) for item in mainlist ]))

   return mk


#csvp="C:\MAADS\Companies\Precision Drilling\PoC\Data\decision2_cleanholetime\cleanholetimeD2training.csv"
#tofile1="C:\MAADS\Companies\Precision Drilling\PoC\Data\decision2_cleanholetime\cleanholetimeD2trainingoptimized.csv"

#csvp="C:\MAADS\Companies\Precision Drilling\PoC\Data\decision2_cleanholetime\cleanholeD2training2.csv"
#csvp="C:\\MAADS\\Companies\\Precision Drilling\\PoC\\Data\\decision3_backream\\backreamstandD3training.csv"
#tofile="C:\\MAADS\\Companies\\Precision Drilling\\PoC\\Data\\decision3_backream\\backreamstandD3trainingoptimized.csv"

csvp2="C:\\MAADS\\Companies\\Precision Drilling\\PoC\\Data\\decision4a_stickslip\\backreamD4Atraining.csv"
tofile2="C:\\MAADS\\Companies\\Precision Drilling\\PoC\\Data\\decision4a_stickslip\\backreamD4Atrainingoptimized.csv"

bincutoff=.7
distcutoff=.5
numbins=10
#balancebigdata(csvp2,numbins,2000,tofile2,bincutoff,distcutoff,1)


#maads.balancebigdata(csvp2,numbins,2000,tofile2,bincutoff,distcutoff,1)



