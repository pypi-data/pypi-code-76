import pandas as pd
import numpy as np
import jsonlines
import re
import json

def read_io(filepath, source='rasa_nlu.md', target='rasa_nlu'):
    ## available options
    # rasa_nlu.md, rasa_nlu

    if source == 'rasa_nlu.md' and target == 'rasa_nlu':
        ## TODO
        temp = read_io(filepath, 'rasa_nlu.md', 'json_str')
        #############################################################

        nludata = pd.read_json(temp)
        nludata = pd.DataFrame(nludata['rasa_nlu_data']['common_examples'])

        return nludata
    elif source == 'rasa_nlu.md' and target == 'json':
        ## TODO
        temp = read_io(filepath, 'rasa_nlu.md', 'json_str')
        nludata = json.loads(temp)
        return nludata

    elif source == 'rasa_nlu.md' and target == 'json_str':
        nludata = read_io(filepath, 'rasa_nlu.md', 'training_data')
        nludata = nludata.nlu_as_json()
        return nludata

    elif source == 'rasa_nlu.md' and target == 'training_data':
        
        # from rasa.importers.rasa import RasaFileImporter
        # importer = RasaFileImporter(None, None, [filepath])
        # nludata = await importer.get_nlu_data()
        from typing import Iterable , Text
        from rasa.nlu.training_data import TrainingData
        from rasa.nlu.training_data import loading
        language = 'en'
        training_datas = [loading.load_data(nlu_file, language) for nlu_file in [filepath]]
        nludata = TrainingData().merge(*training_datas)
        nludata.fill_response_phrases()
        return nludata


    elif source == 'rasa_nlu.md' and target == 'finie':
        ## TODO
        temp = read_io(filepath, 'rasa_nlu.md', 'rasa_nlu')
        temp = convert_io(temp, 'rasa_nlu', 'finie')
        return temp

    elif source == 'rasa_nlu.md' and target == 'spacy':
        ## TODO
        temp = read_io(filepath, 'rasa_nlu.md', 'rasa_nlu')
        temp = convert_io(temp, 'rasa_nlu', 'finie')
        temp = convert_io(temp, 'finie', 'spacy')
        return temp

    elif source == 'doccano.jsonl' and target == 'finie':
        dftemp = []
        intent = filepath
        with jsonlines.open(filepath , mode='r') as f:

            _f_jsonlines = []
            for line in f:
                _f_jsonlines.append(line)
            _f_jsonlines = sorted(_f_jsonlines, key=lambda x: x['id']) if 'id' in _f_jsonlines[0] else _f_jsonlines

            for line in _f_jsonlines:
                temp = []
                line_labels = sorted(line['labels'], key=lambda x:x[0])
                for l in line_labels:
                    temp.append({'label': l[2], 'word':line['text'][l[0]:l[1]], 'start':l[0], 'end':l[1]})

                assert line['text'] == " ".join(t['word'] for t in temp)
                dftemp.append((line['text'], temp, intent))

        df = pd.DataFrame(dftemp, columns=['Sentence', 'Labels', 'Intent'])
        return df

