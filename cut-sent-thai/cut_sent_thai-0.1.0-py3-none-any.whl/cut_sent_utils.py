import numpy as np
import random
# from pythainlp.tag.named_entity import ThaiNameTagger
# ner = ThaiNameTagger()
# from thaipos import pos_tag, HMM
from thaipos import pos_tag
# hmm = HMM()
import torch

def genTrainingExamples(sentence_pairs, sentencesInSameParagraph, max_context_length=5):
    """
    generate training examples [ t_{-max_context_length},...,t_{max_context_length} ] for a paragaph
    inputs:
        sentence_pairs [(A,B),...] where A and B are sentences (str)
        sentencesInSameParagraph [A,B,C,...] where A,B,C,... are sentences (str)
    returns:
        positive_examples: [[left,right],...,], where each left and right is list of tuple
                            each tuple is (token,pos_tag,ner_tag) that's returned form ThaiNameTagger()

        negative_example: same as positive_example but built from negative (no cut) examples

        a positive example looks like: (first two lines is left, the rest is right)
        [[(' ', 'PUNCT', 'O'), ('ครั้ง', 'NOUN', 'O'), 
        ('ที่', 'SCONJ', 'O'), (' ', 'PUNCT', 'O'), ('1', 'NUM', 'O')], 
        [('โครงการ', 'NOUN', 'O'), ('วิจัยและพัฒนา', 'NOUN', 'O'), 
        ('อิเล็กทรอนิกส์', 'NOUN', 'O'), ('และ', 'CCONJ', 'O'), 
        ('คอมพิวเตอร์', 'NOUN', 'O')]]
    """
    paragraph = " ".join(sentencesInSameParagraph).strip()
    if len(paragraph) > 500:
        paragraph = paragraph[0:500]
    # print(paragraph)
    try:
        tokenizedAndTagged = pos_tag(paragraph)
    except:
        print("error!!!!!!")
    # print(tokenizedAndTagged)
    # tokenizedAndTagged = ner.get_ner(paragraph)
    positive_examples = []
    negative_examples = []

    # count how many spaces that should cut
    num_space_cut = len(sentencesInSameParagraph) - 1
    # print(num_space_cut)

    # count how many spaces in each sentence
    num_space_sentences = []
    for s in sentencesInSameParagraph:
        num_space_sentences.append( len(s.split(" "))-1 )
    # print(num_space_sentences)
    
    index_space_should_cut = []
    acc = 0
    for i in range(num_space_cut):
        index_space_should_cut.append(num_space_sentences[i] + 1 + acc)
        acc += num_space_sentences[i] + 1
    # print(index_space_should_cut)

    assert len(index_space_should_cut) == num_space_cut

    current_space_index = 1
    for i, (t, _) in enumerate(tokenizedAndTagged):
        if t == '<space>':
            left = tokenizedAndTagged[max(i-max_context_length,0):i]
            right = tokenizedAndTagged[i+1:min(i+max_context_length+1,len(tokenizedAndTagged))]
            left_tok = [x[0] for x in left]
            right_tok = [x[0] for x in right]
            # check if this sentence split or not
            split = False
            leftStr = "".join(left_tok)
            rightStr = "".join(right_tok)
            leftStr = leftStr.replace("<space>", " ").strip()
            rightStr = rightStr.replace("<space>", " ").strip()
            # print(leftStr)
            # print(rightStr)
            # for pair in sentence_pairs:
                # print(leftStr.find(pair[0]), rightStr.find(pair[1]), pair[0].find(leftStr), pair[1].find(rightStr))
                # if (leftStr.find(pair[0]) != -1 and rightStr.find(pair[1]) != -1) or (pair[0].find(leftStr) != -1 and pair[1].find(rightStr) != -1):
                #     split = True
            # print(split)
            # print("")
            if current_space_index in index_space_should_cut:
                split = True
            current_space_index += 1
            if split:
                # add to positive example
                positive_examples.append([left , right])
            else:
                # add to negative example
                negative_examples.append([left , right])

    return (positive_examples, negative_examples)


