import ast
import os
from itertools import combinations
from itertools import product
from collections import defaultdict
from itertools import count
from itertools import product

import pandas as pd
from lingpy import ipa2tokens
import Levenshtein as ld

from loanpy.helpers import applyfunc2col
from loanpy.helpers import flatten
from loanpy.helpers import ipa2clusters
from loanpy.helpers import word2struc
from loanpy.helpers import editdistancewith2ops

def launch(dfetymology="dfetymology.csv",timelayer="",substituteclusters="substidict.txt",L2="dfgot.csv",substitutephons="substi.csv"):

    os.chdir(os.path.dirname(os.path.abspath(__file__))+r"\data")
    
    global dfety
    dfety=pd.read_csv(dfetymology,encoding="utf-8")
    if timelayer != "":
        dfety=dfety[dfety.Lan==timelayer].reset_index(drop=True)
    
    if substituteclusters!="": #for adapt1(), adapt2(), adapt3()
        with open(substituteclusters, "r", encoding="utf-8") as f:
            global substidict
            substidict = ast.literal_eval(f.read())
        global wordstruc
        wordstruc=list(set(dfety["old_struc"])) #this a list of wordstructures that were allowed in the old layer
        global maxnrofclusters
        maxnrofclusters=sorted(map(len,map(ipa2tokens,wordstruc)))[-1] #this is the maximum nr of consonant and vowel clusters in a uralic word

    else: #for deletion() and clusters2substidict() 
        global allowedclust
        allowedclust=set(flatten(dfety["Old"].apply(ipa2clusters).tolist())) #this is a list of all clusters that are documented in dfetymology
        global maxclustlen
        tokenizedclust=list(map(ipa2tokens,allowedclust)) #this variable is only used in the line below
        maxclustlen=sorted(map(len,tokenizedclust),reverse=True)[0] #how amny ipa-tokens long was the longest possible cluster in uralic
        global dfsubsti
        dfsubsti=pd.read_csv(substitutephons,encoding="utf-8")
        global sudict
        sudict=dict(zip(dfsubsti["L2_phons"], dfsubsti["L1_substitutions"])) #convert the filledout.csv to a dictionary (which is faster to work with)
        global dfL2
        dfL2=pd.read_csv(L2,encoding="utf-8")    
        
def deletion(cluster):    

    cluster = ipa2tokens(cluster,merge_vowels=False,merge_geminates=False) #"abcd"-> ["a","b","c","d"]
    allsubsti = list(map(sudict.get, cluster)) #["a","b"]->["x, y", "z"]
    allsubsti = flatten([i.split(", ") for i in allsubsti]) #["x, y", "z"] -> ["x","y","z"]
    
    for index in range(2,maxclustlen+1): #combinations ONLY for 2 or more phonemes 
        for clu in combinations(cluster, index): #abcd->ab,ac,ad,bc,bd,cd (tuples)
            clu=list(map(sudict.get, clu)) #(a,b) -> ('x, y','z') get L1_substitutions from dict
            clu=[i.split(", ") for i in clu] #turn L1_substitutions to lists: ('x, y','z') -> ([x,y],[z])
            for j in product(*clu): #([x,y],[z]) -> [(x,z),(y,z)] list of tuples
                allsubsti.append("".join(list(j))) #tuple->list->string (x, z)->[x,z]->"xz"
    
    return ", ".join(list(dict.fromkeys([x for x in allsubsti if x in allowedclust])))

def clusters2substidict(name="substidict"):

    global dfsubsti
    clusters = sorted(set(flatten(dfL2.ipa.apply(ipa2clusters).tolist()))) #get all possible gothic clusters #not the same as substiphons
    clusters = [clu for clu in clusters if clu not in dfsubsti.L2_phons.tolist()] #subtract single phonemes (non-clusters), b/c combinations() can't handle them
    dfclust=pd.DataFrame({"L2_phons": clusters, "L1_substitutions": list(map(deletion,clusters))}) #col1: actual clusters, col2: their possible L1_substitutions
    dfsubsti=dfsubsti.append(dfclust) #merge df of single phonemes and clusters
    substidict=str(dict(zip(dfsubsti.L2_phons,dfsubsti.L1_substitutions))) #transform csv to machine-readable dictionary
    with open(name+".txt","w",encoding="utf-8") as data:
        data.write(substidict)
        
def adapt1(L2ipa):

    return L2ipa.replace("b","p").replace("c","s").replace("d","t").replace("h","k").replace("x","s").replace("z","s").replace("ɔ","ɑ").replace("ɛ","æ")\
    .replace("ɡ","k").replace("ɪ","i").replace("ɸ","p").replace("β","w").replace("θ","t").replace("l̥","V").replace("m̥","V").replace("n̥","V").replace("r̥","V")

def adapt2(L2ipa):

    struc=word2struc(L2ipa)
    C=[]
    for i in wordstruc:
        C.append(editdistancewith2ops(struc,i))
    adaptedstruc=sorted(list(zip(C,wordstruc)))[0][1]
    edits=ld.editops(struc,adaptedstruc) #editops between the actual structure and the closest allowed structure
    L2ipaout=L2ipa.replace("m̥","V").replace("l̥","V").replace("n̥","V").replace("r̥","V") #else apply_edit interprets the circles as chars of their own
    return adapt1(ld.apply_edit(edits, L2ipaout, adaptedstruc))

def adapt3(L2ipa):
    
    args=[]
    substilist=[]
    L2ipa=ipa2clusters(L2ipa)
    
    if len(L2ipa)>maxnrofclusters:
        return "too long"

    idxdict = defaultdict(count(1).__next__) #same letter same substitution. e.g. a->v/w: acab -> vxvy/wxwy and not vxwy/wxvy
    idxlist = [idxdict[cluster]-1 for cluster in L2ipa] #'acab' -> idxlist=[0,1,0,2]
    L2ipa = list(dict.fromkeys(L2ipa)) #'acab'->'acb'

    for i in L2ipa:
        args.append(substidict[i].split(", ")) #'acb'-> [['v','w'],['x'],['y','z']]
    for subst in product(*args): #[['v','w'],['x'],['y','z']] -> vxy,vxz,wxy,wxz
        mirror=[] #vxy,vxz,wxy,wxz -> vxvy,vxvz,wxwy,wxwz 
        for i in idxlist:
            mirror+=subst[i]
            mirror="".join(mirror)
        substilist.append(mirror)
    output = ", ".join([i for i in substilist if word2struc(i) in wordstruc])
    return output if output!="" else "wrong phonotactics"