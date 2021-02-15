# %%
import xml.etree.ElementTree as ET
from h5py._hl.filters import CHUNK_BASE
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
positive_examples_all = []
negative_examples_all = []

CHUNK_SIZE = 5 # maximum number of sentences in one paragraph, if paragraph is longer than this, cut it.

for lv1 in root:
    if lv1.tag == 'document':
        for lv2 in lv1:
            if lv2.tag == 'paragraph':
                sentencesInSameParagraph = []
                sentence_pairs = []
                for s in lv2:
                    sentence = s.get('raw_txt')
                    sentencesInSameParagraph.append(sentence)
                
                # get pairs of sentence
                for i in range(0,len(sentencesInSameParagraph)-1):
                    sentence_pairs.append( (sentencesInSameParagraph[i], sentencesInSameParagraph[i+1]) )

                num_chunks = len(sentencesInSameParagraph) // CHUNK_SIZE
                start_single = 0
                start_pair = 0
                while (start_single <= len(sentencesInSameParagraph)-CHUNK_SIZE):
                    sentencesInSameParagraph_c  = sentencesInSameParagraph[start_single:start_single+CHUNK_SIZE]
                    sentence_pairs_c = sentence_pairs[start_pair:start_pair+CHUNK_SIZE-1]
                    positive_examples, negative_examples = genTrainingExamples(sentence_pairs, sentencesInSameParagraph, max_context_length=MAX_CONTEXT_LENGTH)
                    positive_examples_all += positive_examples
                    negative_examples_all += negative_examples
                    start_single += CHUNK_SIZE
                    start_pair += CHUNK_SIZE

# %%
with open('positive_examples.pickle', 'rb') as f:
    positive_examples_all = pickle.load(f)

with open('negative_examples.pickle', 'rb') as f:
    negative_examples_all = pickle.load(f)

print(len(negative_examples_all))
print(len(positive_examples_all))

# %%
unique_tokens, unique_pos = build_vocabs(positive_examples_all,negative_examples_all)
VOCAB_SIZE = len(unique_tokens)
print(VOCAB_SIZE)
# my_lst = list(unique_tokens)
# print(my_lst[0:100])

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

cb = ModelCheckpoint("cut_sentence.h5", save_best_only=True)

model.fit([X_train, X_pos_train], y_train,
    validation_data=([X_test, X_pos_test], y_test),
    batch_size=128, shuffle=True, class_weight=class_weight, epochs=5, callbacks=[cb])

with open("stoi.pickle", "wb") as f:
    pickle.dump(stoi, f);

with open("stoi_pos.pickle", "wb") as f:
    pickle.dump(stoi_pos, f);

# confusion matrix and classification report
model_loaded = load_model("cut_sentence.h5")
y_pred = np.round(model_loaded.predict([X_test, X_pos_test]))

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred, target_names=['no cut','cut']))

# %%
# -------------------------inference--------------------------------
test1 = "ในปลายปี 2529 กระทรวงวิทยาศาสตร์ เทคโนโลยีและการพลังงาน โดยมติคณะรัฐมนตรีได้จัดตั้งศูนย์เทคโนโลยีอิเล็กทรอนิกส์และคอมพิวเตอร์แห่งชาติขึ้น เพื่อพัฒนาเทคโนโลยีอิเล็กทรอนิกส์ในประเทศ และเทคโนโลยีด้านคอมพิวเตอร์ทั้งซอฟต์แวร์และฮาร์ดแวร์ โดยการสนับสนุนให้มีการวิจัยและพัฒนาในด้านนี้ จนถึงขั้นพัฒนาผลของการวิจัยและพัฒนาไปสู่การผลิตในเชิงอุตสาหกรรมและพาณิชย์ ตลอดจนสามารถแข่งขันได้ในตลาดภายในและต่างประเทศ"
test2 = "งานวิจัยขั้นต่อไปจะเป็นการพัฒนา PC ขนาดกลาง ซึ่งมีจำนวน I/O ขนาดสูงสุด 256 จุด สามารถรับ Input จำพวก Analog High Speed Pulse Thumbwheel ฯลฯ ความเร็วเฉลี่ยของแต่ละคำสั่งมีค่าลดลงเหลือประมาณ 8-10 usec. โครงสร้างของระบบจะเป็นแบบโมดูล ทำให้ผู้ใช้สามารถกำหนดขนาดและชนิดของ I/O ได้ตามความเหมาะสมของงาน"
test3 = "จากรากฐานทางเทคโนโลยีเดิมที่มีอยู่ รวมกับเทคโนโลยีใหม่ ทั้งด้านฮาร์ดแวร์และซอฟต์แวร์ที่รุดหน้าไปทุกวัน คณะผู้วิจัยได้พัฒนาระบบภาษาไทยระดับแก่นเป็นรูปแบบ System Call ที่เป็นมาตรฐานร่วมบนเครื่องไมโครคอมพิวเตอร์ และพร้อมที่จะขยายไปติดตั้งบนเครื่องคอมพิวเตอร์ในระดับที่สูงขึ้นของเวอร์กสเตชั่น มินิและเมนเฟรมในอนาคตอันใกล้นี้"
test4 = "ทั้งนี้ หลังจากที่คณะกรรมการกิจการกระจายเสียง กิจการโทรทัศน์ และกิจการโทรคมนาคมแห่งชาติ หรือ กสทช. ได้จัดงานประมูลคลื่น 5 จี ขึ้นเมื่อวันที่ 16 ก.พ.2563 เอไอเอสได้คลื่นความถี่แบรนด์ 41 (TDD, 2600 MHz) รวม 100 MHz (10 ใบอนุญาต) และทรูมูฟเอช ได้รวม 90 MHz (9 ใบอนุญาต) Opensignal พบว่า ระหว่างวันที่ 1 เม.ย.-30 มิ.ย.2563 ทั้งเอไอเอสและทรูมูฟเอช ได้ใช้คลื่น 2600 MHz ที่ได้มาใหม่จำนวน 20-40 MHz สำหรับให้บริการ 4 จีในบางพื้นที่ ทำให้ผู้ใช้คลื่นความถี่ Band 41 ได้รับประสบการณ์ความเร็วในการดาวน์โหลด 4 จี ดีกว่าอย่างเห็นได้ชัดทั้งบนเครือข่ายของเอไอเอสและทรูมูฟเอช"

paragraph = test4
print(inference_cut_sentence(paragraph, model_loaded, stoi, stoi_pos, max_context_length=5))
# %%
import tensorflow as tf
tf.keras.utils.plot_model(model, to_file='./my_model.png', show_shapes=True)
# %%