def build_vocabs(positive_examples_all, negative_examples_all):
    """
    build the vocabuary for words, POS tags, and NER tags
    inputs:
        positive_examples_all: list of positive_examples, see genTrainingExamples()
        negative_example_all: same as positive_examples_all but for negative
    return:
        unique_tokens: set of unique words
        unique_pos: set of unique POS tags

    """
    unique_tokens = set()
    unique_pos = set()
    # unique_ner = set()

    # we need to hold out some proportion of corpus from
    # building vocab, so that the model will encounter
    # some <unk> during training
    ratio_corpus_used = 0.8
    limit_length_positive = round( len(positive_examples_all)*ratio_corpus_used )
    limit_length_negative = round( len(negative_examples_all)*ratio_corpus_used )

    for p1 in positive_examples_all[0:limit_length_positive]:
        for p2 in p1[0]:
            if p2[0] not in unique_tokens:
                unique_tokens.add(p2[0])
            if p2[1] not in unique_pos:
                unique_pos.add(p2[1])
            # if p2[2] not in unique_ner:
            #     unique_ner.add(p2[2])
        for p2 in p1[1]:
            if p2[0] not in unique_tokens:
                unique_tokens.add(p2[0])
            if p2[1] not in unique_pos:
                unique_pos.add(p2[1])
            # if p2[2] not in unique_ner:
            #     unique_ner.add(p2[2])

    for p1 in negative_examples_all[0:limit_length_negative]:
        for p2 in p1[0]:
            if p2[0] not in unique_tokens:
                unique_tokens.add(p2[0])
            if p2[1] not in unique_pos:
                unique_pos.add(p2[1])
            # if p2[2] not in unique_ner:
            #     unique_ner.add(p2[2])
        for p2 in p1[1]:
            if p2[0] not in unique_tokens:
                unique_tokens.add(p2[0])
            if p2[1] not in unique_pos:
                unique_pos.add(p2[1])
            # if p2[2] not in unique_ner:
            #     unique_ner.add(p2[2])

    if ';' not in unique_tokens:
        unique_tokens.add(';')
    
    unique_tokens.add('<unk>')
    unique_pos.add('<unk>')
    # unique_ner.add('<unk>')

    return unique_tokens, unique_pos

def build_dictionaries(unique_tokens, unique_pos):
    """
    build the dictionaries stoi/itos for each type (word, pos, ner) of tokens
    inputs:
        unique_tokens, unique_pos, are the dictionaries
    return:
        stoi, itos, stoi_pos, itos_pos are the dictionaries
    """
    stoi = {}
    itos = {}
    for i, word in enumerate(unique_tokens):
        stoi[word] = i
        itos[i] = word

    stoi_pos = {}
    itos_pos = {}
    for i, tag in enumerate(unique_pos):
        stoi_pos[tag] = i
        itos_pos[i] = tag

    # stoi_ner = {}
    # itos_ner = {}
    # for i, tag in enumerate(unique_ner):
    #     stoi_ner[tag] = i
    #     itos_ner[i] = tag

    return stoi, itos, stoi_pos, itos_pos