def write_io(inputs, filepath, source='rasa_nlu_ner', target='rasa_nlu.md'):

    if source == 'finie' and target == 'doccano.jsonl':
        df = inputs
        with open(filepath, 'w') as f:
            # {"text": "Peter Blackburn", "labels": [ [0, 15, "PERSON"] ]}
            # {"text": "EU rejects German call to boycott British lamb.", "labels": [ [0, 2, "ORG"], [11, 17, "MISC"], ... ]}
            for idx, row in df.iterrows():
                d = row['Labels']

                temp0 = ''
                temp1 = []
                offset = 0
                token_count = len(d)
                lidx = 0
                while lidx < token_count:
                    l = d[lidx]
                    
                    word = l['word']
                    label = l['label']

                    # temp1.append([offset, offset+len(word), label])
                    temp1.append([l['start'], l['end'], label])
                    
                    if lidx < token_count -1:
                        if l['end'] != d[lidx+1]['start']:
                            temp0 += word + " "
                        else:
                            temp0 += word
                    else:
                        temp0 += word
                    # temp0 += word + " "
                    offset += len(word) +1
                    
                    lidx += 1
                
                temp0 = temp0.strip()
                line = json.dumps({"text":temp0, "labels":temp1})
        
                f.write(line + '\n')
    
    elif source == 'rasa_nlu_ner' and target == 'rasa_nlu.md':
        
        def generate_entity(e):
            
            # [3]{"entity":"B-DURATION", "role":"MONTH"}
            result = ''
            result += '['
            value = e['value']
            result += value
            result += ']'
            result += '{'
            entity = e['entity']
            result += f'"entity": "{entity}"'
            if 'role' in e:
                role = e['role']
                result += f', "role": "{role}"'
            result += '}'
            return result

        def generate_sentence(row):
            text = row['Text']
            entities = row['Entities']
            if entities != entities:
                return text
            else:
                result = ''
                prev_end = 0
                for e in entities:
                    result += text[prev_end:e['start']]
                    result += generate_entity(e)
                    prev_end = e['end']
                result += text[prev_end:]
                return result

        df = inputs
        with open(filepath,'w') as f:
            for entry, group in df.groupby('Intent'):
                f.write('## intent:' + entry + '\n')
                for idx, row in group.iterrows():
                    sentence = generate_sentence(row)
                    f.write('- ' + sentence + '\n')
                f.write('\n')

    elif source == 'rasa_finie_nlu_ner' and target == 'rasa_nlu.md':
        def generate_entity(token, roles=['to', 'from','DAY','MONTH','YEAR'], delimiter='-'):
    
            def generate_format(word, entity, role, O='O'):
                
                if entity == O:
                    return word
                
                if role:
                    return f'[{word}]{{"entity":"{entity}", "role":"{role}"}}'
                else:
                    return f'[{word}]{{"entity":"{entity}"}}'
            
            result = None
            
            label = token['label']
            label_parts = label.split(delimiter)
            
            matched_roles = list(set(label_parts) & set(roles) )
            
            if len(matched_roles) == 0:
                result = generate_format(token['word'], label , None)
            elif len(matched_roles) == 1:
                templabel = delimiter.join([l for l in label_parts if l not in matched_roles])
                result = generate_format(token['word'], templabel, matched_roles[0])
            else:
                print(label)
                print(matched_roles)
                assert "Number of matched roles is not 1" == 0
                
            assert result != None
            
            return result

        def write_df_to_file(f, df, keep_examples_without_entity=True):
            
            for entry, group in df.groupby('Intent'):
                f.write('## intent:' + entry + '\n')

                if 'Labels' in df.columns:
                    if np.all(group['Labels'].isna().values):
                        group = group.dropna(axis=1)
                
                if 'Labels' in group.columns:

                    for text in group['Labels'].values:
                        temp = ""
                        for token in text:
                            temp += generate_entity(token) + " "

                        if ']{"entity":"' in temp or keep_examples_without_entity:
                            text = temp
                            f.write('- ' + text.strip() + '\n')
                else:
                    for text in group['Text'].values:
                        f.write('- ' + text.strip() + '\n')
                    
                f.write('\n')

        df = inputs
        with open(filepath,'w') as f:   
            write_df_to_file(f, df)

            if len(df['Intent'].unique()) == 1 and False: # Disable dummy entries
                
                f.write('## intent:' + 'dummy' + '\n')
                f.write('- ' 'dummy 1' + '\n')
                f.write('- ' 'dummy 2' + '\n')
                f.write('- ' 'dummy 3' + '\n')
                f.write('- ' 'dummy 4' + '\n')
                f.write('- ' 'dummy 5' + '\n')
                f.write('- ' 'dummy 6' + '\n')
                f.write('\n')
            
            #     f.write(regexconfig)
            #     f.write('\n')
            pass
    elif source == 'rasa_nlu_base' and target == 'rasa_nlu.md':
        train = inputs
        with open(filepath ,'w') as f:

            for entry, group in train.loc[:60].groupby('Intent'):
                f.write('## intent:' + entry + '\n')
                
                for text in group['Text'].values:
                    f.write('- ' + text.strip() + '\n')
                    
                f.write('\n')

    elif source == 'rasa_story_base' and target == 'rasa_story.md':
        train = inputs
        with open(filepath,'w') as f:
        #     f.write('text1')

            for entry, group in train.groupby('Intent'):
                f.write('## ' + entry + '\n')
                f.write('* ' + entry + '\n')
                f.write('    - utter_group_' + entry + '\n')
                
                f.write('\n')

    elif source == 'rasa_domain_base' and target == 'rasa_domain.md':
        train = inputs

        # http://www.yamllint.com/

        escapecharregex = r'\\.*?\s'
        with open(filepath ,'w') as f:
        #     f.write('text1')

            f.write('intents:\n')
            for entry, group in train.groupby('Intent'):
                f.write('- ' + entry + '\n')
                
            f.write('responses:\n')
            for entry, group in train.groupby('Intent'):
                f.write('  utter_group_' + entry + ':\n')
                
                answer =  group['Answer'].values[0]
                # if("Sizi anlamaya çalışıyorum." in answer):
                #     print(answer)
                #     print(type(answer))
                #     print(re.sub(emojiregex, " ", str(answer)))
                # text = re.sub(escapecharregex, " ", answer)
                text = answer.replace('\\', "\\\\")
                text = text.replace('"', '\\"')
                f.write('  - text: "' + text + '"\n\n')
                
                
            f.write('\n')
            
            f.write('actions:\n')
            f.write('- action_request_example_1\n')
            f.write('\n')
            
            f.write('session_config:\n')
            f.write('  session_expiration_time: 0.0\n')
            f.write('  carry_over_slots_to_new_session: true\n')
            f.write('\n')

