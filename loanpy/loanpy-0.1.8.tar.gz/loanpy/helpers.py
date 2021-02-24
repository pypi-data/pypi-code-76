import os
import re

from lingpy import ipa2tokens
import pandas as pd
from gensim.models import KeyedVectors
from nltk.corpus import wordnet as wn

cns="jwʘǀǃǂǁk͡pɡ͡bcɡkqɖɟɠɢʄʈʛbb͡ddd̪pp͡ttt̪ɓɗb͡βk͡xp͡ɸq͡χɡ͡ɣɢ͡ʁc͡çd͡ʒt͡ʃɖ͡ʐɟ͡ʝʈ͡ʂb͡vd̪͡z̪d̪͡ðd̪͡ɮ̪d͡zd͡ɮd͡ʑp͡ft̪͡s̪t̪͡ɬ̪t̪͡θt͡st͡ɕt͡ɬxçħɣʁʂʃʐʒʕʝχfss̪vzz̪ðɸβθɧɕɬɬ̪ɮʑɱŋɳɴmnn̪ɲʀʙʟɭɽʎrr̪ɫɺɾhll̪ɦðʲt͡ʃʲnʲʃʲCl̥m̥n̥r̥"
vow="ɑɘɞɤɵʉaeiouyæøœɒɔəɘɵɞɜɛɨɪɯɶʊɐʌʏʔɥɰʋʍɹɻɜ¨ȣ∅V"
cnsvow_regex="[^"+cns+vow+"]"

os.chdir(os.path.dirname(os.path.abspath(__file__))+r"\data\\")

def applyfunc2col(nameofcsv, inputcol, function, outputcol, name):

    dataframe=pd.read_csv(nameofcsv, encoding="utf-8")
    dataframe[outputcol]=dataframe[inputcol].apply(function)
    dataframe.to_csv(name,encoding="utf-8",index=False)

def flatten(mylist):

    return [item for sublist in mylist for item in sublist]

def word2struc(ipastring): #e.g. in: "baba" out: "CVCV" 
    output=""
    for i in ipa2tokens(ipastring, merge_vowels=False, merge_geminates=False):
        i=re.sub(cnsvow_regex,"",i) #keep only characters that are in cns and vow
        i=''.join([c for c in i if c not in "".join(set(re.sub(r'[^\W+]', '', cns)))+"ʲ"]) #remove ̥̪͡ ʲ from i
        if i in cns:
            output+="C"
        elif i in vow:
            output+="V"
    return output

#def word2struc(ipastring): #e.g. in: "baba" out: "CVCV" 

    #return "".join([(lambda x: "C" if (x in cns) else ("V" if (x in vow) else ""))(i) for i in ipa2tokens(ipastring, merge_vowels=False, merge_geminates=False)])

def ipa2clusters(ipastring): #out: list of consonant and vowel clusters e.g. in: "roflmao", out: ["r","o","flm","ao"]

    return [j for j in "".join([(lambda x: "€"+x+"€" if x[0] in vow else x)(i) for i in ipa2tokens(ipastring, merge_vowels=True)]).split("€") if j]

def list2regex(sclist):

    if sclist == ["0"] or sclist == ["00"] or sclist == ["000"]:
        return "" #these are derivational suffxies that appeared later in the new language, so we shouldn't search for them in the regex
       
    if "ȣ" in sclist:
        sclist.remove("ȣ")
        sclist.extend(["ɑ", "o", "u"])
    if "¨" in sclist:
        sclist.remove("¨")
        sclist.extend(["a", "æ", "e", "i"])
    if "ɜ" in sclist:
        sclist.remove("ɜ")
        sclist.extend(["ɑ", "o", "u", "a", "æ", "e", "i"])
            
    stem = "("+"|".join([i for i in list(dict.fromkeys(sclist))]) #bracket in the beginning and "|" as a separator (means "or" in regex)    
    
    for i in sclist: #if consonant or vowel, add placeholder "C" or "V" (=any consonant, any vowel)
        if i in cns:
            if "C" not in stem:
                stem+="|C"
        if i in vow:
            if "V" not in stem:
                stem+="|V"
        j=ipa2tokens(i)
        if len(j)>=2: #do combinatorics for clusters e.g "mp"->"mp",mC","Cp","CC" (there are no vowel clusters in uralic)
            if "CC" not in stem: 
                stem+="|CC"
            if j[0]+"C" not in stem:
                stem+="|"+j[0]+"C"
            if "C"+j[1] not in stem:
                stem+="|C"+j[1]
    
    if "0" in stem: #if sth CAN be a derivational suffix but doesnt have to, add a "?" after the bracket. (=optional search in regex)
        stem=stem.replace("0","").replace("|)",")").replace("(|","(").replace("||","|")
        return stem+")?"
    
    return stem+")" #close the regex bracket

def editdistancewith2ops(string1, string2): #provided by ita_c from geeksforgeeks https://www.geeksforgeeks.org/edit-distance-and-lcs-longest-common-subsequence/ (11.feb.2021)
 
    m = len(string1)     # Find longest common subsequence (LCS)
    n = len(string2)
    L = [[0 for x in range(n + 1)] 
            for y in range(m + 1)] 
    for i in range(m + 1):
        for j in range(n + 1):
            if (i == 0 or j == 0):
                L[i][j] = 0
            elif (string1[i - 1] == string2[j - 1]):
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j],
                              L[i][j - 1])
 
    lcs = L[m][n]
 
    return (m - lcs) + (n - lcs)*0.4 # Edit distance is delete operations + insert operations*0.4.

def loadvectors(filename="GoogleNews-vectors-negative300.bin"):

    global model
    model = KeyedVectors.load_word2vec_format(filename, binary=True)

def getsynonyms(enword, pos="nvar"):

    enword=enword.split(', ')
    return list(dict.fromkeys(flatten([enword]+[y.lemma_names() for y in [wn.synsets(x) for x in enword][0] if y.pos() in pos])))[:20]
        
def gensim_synonyms(L1_en, L2_en, posL1='nvar', posL2='nvar'):
    
    if isinstance(L1_en, float) or isinstance(L2_en, float): #missing translations = empty cells = nans = floats
        return -1
    
    else: #get names of synsets, if they match the wordtype, flatten list, remove duplicates
        L1=getsynonyms(L1_en, posL1)
        L2=getsynonyms(L2_en, posL2)
        
        topsim=-1 #score of the most similar word pair
        for L1_syn in L1:
            for L2_syn in L2: #calculate semantic similarity of all pairs0
                try:
                    modsim=model.similarity(L1_syn, L2_syn)
                except KeyError: #if word is not in KeyedVecors of gensim continue
                    continue                                   
                if modsim>topsim: #replace topsim if word pair is more similar than the current topsim, 
                    topsim=modsim                 
        return topsim
    
def gensim_similarity(en_word1,en_word2):
    return model.similarity(en_word1,en_word2)