# %%
import xml.etree.ElementTree as ET
from pythainlp import word_vector
import numpy as np
import random
# from pythainlp.tag.named_entity import ThaiNameTagger
from cut_sent_utils import genTrainingExamples, build_vocabs
from cut_sent_utils import build_dictionaries, create_training_data, inference_cut_sentence
import pickle
import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"
# ner = ThaiNameTagger()
MAX_CONTEXT_LENGTH = 5

word2vec_model = word_vector.get_model()
root = ET.parse('xmlchid.xml').getroot()

# %%
words = []
pos_tags = []
cut = []

for lv1 in root:
    if lv1.tag == 'document':
        for lv2 in lv1:
            if lv2.tag == 'paragraph':
                for i, lv3 in enumerate(lv2): # sentences
                    if lv3.tag == 'sentence':
                        for j, lv4 in enumerate(lv3): # words
                            word = lv4.get('surface')
                            pos = lv4.get('pos')
                            if j == 0 and i >= 1: # if it's the first word in a sentence and there is a previous sentence in this paragraph
                                # insert a space (artificial, not part of the corpus) between two sentences
                                words.append('<space>') 
                                pos_tags.append('PUNC')
                                cut.append(1) # 1 is for cut

                                # insert the actual first word of the sentence
                                words.append(word) 
                                pos_tags.append(pos)
                                cut.append(0) # 0 is for not cut
                            elif j >= 1 and i >= 1: # every other words in the sentence that's not the first word
                                words.append(word) 
                                pos_tags.append(pos)
                                cut.append(0) # 0 is for not cut
                            elif i == 0: # the first sentence in the paragraph
                                words.append(word) 
                                pos_tags.append(pos)
                                cut.append(0) # 0 is for not cut

# %%
max_context_length = 5
positive_examples = []
negative_examples = []

for i, w in enumerate(words):
    if w == '<space>':
        idxs = range(max(i-max_context_length,0),i)
        left = []
        for k in idxs:
            left.append((words[k], pos_tags[k]))

        idxs = range(i+1, min(i+max_context_length+1,len(words)))
        right = []
        for k in idxs:
            right.append((words[k], pos_tags[k]))

        if cut[i] == 1:
            positive_examples.append([left , right])
        else:
            negative_examples.append([left , right])
# %%
import copy
positive_examples_all = copy.deepcopy(positive_examples)
negative_examples_all = copy.deepcopy(negative_examples)
print(len(negative_examples_all))
print(len(positive_examples_all))

# %%
unique_tokens, unique_pos = build_vocabs(positive_examples_all,negative_examples_all)
VOCAB_SIZE = len(unique_tokens)
print(VOCAB_SIZE)

# %%
# build dictionary
stoi, itos, stoi_pos, itos_pos = build_dictionaries(unique_tokens, unique_pos)

# %%
input_train_data, input_pos_data, input_target = create_training_data(
    positive_examples_all,
    negative_examples_all,
    stoi, itos, stoi_pos, itos_pos,
    balanced=True, max_context_length=5
)

# %%
# shuffle the training data
shuffled_row_index = [i for i in range(len(positive_examples_all) + len(positive_examples_all))]
random.shuffle(shuffled_row_index)
input_train_data = input_train_data[shuffled_row_index,:]
input_pos_data = input_pos_data[shuffled_row_index,:]
# input_ner_data = input_ner_data[shuffled_row_index,:]
input_target = input_target[shuffled_row_index]

# train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, X_pos_train, X_pos_test, y_train, y_test = train_test_split(
    input_train_data, input_pos_data, input_target, test_size=0.33, random_state=42)

# %%
# build model
from tensorflow.keras.layers import Dense, Embedding, Input, LSTM, Bidirectional, Dropout, concatenate, BatchNormalization, LayerNormalization
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam, RMSprop, SGD
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import BinaryCrossentropy

EMDEDDING_DIM = 150
input = Input(shape=(MAX_CONTEXT_LENGTH*2,)) # CONTEXT_SIZE is half of actual context
input_pos = Input(shape=(MAX_CONTEXT_LENGTH*2,)) # CONTEXT_SIZE is half of actual context
# input_ner = Input(shape=(MAX_CONTEXT_LENGTH*2,)) # CONTEXT_SIZE is half of actual context

x = Embedding(VOCAB_SIZE, EMDEDDING_DIM, input_length=MAX_CONTEXT_LENGTH*2, name='embedding_tok')(input)
x = Model(input, x)

y = Embedding(len(unique_pos), 50, input_length=MAX_CONTEXT_LENGTH*2, name='embedding_pos')(input_pos)
y = Model(input_pos,y)

# z = Embedding(len(unique_ner), 50, input_length=MAX_CONTEXT_LENGTH*2, name='embedding_ner')(input_ner)
# z = Model(input_ner,z)

# combined = concatenate([x.output,y.output,z.output], axis=2)
combined = concatenate([x.output,y.output], axis=2)
out = LayerNormalization(axis=2)(combined)
# out = LSTM(100, return_sequences=False)(out) 
out = Bidirectional(LSTM(512, return_sequences=False))(out) 
out = Dense(512, activation='relu')(out)
out = Dropout(0.5)(out)
out = Dense(1, activation='sigmoid')(out)

model = Model([x.input, y.input], out)
model.compile(optimizer=Adam(learning_rate=5e-4), loss=BinaryCrossentropy(label_smoothing=0.15), metrics=[tf.keras.metrics.TruePositives()])
# model.compile(optimizer=SGD(learning_rate=5e-4, momentum=0.9, nesterov=True), loss='binary_crossentropy', metrics=[tf.keras.metrics.AUC()])
model.summary()

class_weight = {
    0: 1,
    1: 1
}

cb = ModelCheckpoint("cut_sentence_perfect_tokens.h5", save_best_only=True)

model.fit([X_train, X_pos_train], y_train,
    validation_data=([X_test, X_pos_test], y_test),
    batch_size=128, shuffle=True, class_weight=class_weight, epochs=5, callbacks=[cb])

with open("stoi.pickle", "wb") as f:
    pickle.dump(stoi, f);

with open("stoi_pos.pickle", "wb") as f:
    pickle.dump(stoi_pos, f);

# confusion matrix and classification report
model_loaded = load_model("cut_sentence_perfect_tokens.h5")
y_pred = np.round(model_loaded.predict([X_test, X_pos_test]))

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred, target_names=['no cut','cut']))
# %%
