
######################################################
######################################################
# !pip install python-Levenshtein
try:
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    from jellyfish import jaro_similarity 

    from fuzzy_sequence_matcher.fuzzy_sequence_matcher import best_matches
except:
    pass
import difflib # SequenceMatcher
# !pip install cdifflib
# import cdifflib # CSequenceMatcher

######################################################
######################################################
from spacy.gold import align

######################################################
######################################################
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

######################################################
######################################################
import itertools


######################################################
######################################################

def __examples():
        
    def align_fuzzy(s1, s2):
        # sm = fuzz.SequenceMatcher(a=s1, b=s2, autojunk=False) # difflib.SequenceMatcher
        # sm = fuzz.SequenceMatcher(seq1=s1, seq2=s2, ) # fuzzywuzzy.StringMatcher.StringMatcher # requires python-Levenshtein
        # sm = fuzzywuzzy.StringMatcher.StringMatcher(seq1=s1, seq2=s2)
        # sm = cdifflib.CSequenceMatcher(a=s1, b=s2, )
        sm = difflib.SequenceMatcher(a=s1, b=s2, )
        temp = []

        for op in sm.get_opcodes():

            if op[0] == 'equal':
                temp1 = sm.a[op[1]:op[2]]
                temp2 = sm.b[op[3]:op[4]]

                for _t1, _t2 in zip(temp1, temp2):
                    temp.append( (_t1, _t2) )

            elif op[0] == 'replace':
                temp1 = sm.a[op[1]:op[2]]
                temp2 = sm.b[op[3]:op[4]]
                ####################
                _temp_diff = len(temp1) - len(temp2)
                _tempsmall, _templong = (temp1, temp2) if _temp_diff < 0 else (temp2, temp1)
                ####################
                tempx = best_matches(temp1, temp2, scorer=jaro_similarity)
                for idx, item in enumerate(_templong):

                    if item not in [t[0] for t in tempx] + [t[1] for t in tempx]:
                        _tempsmall.insert(idx, '')    
                ####################
                for _t1, _t2 in zip(temp1, temp2):
                    temp.append( (_t1, _t2) )
                ####################
                pass
        
        return temp

    def __example1():
        s1 = ['selam', 'lar', 'lar', 'lar', 'lar', 'na','bersi', 'niz', 'nasilsin', '?']
        s2 = ['selamlar', 'naber', 'siniz', '?']

        # s1 = ['selam', 'larki', 'lar', 'lar', 'lar', 'na','brs', 'nz', 'nasilsin', '?']
        # s2 = ['selmlar', 'ki', 'naber', 'siniz', '?']

        # s1 = ['selam', 'istemiyorum', 'lar', 'lar', 'lar', 'seni', 'istemiyorum', 'alabilir', 'misin', '?']
        # s2 = ['selmlar', 'istemyrm', 'lar', 'lar', 'sen', 'istemiyorum', 'alabilir', 'misin', '?']

        js1 = ''.join(s1)
        js2 = ''.join(s2)

        # 1 ################################################################
        # [print(item) for item in align_fuzzy(s1, s2)];
        # print()

        # 2 ################################################################
        # try:
        #     align(s1,s2)
        #     # alignment = align(s1n, s2n)
        #     # cost, a2b, b2a, a2b_multi, b2a_multi = alignment
        #     # a2b_multi
        #     pass
        # except Exception as e:
        #     print('spacy gold align failed')
        #     print(e)
        #     print()


        # 3 ################################################################
        [print(item) for item in align_fuzzy_multi(s1, s2, jaro_similarity)];
        # align_fuzzy_multi(s1,s2, fuzz.ratio)
        print()
        print()
            
 
        # 4 ################################################################
        [print(item) for item in align_fuzzy_multi(s1, s2, fuzz.ratio )];
        # align_fuzzy_multi(s1,s2, fuzz.ratio)
        print()
        print()

        # 5 ################################################################
        # [print(item) for item in align_fuzzy_multi(js1, js2, fuzz.ratio )];


        # 6 ################################################################
        dsm = difflib.SequenceMatcher(a=js1, b=js2).get_opcodes()
        for d in dsm:
            print(js1[d[1]:d[2]], ' -- ', js2[d[3]:d[4]])

    def __example2():
        # pip install dtw-python
        # https://github.com/pierre-rouanet/dtw
        # !pip install fastdtw
        import numpy as np
        from scipy.spatial.distance import euclidean
        from tensorflow import keras
        from fastdtw import fastdtw

        from sklearn import preprocessing
        le = preprocessing.LabelEncoder()

        temp = [chr(c).lower() for c in range(32,127)]
        temp = [ v for (i,v) in enumerate(temp) if v not in temp[0:i] ]
        le.fit(temp)

        # x = np.array(js1)
        # y = np.array(js2)
        x = keras.utils.to_categorical(le.transform(list(js1)), num_classes=len(temp))
        y = keras.utils.to_categorical(le.transform(list(js2)), num_classes=len(temp))

        distance, path = fastdtw(x, y, dist=euclidean)
        print(path)

        # temp = []
        # ti = -1
        # tj = -1


        # for p in path:
            
        #     if ti == p[0] or tj == p[1]:
                
        #         if ti == p[0]:
        #             tj += 1
        #         elif tj == p[1]:
        #             ti += 1
        #         else:
        #             print('whaut')
                
        #     else:
        #         temp.append(p)
        #         ti +=1
        #         tj +=1

        # print(temp)
        # path = temp

        # temp = ''
        # temp2 = ''
        # for p in path:
        #     temp += js1[p[0]]
        #     temp2 += js2[p[1]]
            
            
        # print(temp)
        # print(temp2)
        # path
        # print()
        # s1 = ['selam', 'lar', 'lar', 'lar', 'lar', 'na','bersi', 'niz', 'nasilsin', '?']
        # s2 = ['selamlar', 'naber', 'siniz', '?']

        pd.DataFrame([(p[0],js1[p[0]], js2[p[1]], p[1]) for p in path ],)

    def __example3():

        def align_entities(self, entities, tokens):

            aligned_entities = []
            
            e_len = len(entities)
            t_len = len(tokens)
            
            e_idx = 0
            t_idx = 0
            t_running_offset = 0
            t_running_offset_v2 = 0
            
            while True:
                
                e_matched_bool = False
                e_value = entities[e_idx]['value']
                e_running_offset = entities[e_idx]['start']
                e_end_offset = entities[e_idx]['end']
                
                t_value = tokens[t_idx]['text']
                t_end_offset = t_running_offset + len(t_value)
                t_end_offset_v2 = t_running_offset_v2 + len(t_value)
                
                ##########################################
                
                value_bool = t_value in e_value 
                start_bool = t_running_offset_v2 == e_running_offset
                end_bool = t_end_offset_v2 == e_end_offset
                
                match_ratio = max(min(t_end_offset_v2, e_end_offset) - max(t_running_offset_v2, e_running_offset), 0) / min(t_end_offset_v2 - t_running_offset_v2, e_end_offset - e_running_offset)
                
                ##########################################
                
                if start_bool or end_bool or match_ratio > 0.1:
                    
                    if 'role' in entities[e_idx]:
                        aligned_entities.append({
                            'value': t_value,
                            'entity': entities[e_idx]['entity'],
                            'role': entities[e_idx]['role'],
                            'start': t_running_offset,
                            'end': t_end_offset,
                        })
                    else:
                        aligned_entities.append({
                            'value': t_value,
                            'entity': entities[e_idx]['entity'],
                            'start': t_running_offset,
                            'end': t_end_offset,
                        })
                
                    if e_end_offset <= t_end_offset_v2:
                        e_idx += 1
                
                ##########################################
                
                # print(start_bool, end_bool, match_ratio)
                # print(e_value, t_value, )
                # print('e',e_running_offset, 'tv2',t_running_offset_v2)
                
                ##########################################
                
                if e_idx == e_len:
                    break
                
                ##########################################
                
                t_idx += 1
                t_running_offset = t_end_offset + 1
                t_running_offset_v2 = min(  t_end_offset_v2 + 1,  
                                            max(aligned_entities[-1]['end'] 
                                                    if aligned_entities else 0, 
                                                entities[e_idx]['start']
                                            )  
                                        )
                
                ##########################################
                
                if t_idx == t_len:
                    print()
                    print(" PROBLEM - NOT ALL ENTITIES ARE MATCHED ")
                    
                    print('entities', '\n', entities, '\n')
                    print('tokens', '\n', tokens, '\n')
                    break
                    

            return aligned_entities


