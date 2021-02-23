import os
from lstm_crf.model.data_utils import CoNLLDataset
from lstm_crf.model.ner_model import NERModel
from lstm_crf.model.config import Config
import json
import sys, os
from tags.tag import tags as label_tags

config = Config(train_file_path=os.path.join(os.getcwd(),'base_data'))
data_prefix = "p1_all"
if data_prefix:
    cwd = os.path.join(os.getcwd(),'base_data')
    config.filename_dev   = os.path.join(cwd, 'data', data_prefix + '_' + os.path.basename(config.filename_dev))
    config.filename_test  = os.path.join(cwd, 'data', data_prefix + '_' + os.path.basename(config.filename_test))
    config.filename_train = os.path.join(cwd, 'data', data_prefix + '_' + os.path.basename(config.filename_train))

# build model
model = NERModel(config)
model.build()
model.restore_session(config.dir_model)

# with open("tag.json") as f1:
#     label_tags = json.load(f1)

with open('operation_type.json') as fp:
    operation = json.load(fp)['operation_type']

def align_data(data):
    """Given dict with lists, creates aligned strings

    Adapted from Assignment 3 of CS224N

    Args:
        data: (dict) data["x"] = ["I", "love", "you"]
              (dict) data["y"] = ["O", "O", "O"]

    Returns:
        data_aligned: (dict) data_align["x"] = "I love you"
                           data_align["y"] = "O O    O  "

    """
    spacings = [max([len(seq[i]) for seq in data.values()])
                for i in range(len(data[list(data.keys())[0]]))]
    data_aligned = dict()

    # for each entry, create aligned string
    for key, seq in data.items():
        str_aligned = ""
        for token, spacing in zip(seq, spacings):
            str_aligned += token + " " * (spacing - len(token) + 1)

        data_aligned[key] = str_aligned

    return data_aligned



def interactive_shell(model):
    """Creates interactive shell to play with model

    Args:
        model: instance of NERModel

    """
    model.logger.info("""
This is an interactive mode.
To exit, enter 'exit'.
You can enter a sentence like
input> I love Paris""")

    while True:
        try:
            # for python 2
            sentence = raw_input("input> ")
        except NameError:
            # for python 3
            sentence = input("input> ")

        words_raw = sentence.strip().split(" ")

        if words_raw == ["exit"]:
            break
        preds = model.predict(words_raw)
        to_print = align_data({"input": words_raw, "output": preds})

        for key, seq in to_print.items():
            model.logger.info(seq)



def get_tags(tag):
    if(tag!='N'):
        actual_tag = ''
        sublab,lab = tag.split('_')
        if(lab=='p'):
            actual_tag = 'participants/'+label_tags['participants'][sublab]
        elif(lab=='i'):
            actual_tag = 'interventions/'+label_tags['interventions'][sublab]
        else:
            actual_tag = 'outcomes/'+label_tags['outcomes'][sublab]
        if(operation=='starting_spans'):
            actual_tag = actual_tag.split('/')[0]
        return actual_tag
    else:
        return "None"
            
        
def process_results(word_list,tag_list):

    res = []
    mydict = {}
    flag = 0
    text = word_list[0]
    i=1
    tag=tag_list[0]
    while(i<len(tag_list)):
        curr_tag = tag_list[i]
        if(curr_tag!=tag):
            # print("a")
            # print(text)
            res.append({"tag":get_tags(tag),"text":text.strip()})
            # print("--a")
            # mydict[text] = tag
            text=""
            text = text+" "+word_list[i]
            tag = curr_tag
        else:
            # print(text)
            text = text+" "+word_list[i]
            tag = curr_tag
        i = i+1
    res.append({"tag":get_tags(tag),"text":text.strip()})
    return res

# pred = model.predict("atomoxetine is an established treatment for attention-deficit/hyperactivity disorder in children few studies have examined its efficacy for adults")
# print(pred)
def main(words_raw,data_prefix = "p1_all"):
    # create instance of config
    # create dataset
    pred = model.predict(words_raw)
    # print(process_results(words_raw.split(),pred))
    return process_results(words_raw.split(),pred)


# if __name__ == "__main__":
#     main(sys.argv[2],data_prefix = sys.argv[1])
# if __name__ == "__main__":
#     main(sys.argv[2],data_prefix = sys.argv[1])
