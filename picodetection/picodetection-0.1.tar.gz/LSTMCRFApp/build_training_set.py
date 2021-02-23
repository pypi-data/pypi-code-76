import pandas as pd
import spacy,re
nlp = spacy.load('en_core_web_sm')
import json

def excel_dict():
    data = pd.read_csv('/home/nitayananda/PICO/train.csv',sep='\t')
    data.fillna('')
    data_dict={}
    value_dict={}
    label_details=[]
    for idx in data.index:
        if(str(data['PICO'][idx])=='' or str(data['PICO'][idx])=='nan'):
            continue
        print(idx)
        temp_label_dict={}
        if(str(data['PMID'][idx])) not in data_dict:
            if(len(label_details)!=0):
                value_dict['label_details']=label_details
                data_dict[str(data['PMID'][idx])] = value_dict
            value_dict={}
            label_details=[]        
            value_dict["SENT"] = str(data["SENT"][idx])
            temp_label_dict['label'] = data['LABEL'][idx]
            label_string=''
            if(str(data['NEW_LABEL_STRING']))=='nan':
                label_string = str(data['NEW_LABEL_STRING'][idx])
            else:
                label_string = str(data['LABEL_STRING'][idx])
            temp_label_dict['label_string'] = label_string
            temp_label_dict['label_string_token'] =  [ent.text.lower() for ent in nlp(label_string)]
            temp_label_dict['detailed_label'] = str(data['PICO'][idx])
            label_details.append(temp_label_dict)
        else:
            temp_label_dict['label'] = data['LABEL'][idx]
            label_string=''
            if(str(data['NEW_LABEL_STRING']))=='nan':
                label_string = str(data['NEW_LABEL_STRING'][idx])
            else:
                label_string = str(data['LABEL_STRING'][idx])
            temp_label_dict['label_string'] = label_string
            temp_label_dict['label_string_token'] =  [ent.text for ent in nlp(label_string)]
            temp_label_dict['detailed_label'] = str(data['PICO'][idx])
            label_details.append(temp_label_dict)
        
    if(len(label_details)!=0):
        value_dict['label_details']=label_details
        data_dict[str(data['PMID'][idx])] = value_dict


    with open('result1.json', 'w') as fp:
        json.dump(data_dict, fp)

#excel_dict()
with open('result1.json', 'r') as fp:
    result = json.load(fp)

fp =  open('p1_all_gold_comp.txt','w')
fp2 =  open('p1_all_gold.txt','w')
i=0

for val in list(result.values()):
    # print(pmid)
    print(i)
    i=i+1
    sent = val['SENT']
    for ent in nlp(sent):
        fp.write(ent.text+' '+ent.tag_+' ')
        fp2.write(ent.text+' '+ent.tag_+' ')
        label_details = val['label_details']
        # if(label_details[0]['detailed_label']=='' or label_details[0]['detailed_label']=='nan'):
        #     continue
        label='N'
        detailed_label = 'N'
        for label_detail in label_details:
            if(ent.text.lower() in label_detail['label_string_token']):
                detailed_label = label_detail['detailed_label']
                label = detailed_label.split('-')[0]#'1_'+detailed_label.split('-')[0][0].lower()
                detailed_label = re.sub(' ','-',detailed_label)
                if(label=='' or label=='nan'):
                    label='N'
                if(detailed_label=='' or detailed_label=='nan' or not detailed_label.__contains__('-')):
                    detailed_label='N'
        fp.write(label)
        fp2.write(detailed_label)
        fp.write('\n')
        fp2.write('\n')
    fp.write('\n')
    fp2.write('\n')