def convert_io(inputs, source='finie', target='spacy'):
    
    ## available options
    # finie - spacy
    # spacy - finie

    if source == 'finie' and target == 'spacy':

        if str(type(inputs)) == str(type(pd.DataFrame())):
            df = inputs

        import spacy
        from spacy.lang.tr import Turkish as SpacyTurkish
        from spacy.tokens import Span, Token, Doc

        trnlp = SpacyTurkish()
        sdocs = []
        for idx, row in df.iterrows():
            tokens = [ann['word'] for ann in row['Labels']]
            spaces = [row['Labels'][i]['end'] != row['Labels'][i+1]['start'] for i in range(0, len(tokens)-1)] + [False]

            sdoc = spacy.tokens.doc.Doc(trnlp.vocab, words=tokens, spaces=spaces)
            for idx, ann in enumerate(row['Labels']):
                sdoc.ents += (Span(sdoc, idx, idx+1, label=ann['label']), )
            sdocs.append(sdoc)
        return sdocs

    elif source == 'spacy' and target == 'finie':
        spacy_docs = None
        class_name = None
        class_column_name = 'label'

        if str(type(inputs)) == str(type(['a'])):
            spacy_docs = inputs
        elif str(type(inputs)) == str(type({'a':'b'})):
            if 'spacy' in inputs:
                spacy_docs = inputs['spacy']
            else:
                assert 1 == 0
            if 'label' in inputs:
                class_name = inputs['label']
                class_column_name = 'Label'
            elif 'intent' in inputs:
                class_name = inputs['intent']
                class_column_name = 'Intent'
        
        spacy_docs_temp = [[{'label':t.ent_type_,'word':t.text, 'start': t.idx, 'end': t.idx + len(t.text),} for t in s] for s in spacy_docs]
        df = pd.DataFrame({'Labels':spacy_docs_temp})
        df[class_column_name] = class_name
        df['Sentence'] = [s.text for s in spacy_docs]

        return df

    elif source == 'rasa_nlu' and target == 'finie':

        from spacy.lang.tr import Turkish as SpacyTurkish
        from pyspace.nlp.toolkit.spacy import SpacyMatcherEntityUpdater, SpacyPostTokenizer, SpacyTokenizer, SpacyRegexReplaceNormalizer, SpacyWhitespaceNormalizer, SpacyEndPunctuationNormalizer

        df = inputs.copy()

        nlp = SpacyTurkish()
        nlp.tokenizer = lambda x: x
        nlp.add_pipe(SpacyTokenizer(nlp))
        nlp.add_pipe(SpacyPostTokenizer(merge_bool=True))

        finie_formatted_entities = []
        for idx, row in df.iterrows():
            text = row['text']
            entities = row['entities']
            if str(type(entities)) != str(type([])):
                entities = []
                
            doc = nlp(text, component_cfg={"SpacyPostTokenizer": {"posttokenization": entities, }})
            entities = SpacyPostTokenizer.update_entities(entities, doc)

            temp = [e['start'] for e in entities]

            for t in doc:
                if t.idx not in temp:

                    e = {
                        'start': t.idx,
                        'end': t.idx + len(t.text),
                        'value': t.text,
                        'entity': 'O',
                    }
                    entities.append(e)
                    temp.append(e['start'])
            
            entities = sorted(entities, key=lambda x: x['start'])
            for e in entities:
                e['word'] = e['value']
                del e['value']
                e['label'] = e['entity']
                del e['entity']
                if 'role' in e:
                    e['label'] += '-'+e['role']
                    del e['role']

            finie_formatted_entities.append(entities)
        
        df['Labels'] = finie_formatted_entities
        df = df[['text', 'intent', 'Labels']]
        df.columns = ['Sentence', 'Intent', 'Labels']
        return df

    elif source == 'softtechnlp' and target == 'rasa_nlu':
        from spacy.lang.tr import Turkish as SpacyTurkish
        from pyspace.nlp.toolkit.spacy import SpacyMatcherEntityUpdater, SpacyPostTokenizer, SpacyTokenizer, SpacyRegexReplaceNormalizer, SpacyWhitespaceNormalizer, SpacyEndPunctuationNormalizer
        
        df, config = inputs
        df = df.copy()

        nlp = SpacyTurkish()
        nlp.tokenizer = lambda x: x
        nlp.add_pipe(SpacyTokenizer(nlp))
        nlp.add_pipe(SpacyPostTokenizer(merge_bool=False))
        def _to_rasa_nlu(row, config={}):
            
            def _to_entity(text, value, entity):
                
                if value == value:
                    value = value.strip()
                    value = np.nan if value == '' else value
                
                if value == value:
                    matches = list(re.finditer(value,text))

                    return [{
                        'start':match.span()[0],
                        'end':match.span()[1],
                        'value':value,
                        'entity':entity,
                    } for match in matches]
                else:
                    return [None]

            entities = []
            for col in config:
                entities.extend(_to_entity(row['Text'], row[col], config[col]))
            entities = [e for e in entities if e]
                
            if entities == []:
                entities = np.nan # float('nan')
            else:
                doc = nlp(row['Text'], component_cfg={"SpacyPostTokenizer": {"posttokenization": entities, }})
                entities = SpacyPostTokenizer.update_entities(entities, doc)

            return entities

        df['Labels'] = df.apply(lambda row: _to_rasa_nlu(row, config=config), axis=1) 
        df = df[['Text','Intent','Labels']]
        df.columns = ['text', 'intent', 'entities']

        return df

    elif source == 'finie_raw' and target == 'finie':
        from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer
        
        df = inputs

        temp = []
        for idx, row in df.iterrows():
            text = row['Sentence']
            entities = row['Labels']

            temptext = ''
            tempstart = 0
            for e in entities:

                e['start'] = tempstart
                e['end'] = tempstart + len(e['word'])

                temptext += e['word']

                if e['end'] == len(text):
                    assert temptext == text
                    for e in entities:
                        assert 'start' in e
                    break
                else:
                    if xNormalizer.is_whitespace(text[e['end']]):
                        tempstart = e['end']+1
                        temptext += text[e['end']]
                    else:
                        tempstart = e['end']
        
        return df

    elif source == 'rasa_nlu.md' and target == 'rasa_nlu.json':
        read_path, write_path = inputs

        temp = read_io(read_path, source='rasa_nlu.md', target='json_str')

        with open(write_path,'w') as f:
            f.write(temp)

    elif source == 'rasa_nlu.xlsx' and target == 'rasa_nlu.json':
        read_path, write_path = inputs
        write_path_md = write_path[:-5] + '.md'

        temp = pd.read_excel(read_path)
        assert list(temp.columns) == ['Text', 'Intent']
        natemp = temp[temp.isna().apply(lambda x: x['Text'] and x['Intent'], axis=1)]
        if natemp.shape[0] != 0:
            print('There are emty cells.')
            display(natemp)
        temp = temp.dropna()

        write_io(temp, write_path_md, source='rasa_nlu_ner', target='rasa_nlu.md')
        convert_io([write_path_md, write_path], source= 'rasa_nlu.md' , target = 'rasa_nlu.json')

    else:
        assert source == 'invalid source type'
        

