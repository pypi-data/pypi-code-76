import pandas as pd
import spacy,re,os
nlp = spacy.load('en_core_web_sm')
import json

def excel_dict():
    data = pd.read_csv('/home/nitayananda/PICO/PICO_TEST_EBMMODEL.csv',sep='\t')
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

#sexcel_dict()
with open('result1.json', 'r') as fp:
    result = json.load(fp)

with open('pico_detailed_tagger.json', 'r') as fp:
    pico_tags = json.load(fp)

def return_pico_val(tag,pico):
    detailed_label = re.sub(pico+'-','',tag)
    detailed_label = re.sub('-$','',detailed_label)
    flag = False
    for key,val in pico_tags[pico.lower()].items():
        if(val==detailed_label):
            flag = True
            return key
    return False
    
        

i=0
cwd = '/home/nitayananda/PICO/EBMNLPHirech/LSTMCRFApp'
base_path = os.path.join(cwd,'nlp_data')
os.makedirs(os.path.join(cwd,'nlp_data'),exist_ok=True)
document_path = os.path.join(base_path,'documents')
os.makedirs(document_path,exist_ok=True)
# annotation_path = os.path.join(base_path,'annotations')
intervention_train_path = os.path.join(base_path,'annotations/aggregated/starting_spans/interventions')
os.makedirs(intervention_train_path,exist_ok=True)
participant_train_path = os.path.join(base_path,'annotations/aggregated/starting_spans/participants')
os.makedirs(participant_train_path,exist_ok=True)
outcome_train_path = os.path.join(base_path,'annotations/aggregated/starting_spans/outcomes')
os.makedirs(outcome_train_path,exist_ok=True)
intervention_train_path_detailed = os.path.join(base_path,'annotations/aggregated/hierarchical_labels/interventions')
os.makedirs(intervention_train_path_detailed,exist_ok=True)
participant_train_path_detailed = os.path.join(base_path,'annotations/aggregated/hierarchical_labels/participants')
os.makedirs(participant_train_path_detailed,exist_ok=True)
outcome_train_path_detailed = os.path.join(base_path,'annotations/aggregated/hierarchical_labels/outcomes')
os.makedirs(outcome_train_path_detailed,exist_ok=True)
total_pmid = len(result.items())
train_length = int(total_pmid*0.8)

for key,val in list(result.items()):
    if(i < train_length):
        batch = 'train'
    else:
        batch = 'test/gold'
    ++i
    token_file = open(os.path.join(document_path,str(key)+'.tokens'),'w')
    pos_file = open(os.path.join(document_path,str(key)+'.pos'),'w')
    os.makedirs(os.path.join(intervention_train_path,batch),exist_ok=True)
    intervention_file = open(os.path.join(intervention_train_path,batch,str(key)+'.AGGREGATED.ann'),'w')
    os.makedirs(os.path.join(participant_train_path,batch),exist_ok=True)
    participant_file = open(os.path.join(participant_train_path,batch,str(key)+'.AGGREGATED.ann'),'w')
    os.makedirs(os.path.join(outcome_train_path,batch),exist_ok=True)
    outcome_file = open(os.path.join(outcome_train_path,batch,str(key)+'.AGGREGATED.ann'),'w')
    os.makedirs(os.path.join(intervention_train_path_detailed,batch),exist_ok=True)
    intervention_file_detailed = open(os.path.join(intervention_train_path_detailed,batch,str(key)+'.AGGREGATED.ann'),'w')
    os.makedirs(os.path.join(participant_train_path_detailed,batch),exist_ok=True)
    participant_file_detailed = open(os.path.join(participant_train_path_detailed,batch,str(key)+'.AGGREGATED.ann'),'w')
    os.makedirs(os.path.join(outcome_train_path_detailed,batch),exist_ok=True)
    outcome_file_detailed = open(os.path.join(outcome_train_path_detailed,batch,str(key)+'.AGGREGATED.ann'),'w')
    print(i)
    i=i+1
    sent = val['SENT']
    for ent in nlp(sent):
        token_file.write(ent.text)
        pos_file.write(ent.tag_)
        token_file.write('\n')
        pos_file.write('\n')

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

        if(label=='Interventions'):
            intervention_file.write(str(1))
            detailed_label_val = return_pico_val(detailed_label,label)
            if(detailed_label_val):
                intervention_file_detailed.write(detailed_label_val)
            else:
                intervention_file_detailed.write(str(0))

        else:
            intervention_file.write(str(0))
            intervention_file_detailed.write(str(0))
        if(label=='Participants'):
            participant_file.write(str(1))
            detailed_label_val = return_pico_val(detailed_label,label)
            if(detailed_label_val):
                participant_file_detailed.write(detailed_label_val)
            else:
                participant_file_detailed.write(str(0))
        else:
            participant_file.write(str(0))
            participant_file_detailed.write(str(0))
        if(label=='Outcomes'):
            outcome_file.write(str(1))
            detailed_label_val = return_pico_val(detailed_label,label)
            if(detailed_label_val):
                outcome_file_detailed.write(detailed_label_val)
            else:
                outcome_file_detailed.write(str(0))
        else:
            outcome_file.write(str(0))
            outcome_file_detailed.write(str(0))
        intervention_file.write('\n')
        participant_file.write('\n')
        outcome_file.write('\n')
        intervention_file_detailed.write('\n')
        participant_file_detailed.write('\n')
        outcome_file_detailed.write('\n')

       
    token_file.close()
    pos_file.close()
    intervention_file.close()
    participant_file.close()
    outcome_file.close()
    intervention_file_detailed.close()
    participant_file_detailed.close()
    outcome_file_detailed.close()