def align_fuzzy_multi(s1, s2, scorer):
    
    def generate_pairs(i, j, s1l, s2l):
        pairs = []
        mode = 1
        
        if mode == 0:

            pairs.append( ((i,)          , (j,)          ))
            pairs.append( ((i, i+1)      , (j,)          )) if i < s1l -1 else None
            pairs.append( ((i, i+1, i+2) , (j,)          )) if i < s1l -2 else None
            pairs.append( ((i,)          , (j,j+1)       )) if j < s2l -1 else None
            pairs.append( ((i,)          , (j,j+1,j+2)   )) if j < s2l -2 else None
            pairs.append( ((i, i+1)      , (j, j+1)      )) if i < s1l -1 and j < s2l -1 else None
            pairs.append( ((i, i+1)      , (j, j+1, j+2) )) if i < s1l -1 and j < s2l -2 else None
            pairs.append( ((i, i+1, i+2) , (j, j+1)      )) if i < s1l -2 and j < s2l -1 else None
            pairs.append( ((i, i+1, i+2) , (j, j+1, j+2) )) if i < s1l -2 and j < s2l -2 else None
            pairs.append( ((i+1,)        , (j+1,)        )) if i < s1l -1 and j < s2l -1 else None
            pairs.append( ((i+1, i+2)    , (j+1, )       )) if i < s1l -2 and j < s2l -1 else None
            pairs.append( ((i+1, )       , (j+1, j+2)    )) if i < s1l -1 and j < s2l -2 else None
            pairs.append( ((i+2,)        , (j+1, j+2)    )) if i < s1l -2 and j < s2l -2 else None
            pairs.append( ((i+1, i+2)    , (j+2,)        )) if i < s1l -2 and j < s2l -2 else None
            pairs.append( ((i+1, i+2)    , (j+1, j+2)    )) if i < s1l -2 and j < s2l -2 else None
            pairs.append( ((i+2,)        , (j+2,)        )) if i < s1l -2 and j < s2l -2 else None
        
            
            pairs = [ (scorer( l1,l2 ),l1, l2, pair[0], pair[1] )
                    for pair in pairs 
                    for (l1,l2) in 
                    [(''.join([s1[i1] for i1 in pair[0]]), 
                      ''.join([s2[i2] for i2 in pair[1]]))]
                    if set(pair[0]).intersection(i_blacklist) == set() and 
                       set(pair[1]).intersection(j_blacklist) == set()
            ]
            pairs.sort(key=lambda x: x[0], reverse=True)
        
        elif mode == 1:
            
            def generate_window(i, j, s1l, s2l, window=3):
                pairs = sorted(list(itertools.product(range(window), range(window))), key= lambda x: max(x[0], x[1])*100 -  (1/(abs(x[0]-x[1])+1))*10 ) # 
                pairs = [pair for pair in pairs if i+pair[0] < s1l and j+pair[1] < s2l]
                pairs = [( tuple([i + ii for ii in range(pair[0]+1)]),  tuple([j + jj for jj in range(pair[1]+1)]) ) for pair in pairs]
    
                return pairs
    
            def generate_window_v2(i, j, s1l, s2l, window_1=4, window_2=7):
                temp = sorted(list(itertools.product(range(window_1), range(window_1))), key= lambda x: max(x[0], x[1])*100 -  (1/(abs(x[0]-x[1])+1))*10 ) # 
                pairs = []
                
                for t in temp:
                    pairs += generate_window(i+t[0], j+t[1], s1l, s2l, window=window_2)
                
                
                pairs = [ v for (i,v) in enumerate(pairs) if v not in pairs[0:i] ]
                return pairs
                
            pairs = generate_window_v2(i, j, s1l, s2l, window_1=40, window_2=4)
            # [print(p) for p in pairs]
            pairs = [ (scorer( l1,l2 ),l1, l2, pair[0], pair[1] )
                    for pair in pairs 
                    for (l1,l2) in 
                    [(''.join([s1[i1] for i1 in pair[0]]), 
                      ''.join([s2[i2] for i2 in pair[1]]))]
                    if set(pair[0]).intersection(i_blacklist) == set() and 
                       set(pair[1]).intersection(j_blacklist) == set()
            ]
            pairs.sort(key=lambda x: x[0], reverse=True)
                 
        return pairs
    
    
    result = []
    
    # preprocess
    s1 = [xNormalizer.tr_normalize(ss).lower().replace(" ","") for ss in s1]
    s2 = [xNormalizer.tr_normalize(ss).lower().replace(" ","") for ss in s2]
    
    ## initialize variables
    s1l = len(s1)
    s2l = len(s2)
    
    i = 0
    j = 0
    
    unmatched_i = list(range(s1l))
    unmatched_j = list(range(s2l))
    
    i_blacklist = set(range(s1l)).difference(set(unmatched_i))
    j_blacklist = set(range(s2l)).difference(set(unmatched_j))
    
    ## process alignment
    
    while i < s1l and j < s2l: 
        
        ## analyse alignment
        
        pairs = generate_pairs(i, j, s1l, s2l)

        
        ## QUESTION : WHEN SCORES ARE EQUAL, FIRST SHORTEST EXAMPLE SHOULD BE SELECTED
        ##            DOES SORT FUNCTION SATISFY THIS REQUIREMENT
        

        ## match a pair
        
        # print(pairs[0])
        
        if pairs[0][0] < 0.2:
            
            condition_1 = i_blacklist != set() and max(i_blacklist) > pairs[0][3][0]
            condition_2 = j_blacklist != set() and max(j_blacklist) > pairs[0][4][0]

            if condition_1:
                unmatched_i = [iii for iii in unmatched_i if iii != pairs[0][3][0]]
            
            if condition_2:
                unmatched_j = [iii for iii in unmatched_j if iii != pairs[0][4][0] ]

            if not ( condition_1 or condition_2 ):
                print(s1, pairs[0][1])
                print(s2, pairs[0][2])
                unmatched_i = [iii for iii in unmatched_i if iii != pairs[0][3][0]]
                unmatched_j = [iii for iii in unmatched_j if iii != pairs[0][4][0] ]

        else:
        
            result.append(pairs[0])

            ## update state variables

            unmatched_i = [iii for iii in unmatched_i if iii not in pairs[0][3] ]
            unmatched_j = [iii for iii in unmatched_j if iii not in pairs[0][4] ]
        
        i = min(unmatched_i) if unmatched_i != [] else s1l
        j = min(unmatched_j) if unmatched_j != [] else s2l
        
        i_blacklist = set(range(s1l)).difference(set(unmatched_i))
        j_blacklist = set(range(s2l)).difference(set(unmatched_j))

    # assert i == s1l
    # assert j == s2l
    
    return result