def sort_io(df, source='finie'):

    if source == 'finie':
        entity_col = 'Labels'
        entity_key = 'label'

        df = df.copy()
        df['word_count'] = df[entity_col].apply(lambda x: len(x))
        df['norm_v1'] = df[entity_col].apply(lambda x: ''.join([y[entity_key] for y in x if y[entity_key][:2] != 'I-']))
        df['norm_v2'] = df[entity_col].apply(lambda x: ''.join([y[entity_key] for y in x if y[entity_key][:2] != 'I-' and y[entity_key] != 'O' ]))
        df = df.sort_values(['norm_v2', 'word_count', 'norm_v1'])
        df = df.drop(columns=['norm_v2', 'word_count', 'norm_v1'])
        df = df.reset_index(drop=True)

        return df

def statistics_io(df, source='finie', target='entity'):

    if source == 'finie' and target == 'entity':
        entity_col = 'Labels'
        entity_key = 'label'
        text_key = 'word'

        df = df.copy()
        e2t = {}
        t2e = {}
        for idx, row in df.iterrows():
            entities = row[entity_col]
            for e in entities:
                ent = e[entity_key]
                ent = ent[2:] if ent[:2] in ['B-','I-'] else ent
                text = e[text_key]
                if ent == 'O':
                    # continue
                    pass

                if ent in e2t:
                    e2t[ent] += [text]
                else:
                    e2t[ent] = [text]

                if text in t2e:
                    t2e[text] += [ent]
                else:
                    t2e[text] = [ent]
        
        e2tkeys = list(e2t.keys())
        for ent in e2tkeys:
            vc = pd.DataFrame(pd.DataFrame(e2t[ent], columns=['text'])['text'].value_counts()).reset_index()
            vc.columns = ['text', 'freq']
            vc['entity'] = ent
            e2t[ent] = vc
        t2ekeys = list(t2e.keys())
        for text in t2ekeys:
            vc = pd.DataFrame(pd.DataFrame(t2e[text], columns=['entity'])['entity'].value_counts()).reset_index()
            vc.columns = ['entity', 'freq']
            vc['text'] = text
            t2e[text] = vc

        e2tdf = pd.concat(e2t.values())
        t2edf = pd.concat(t2e.values()) 

        e2tdf = e2tdf[['text','freq','entity']]
        t2edf = t2edf[['text','freq','entity']]

        e2tdf = e2tdf.sort_values(['text','freq','entity']).reset_index(drop=True)
        t2edf = t2edf.sort_values(['text','freq','entity']).reset_index(drop=True)
        assert np.all(e2tdf == t2edf)
        
        freqsall = e2tdf
        freqsall = freqsall[['entity', 'text', 'freq']]
        freqsall = freqsall.sort_values(['entity','freq','text',], ascending=[True,False,True]).reset_index(drop=True)

        ##################################################################
        ##################################################################

        def check_entity(text, entity='amount'):
            if entity == 'amount':
                textnum1d = ['bir','iki','üç','dört','beş','altı','yedi','sekiz','dokuz'] + ['ıkı','uc','dort','bes','alti','sekız']
                textnum2d = ['on','yirmi','otuz','kırk','elli','altmış','yetmiş','seksen','doksan'] + ['kirk','altmıs','yetmis']
                textnum2p = ['yüz','bin','milyon','milyar',] + ['yuz','bın',]
                textnumX = ['buçuk','bucuk','bck','bçk']
                textnum = textnum1d + textnum2d + textnum2p + textnumX
                currency = ['tl','lira', 'try','usd','$']
                textdate = ['gun','gün','ay','yıl','yil','yılda','yilda',]

                tn = '('+'|'.join(textnum)+')'
                c = '('+'|'.join(currency)+')'
                td = '('+'|'.join(textdate)+')'
                p = fr'(.+?){tn}*{c}*{td}*$'
                text = re.sub(p, r'\1',text,re.I)

                if text in textnum:
                    return True
                
                p = r'[\.,]'
                text = re.sub(p, r'',text)
                
                try:
                    int(text)
                    return True
                except:
                    pass
                
                return False
        
        def split_num(df):
            num = df[df.apply(lambda x: check_entity(x['text'], entity='amount'),axis=1)]
            nonnum = df[df.apply(lambda x: not check_entity(x['text'], entity='amount'),axis=1)]
            return (num, nonnum)


        ##################################################################
        ##################################################################

        ################################################################## V - 0 
        freqfreqs = freqsall['text'].value_counts()

        ################################################################## V - 1
        ## REMOVE ONLY 'O' LABELED TOKENS
        freqs_with_O = freqsall[ ~( (freqsall['entity'] == 'O') & (freqsall['text'].isin(list(freqfreqs[freqfreqs==1].index))) )].reset_index(drop=True)
        freqfreqs = freqs_with_O['text'].value_counts()

        ################################################################## V - 2
        ## TEXT_O # SAME TOKEN LABELED AS 'O' AND ANOTHER
        text_O = freqs_with_O[ ( (freqs_with_O['text'].isin(list(freqs_with_O[freqs_with_O['entity'] == 'O']['text']))) ) ].sort_values(['text', 'entity', 'freq',], ascending=[True,False,False]).reset_index(drop=True) # & (freqs_with_O['text'].isin(list(freqfreqs[freqfreqs!=1].index)))
        text_O_num_text, text_O_nonnum_text = split_num(text_O)
        
        freqs = freqs_with_O[ freqs_with_O['entity'] != 'O'].sort_values(['text', 'entity', 'freq',], ascending=[True,False,False]).reset_index(drop=True)
        freqfreqs = freqs['text'].value_counts()

        ################################################################## V - 3
        ## TEXT_1TO1 # SAME TOKEN IS ALWAYS LABELED AS SAME ENTITY
        text_1to1 = freqs[ freqs['text'].isin(list(freqfreqs[freqfreqs==1].index))].sort_values(['entity','text', 'freq',], ascending=[True,False,False]) 
        text_1to1_num_text, text_1to1_nonnum_text = split_num(text_1to1)
        
        freqs_1toN = freqs[ ~freqs['text'].isin(list(freqfreqs[freqfreqs==1].index))].sort_values(['entity','text', 'freq',], ascending=[True,False,False])
        freqfreqs = freqs_1toN['text'].value_counts()

        ################################################################## V - 4
        ## TEXT_1TON
        ## ## ENTITY ORDERED
        text_1toN_entity_ordered = freqs_1toN.sort_values(['entity','freq', 'text', ], ascending=[True,False,False])
        ## ## TEXT ORDERED
        text_1toN_text_ordered = freqs_1toN.sort_values(['text','entity', 'freq',], ascending=[False,True,False])
        ## ## ## NUM SPLIT
        text_1toN_num_text, text_1toN_nonnum_text = split_num(text_1toN_text_ordered)

        ################################################################## V - END
        output = type("xClass", (object,), {})
        output.text_O                   = type("xClass", (object,), {'all':text_O, 'num':text_O_num_text, 'nonnum':text_O_nonnum_text })
        output.text_1to1                = type("xClass", (object,), {'all':text_1to1, 'num':text_1to1_num_text, 'nonnum':text_1to1_nonnum_text })
        # output.text_1toN                = type("xClass", (object,), {'entity_ordered':text_1toN_entity_ordered, 'text_ordered':text_1toN_text_ordered, 'num':text_1toN_num_text, 'nonnum':text_1toN_nonnum_text }) 
        output.text_1toN                = type("xClass", (object,), {'all':text_1toN_entity_ordered, 'num':text_1toN_num_text, 'nonnum':text_1toN_nonnum_text }) 

        return output


