import os

import pandas as pd
from tqdm import tqdm

from loanpy.helpers import flatten
from loanpy.helpers import gensim_synonyms
from loanpy.helpers import gensim_similarity
from loanpy.helpers import loadvectors

def launch(L1="dfhun.csv", L2="dfgot.csv", L1inputcol="root", L2inputcol="adapt1", timelayer=["U","FU","Ug"]):
    
    os.chdir(os.path.dirname(os.path.abspath(__file__))+r"\data")
    
    global dfmatches
    dfmatches=pd.DataFrame(columns=[L2inputcol,"L1_idx"])
    global dfL2
    dfL2=pd.read_csv(L2,encoding="utf-8",usecols=[L2inputcol])
    dfL2=dfL2[dfL2[L2inputcol]!="too long"]
    dfL2=dfL2[dfL2[L2inputcol]!="wrong phonotactics"]
    dfL2[L2inputcol]=dfL2[L2inputcol].str.split(", ")
    dfL2=dfL2.explode(L2inputcol)

    global dfL1
    dfL1=pd.read_csv(L1,encoding="utf-8",usecols=[L1inputcol,"origin","year"])
    dfL1["ind"]=dfL1.index
    dfL1=dfL1[~dfL1[L1inputcol].str.contains("not old/from L2")] #exclude all fields that contain "not old or gothic" in the field "regexroot"
    if timelayer!="":
        dfL1=dfL1[dfL1["year"]<=sorted(list(set(dfL1[dfL1["origin"].isin(timelayer)]["year"])))[-1]].drop(["origin","year"],axis=1) #set timecap, drop rows below, drop cols
    
    global L2input
    L2input=L2inputcol

def findphoneticmatches(L1regexroot,index,L2inputcol): #index is the unambiguous key to all info in dfL1

    dftotal=dfL2
    dftotal["L1_idx"]=dftotal[L2inputcol].replace(L1regexroot,index,regex=True)
    dftotal=dftotal[dftotal.L1_idx.astype(str).str.isdigit()]
    global dfmatches
    dfmatches=dfmatches.append(dftotal[~dftotal.index.duplicated()])
      
def findloans(sheetname="new",L1="dfhun.csv",L2="dfgot.csv",L1inputcol="root",semantic_similarity=gensim_synonyms):
    #Invalid Excel character '[]:*?/\' in sheetname
    tqdm.pandas(desc="Searching for phonetic matches")
    dfL1.progress_apply(lambda x: findphoneticmatches(x[L1inputcol], x.ind, L2input), axis=1)

    global dfmatches #add cols for semantic_similarity()
    dfmatches=dfmatches.merge(pd.read_csv(L1,encoding="utf-8",usecols=["L1_pos","L1_en"]), left_on="L1_idx", right_index=True)
    dfmatches=dfmatches.merge(pd.read_csv(L2,encoding="utf-8",usecols=["L2_pos","L2_en"]), left_index=True, right_index=True)
    tqdm.pandas(desc="Calculating semantic similarity")
    dfmatches[semantic_similarity.__name__]=dfmatches.progress_apply(lambda x: gensim_synonyms(x.L1_en, x.L2_en, x.L1_pos, x.L2_pos), axis=1)
    dfmatches=dfmatches.sort_values(by=semantic_similarity.__name__,ascending=False).head(200000) #sort, cut off
    dfmatches = dfmatches.drop(["L1_pos","L1_en","L2_pos","L2_en"], axis=1)
    
    dfmatches=dfmatches.merge(pd.read_csv(L2,encoding="utf-8"), left_index=True, right_index=True)     #merge with original dataframes
    dfmatches=dfmatches.merge(pd.read_csv(L1,encoding="utf-8"), left_on="L1_idx", right_index=True)
    dfmatches=dfmatches.sort_values(by=semantic_similarity.__name__, ascending=False) #sort according to semantic similarity 
    dfmatches=dfmatches[:500] #cutoff
    
    writer = pd.ExcelWriter("results.xlsx", engine='xlsxwriter')
    dfdict = pd.read_excel("results.xlsx",sheet_name=None)  #read all the existing sheetes and make a dictionary of them
    dfdict[sheetname]=dfmatches #add dfmatches to the dictionary
    for sheet_name in dfdict.keys(): #write dictionary to results.xlsx
        dfdict[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()