def create_training_data(positive_examples_all, negative_examples_all, 
                        stoi, itos, stoi_pos, itos_pos, 
                        balanced=True, max_context_length=5):
    length_positive = len(positive_examples_all)
    if balanced:
        length_negative = length_positive
    else:
        length_negative = len(negative_examples_all)

    input_train_data = np.zeros([length_positive + length_negative, max_context_length*2])
    input_target = np.zeros([length_positive + length_negative])
    input_pos_data = np.zeros([length_positive + length_negative, max_context_length*2])
    # input_ner_data = np.zeros([length_positive + length_negative, max_context_length*2])
    index = 0

    for sp in positive_examples_all:
        # tuple (A,B), where A and B are list of tokenized words
        left_context = [p[0] for p in sp[0]]
        right_context = [p[0] for p in sp[1]]
        if len(left_context) > max_context_length:
            left_context = left_context[-max_context_length:]
        if len(right_context) > max_context_length:
            right_context = right_context[0:max_context_length]
        while len(left_context) < max_context_length:
            left_context.insert(0, ';')
        while len(right_context) < max_context_length:
            right_context.append(';')
        left_context_ids = []
        right_context_ids = []
        for l in left_context:
            try:
                left_context_ids.append(stoi[l])
            except:
                left_context_ids.append(stoi['<unk>'])
        for r in right_context:
            try:
                right_context_ids.append(stoi[r])
            except:
                right_context_ids.append(stoi['<unk>'])
        input_train_data[index,:] = left_context_ids + right_context_ids

        left_context = [p[1] for p in sp[0]]
        right_context = [p[1] for p in sp[1]]
        if len(left_context) > max_context_length:
            left_context = left_context[-max_context_length:]
        if len(right_context) > max_context_length:
            right_context = right_context[0:max_context_length]
        while len(left_context) < max_context_length:
            left_context.insert(0, 'PUNC')
        while len(right_context) < max_context_length:
            right_context.append('PUNC')
        left_context_ids = []
        right_context_ids = []
        for l in left_context:
            try:
                left_context_ids.append(stoi_pos[l])
            except:
                left_context_ids.append(stoi_pos['<unk>'])
        for r in right_context:
            try:
                right_context_ids.append(stoi_pos[r])
            except:
                right_context_ids.append(stoi_pos['<unk>'])
        input_pos_data[index,:] = left_context_ids + right_context_ids

        # left_context = [p[2] for p in sp[0]]
        # right_context = [p[2] for p in sp[1]]
        # if len(left_context) > max_context_length:
        #     left_context = left_context[-max_context_length:]
        # if len(right_context) > max_context_length:
        #     right_context = right_context[0:max_context_length]
        # while len(left_context) < max_context_length:
        #     left_context.insert(0, 'O')
        # while len(right_context) < max_context_length:
        #     right_context.append('O')
        # left_context_ids = []
        # right_context_ids = []
        # for l in left_context:
        #     try:
        #         left_context_ids.append(stoi_ner[l])
        #     except:
        #         left_context_ids.append(stoi_ner['<unk>'])
        # for r in right_context:
        #     try:
        #         right_context_ids.append(stoi_ner[r])
        #     except:
        #         right_context_ids.append(stoi_ner['<unk>'])
        # input_ner_data[index,:] = left_context_ids + right_context_ids

        input_target[index] = 1
        index += 1

    random.shuffle(negative_examples_all)

    for sp in negative_examples_all:
        # tuple (A,B), where A and B are list of tokenized words
        left_context = [p[0] for p in sp[0]]
        right_context = [p[0] for p in sp[1]]
        if len(left_context) > max_context_length:
            left_context = left_context[-max_context_length:]
        if len(right_context) > max_context_length:
            right_context = right_context[0:max_context_length]
        while len(left_context) < max_context_length:
            left_context.insert(0, ';')
        while len(right_context) < max_context_length:
            right_context.append(';')
        left_context_ids = []
        right_context_ids = []
        for l in left_context:
            try:
                left_context_ids.append(stoi[l])
            except:
                left_context_ids.append(stoi['<unk>'])
        for r in right_context:
            try:
                right_context_ids.append(stoi[r])
            except:
                right_context_ids.append(stoi['<unk>'])
        input_train_data[index,:] = left_context_ids + right_context_ids

        left_context = [p[1] for p in sp[0]]
        right_context = [p[1] for p in sp[1]]
        if len(left_context) > max_context_length:
            left_context = left_context[-max_context_length:]
        if len(right_context) > max_context_length:
            right_context = right_context[0:max_context_length]
        while len(left_context) < max_context_length:
            left_context.insert(0, 'PUNC')
        while len(right_context) < max_context_length:
            right_context.append('PUNC')
        left_context_ids = []
        right_context_ids = []
        for l in left_context:
            try:
                left_context_ids.append(stoi_pos[l])
            except:
                left_context_ids.append(stoi_pos['<unk>'])
        for r in right_context:
            try:
                right_context_ids.append(stoi_pos[r])
            except:
                right_context_ids.append(stoi_pos['<unk>'])
        input_pos_data[index,:] = left_context_ids + right_context_ids

        # left_context = [p[2] for p in sp[0]]
        # right_context = [p[2] for p in sp[1]]
        # if len(left_context) > max_context_length:
        #     left_context = left_context[-max_context_length:]
        # if len(right_context) > max_context_length:
        #     right_context = right_context[0:max_context_length]
        # while len(left_context) < max_context_length:
        #     left_context.insert(0, 'O')
        # while len(right_context) < max_context_length:
        #     right_context.append('O')
        # left_context_ids = []
        # right_context_ids = []
        # for l in left_context:
        #     try:
        #         left_context_ids.append(stoi_ner[l])
        #     except:
        #         left_context_ids.append(stoi_ner['<unk>'])
        # for r in right_context:
        #     try:
        #         right_context_ids.append(stoi_ner[r])
        #     except:
        #         right_context_ids.append(stoi_ner['<unk>'])
        # input_ner_data[index,:] = left_context_ids + right_context_ids

        input_target[index] = 0
        index += 1
        if index >= input_train_data.shape[0]:
            break

    return input_train_data, input_pos_data, input_target

