import ast
import os

from lingpy import ipa2tokens
import pandas as pd

from loanpy.helpers import applyfunc2col
from loanpy.helpers import ipa2clusters
from loanpy.helpers import list2regex

cns="jwʘǀǃǂǁk͡pɡ͡bcɡkqɖɟɠɢʄʈʛbb͡ddd̪pp͡ttt̪ɓɗb͡βk͡xp͡ɸq͡χɡ͡ɣɢ͡ʁc͡çd͡ʒt͡ʃɖ͡ʐɟ͡ʝʈ͡ʂb͡vd̪͡z̪d̪͡ðd̪͡ɮ̪d͡zd͡ɮd͡ʑp͡ft̪͡s̪t̪͡ɬ̪t̪͡θt͡st͡ɕt͡ɬxçħɣʁʂʃʐʒʕʝχfss̪vzz̪ðɸβθɧɕɬɬ̪ɮʑɱŋɳɴmnn̪ɲʀʙʟɭɽʎrr̪ɫɺɾhll̪ɦðʲt͡ʃʲnʲʃʲCl̥m̥n̥r̥"
vow="ɑɘɞɤɵʉaeiouyæøœɒɔəɘɵɞɜɛɨɪɯɶʊɐʌʏʔɥɰʋʍɹɻɜ¨ȣ∅V"

def launch(soundchangedict="scdict_all.txt",dfetymology="dfetymology.csv",soundsubsti="substi.csv",timelayer=""):
    
    os.chdir(os.path.dirname(os.path.abspath(__file__))+r"\data")
    
    if soundchangedict!="":
        with open(soundchangedict, "r", encoding="utf-8") as f:
            global scdict
            scdict = ast.literal_eval(f.read())
        global oldprefix
        if "#0" in scdict:
            oldprefix=scdict["#0"]+"?"
        #oldprefix="("+"|".join([scdict[i][1:][:-1] for i in ["#0"] if i in scdict])+")?"
        global oldsuffix # all dict entries for "0#","00#","000#" but remove duplicates
        oldsuffix="(((al)(ɑ|o|u|a|æ|e|i))|((ɑ|o|u|a|æ|e|i)(k|r|t)(ɑ|o|u|a|æ|e|i))|((j|m|w|ŋ)(ɑ|o|u|a|æ|e|i)))?" #just had to hardcode this part
    elif soundchangedict=="":
        global dfety
        dfety=pd.read_csv(dfetymology,encoding="utf-8")
        if timelayer != "":
            dfety=dfety[dfety.Lan==timelayer].reset_index(drop=True)   
        global substiphons
        dfsubsti=pd.read_csv(soundsubsti,encoding="utf-8")
        substiphons="".join(str(i) for i in set(dfsubsti["L1_substitutions"].str.split(", ").explode()))+"ȣ¨ɜ#00000#" #all phonemes that will occur in substitutions
        global dfsoundchange
        dfsoundchange=pd.DataFrame() #this will be the final output from which soundchangedict.txt will be generated

def getsoundchanges(reflex,root): #requires two ipastrings as input 

    reflex=ipa2clusters(reflex.replace("ː","")) #this sign can cause trouble otherwise. phoneme length will be ignored.
    root=ipa2clusters(root.replace("ː",""))

    if reflex[0] in vow and root[0] in cns: #both reflex and root have to start with a consonant, if not a "0" has to be inserted, marking a disappeared consonant
        reflex=["0"]+reflex
    elif reflex[0] in cns and root[0] in vow:
        root=["0"]+root

    diff=abs(len(root)-len(reflex)) # "a,b", "c,d,e,f,g" -> "a,b,000","c,d,efg"
    if len(reflex)<len(root):
        reflex+=["0"*diff]
        root=root[:-diff]+["".join(root[-diff:])]
    elif len(reflex)>len(root):
        root+=["0"*diff]
        reflex= reflex[:-diff]+["".join(reflex[-diff:])]

    reflex[0]="#"+reflex[0] #hashtags mark the beginning or end of a word
    reflex[-1]=reflex[-1]+"#"

    dfrootrefl=pd.DataFrame({"reflex":reflex,"root":root})
    dfrootrefl=dfrootrefl[dfrootrefl.root.apply(lambda x: all(elem in substiphons or elem=="0" for elem in ipa2tokens(x)))] #root has no hashtags to remove
    global dfsoundchange #this is a table that contains all possible sound changes, phonemes that are not in substiphons are being ignored!
    dfsoundchange=dfsoundchange.append(dfrootrefl) # global variable gets modified!
    
def dfetymology2soundchangedict(name="scdict"):

    dfety.apply(lambda x: getsoundchanges(x["New"], x["Old"]), axis=1)
    dfsc=dfsoundchange.groupby("reflex")["root"].apply(lambda x: list2regex(sorted(set(x)))).reset_index()
    soundchangedict=str(dict(zip(dfsc.reflex,dfsc.root)))
    
    with open(name+".txt","w",encoding="utf-8") as data:
        data.write(soundchangedict)
        
def reconstruct(ipaword): 

    ipaword=ipa2clusters(ipaword.replace("ː","")) #this character can be annoying. phoneme length is being ignored.
    ipaword[0]="#"+ipaword[0]
    ipaword[-1]=ipaword[-1]+"#" #hashtags denote the beginning and end of words
    return ", ".join([i for i in ipaword if i not in list(scdict.keys())])+" not old/from L2" if not all(elem in list(scdict.keys()) for elem in ipaword) else "^"+oldprefix+"".join([scdict[i] for i in ipaword])+oldsuffix+"$" #replace every phoneme with its regexroot from the dictionary made by makedicts.py