def inference_cut_sentence(paragraph, model, stoi, stoi_pos, max_context_length=5, return_raw=False):
    chunks =  pos_tag(paragraph)
    # print(chunks)
    num2check = 0
    for c in chunks:
        if c[0] == '<space>':
            num2check += 1
    # print(num2check)
    test_data = np.zeros([num2check, max_context_length*2])
    test_data_pos = np.zeros([num2check, max_context_length*2])
    # test_data_ner = np.zeros([num2check, max_context_length*2])

    index = 0
    for i, c in enumerate(chunks):
        if c[0] == '<space>':
            left = chunks[max(i-max_context_length,0):i]
            right = chunks[i+1:min(i+max_context_length+1,len(chunks))]

            left_context = [p[0] for p in left]
            right_context = [p[0] for p in right]
            while len(left_context) < max_context_length:
                left_context.insert(0, ';')
            while len(right_context) < max_context_length:
                right_context.append(';')
            left_context_ids = []
            right_context_ids = []
            for l in left_context:
                try:
                    left_context_ids.append(stoi[l])
                except:
                    left_context_ids.append(stoi['<unk>'])
            for r in right_context:
                try:
                    right_context_ids.append(stoi[r])
                except:
                    right_context_ids.append(stoi['<unk>'])
            test_data[index,:] = left_context_ids + right_context_ids

            left_context = [p[1] for p in left]
            right_context = [p[1] for p in right]
            while len(left_context) < max_context_length:
                left_context.insert(0, 'PUNC')
            while len(right_context) < max_context_length:
                right_context.append('PUNC')
            left_context_ids = []
            right_context_ids = []
            for l in left_context:
                try:
                    left_context_ids.append(stoi_pos[l])
                except:
                    left_context_ids.append(stoi_pos['<unk>'])
            for r in right_context:
                try:
                    right_context_ids.append(stoi_pos[r])
                except:
                    right_context_ids.append(stoi_pos['<unk>'])
            test_data_pos[index,:] = left_context_ids + right_context_ids

            # left_context = [p[2] for p in left]
            # right_context = [p[2] for p in right]
            # while len(left_context) < max_context_length:
            #     left_context.insert(0, 'O')
            # while len(right_context) < max_context_length:
            #     right_context.append('O')
            # left_context_ids = []
            # right_context_ids = []
            # for l in left_context:
            #     left_context_ids.append(stoi_ner[l])
            # for r in right_context:
            #     right_context_ids.append(stoi_ner[r])
            # test_data_ner[index,:] = left_context_ids + right_context_ids

            index += 1

    # y_pred = np.round(model.predict([test_data, test_data_pos, test_data_ner]))
    # y_pred = np.round(model.predict([test_data, test_data_pos]))
    # print(y_pred)
    y_pred = np.round(model.forward(torch.tensor(test_data, dtype=torch.long), torch.tensor(test_data_pos, dtype=torch.long)).detach().cpu().numpy())
    # print(y_pred)
    y_pred = np.argmax(y_pred, axis=1)

    row = 0
    previous_space = 0
    sentence_ans = ""
    sentences_ans = []
    for i, c in enumerate(chunks):
        if c[0] == '<space>' and y_pred[row] == 0:
            tokens = [ p[0] for p in chunks[previous_space:i] ]
            x = "".join(tokens)
            previous_space = i+1
            sentence_ans += x + " "
            row += 1
        elif c[0] == '<space>' and y_pred[row] == 1:
            tokens = [ p[0] for p in chunks[previous_space:i] ]
            x = "".join(tokens)
            previous_space = i+1
            sentence_ans += x + " "
            sentences_ans.append(sentence_ans.strip())
            sentence_ans = ""
            row += 1
        if row == num2check and i == len(chunks)-1:
            tokens = [ p[0] for p in chunks[previous_space:] ]
            x = "".join(tokens)
            previous_space = i+1
            sentence_ans += x + " "
            sentences_ans.append(sentence_ans.strip())

    if not return_raw:
        return sentences_ans
    else:
        return [sentences_ans, y_pred]