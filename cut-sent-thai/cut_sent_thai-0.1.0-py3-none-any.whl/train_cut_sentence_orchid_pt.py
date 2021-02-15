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
from tqdm import tqdm
# ner = ThaiNameTagger()
MAX_CONTEXT_LENGTH = 5

word2vec_model = word_vector.get_model()
root = ET.parse('xmlchid.xml').getroot()

# %%
# skip this cell if loading from pickle
positive_examples_all = []
negative_examples_all = []

CHUNK_SIZE = 5 # maximum number of sentences in one paragraph, if paragraph is longer than this, cut it.

for lv1 in tqdm(root):
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

with open('positive_examples.pickle', 'wb') as f:
    pickle.dump(positive_examples_all, f)

with open('negative_examples.pickle', 'wb') as f:
    pickle.dump(negative_examples_all, f)

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
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.nn.functional as F
from pytorch_lightning.metrics import F1
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import f1_score
from torch.utils.data import Dataset, DataLoader
# %%
# DataSets
class Mydata(Dataset):
    def __init__(self, toks, pos, labels):
        super().__init__()
        self.toks = toks # 2D numpy
        self.pos = pos
        self.labels = labels # 1D numpy

    def __len__(self):
        return self.toks.shape[0]

    def __getitem__(self, idx):
        return (
            torch.tensor(self.toks[idx,:], dtype=torch.long),
            torch.tensor(self.pos[idx,:], dtype=torch.long),
            torch.tensor(self.labels[idx], dtype=torch.long)
        )

train_dataset = Mydata(X_train, X_pos_train, y_train)
test_dataset = Mydata(X_test, X_pos_test, y_test)

# dataloader
batch_size = 128
train_dataloader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    num_workers = 32,
    shuffle=True
)
test_dataloader = DataLoader(
    test_dataset,
    batch_size=32,
    num_workers = 32,
    shuffle=False
)

# %%
# check the dataloader
for i, batch in enumerate(train_dataloader):
    tok, pos, label = batch
    print(tok)
    print(pos)
    print(label)
    break
# %%
# model
EMDEDDING_DIM = 150
POS_DIM = 50
FC_DIM = 512
LSTM_DIM = 512
DROP = 0.5
class CutSentModel(pl.LightningModule):
    def __init__(self):
        super().__init__()

        self.embedding_tok = nn.Embedding(
            num_embeddings=VOCAB_SIZE,
            embedding_dim=EMDEDDING_DIM,
        )

        self.embedding_pos = nn.Embedding(
            num_embeddings=len(unique_pos),
            embedding_dim=POS_DIM,
        )

        self.lstm = nn.LSTM(EMDEDDING_DIM+POS_DIM, LSTM_DIM, 
            batch_first=True,
            bidirectional=False)

        self.fc1 = nn.Linear(LSTM_DIM, FC_DIM)
        self.drop = nn.Dropout(p=DROP)
        self.fc2 = nn.Linear(FC_DIM, 2)

        self.val_preds = []
        self.val_labels = []

    def forward(self, toks, pos):
        x1 = self.embedding_tok(toks) # 32x10x150
        x2 = self.embedding_pos(pos) # 32x10x50
        x = torch.cat((x1,x2), dim=2) # 32x10x200
        out, (hidden, cell) = self.lstm(x)
        out = out[:,-1,:] # get h at the last timestep (time is axis 1 if batch_first=True)
        x = F.relu(self.fc1(out)) 
        x = self.drop(x)
        y = F.softmax(self.fc2(x))
        return y

    def training_step(self, batch, idx):
        toks, pos, labels = batch
        x1 = self.embedding_tok(toks) # 32x10x150
        x2 = self.embedding_pos(pos) # 32x10x50
        x = torch.cat((x1,x2), dim=2) # 32x10x200
        # x = torch.nn.LayerNorm(200)(x)
        out, (hidden, cell) = self.lstm(x)
        out = out[:,-1,:] # get h at the last timestep (time is axis 1 if batch_first=True)
        x = F.relu(self.fc1(out)) 
        x = self.drop(x)
        y = self.fc2(x)
        loss = nn.CrossEntropyLoss()(y, labels)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, idx):
        toks, pos, labels = batch
        x1 = self.embedding_tok(toks) # 32x10x150
        x2 = self.embedding_pos(pos) # 32x10x50
        x = torch.cat((x1,x2), dim=2) # 32x10x200
        out, (hidden, cell) = self.lstm(x)
        out = out[:,-1,:] # get h at the last timestep (time is axis 1 if batch_first=True)
        x = F.relu(self.fc1(out)) 
        y = self.fc2(x)
        loss = nn.CrossEntropyLoss()(y, labels)
        self.log('val_loss', loss)
        pred = F.softmax(y, dim=1) # 2D tensor
        pred = torch.argmax(pred, dim=1) # 1D tensor
        self.val_preds.append(pred) # list of 1D tensors
        self.val_labels.append(labels) # list of 1D tensors

    def on_validation_epoch_start(self):
        self.val_preds = []
        self.val_labels = []

    def on_validation_epoch_end(self):
        preds_all = []
        labels_all = []

        for p in self.val_preds:
            pred_cpu = p.detach().cpu().numpy()
            pred_cpu = pred_cpu.tolist()
            preds_all += pred_cpu

        for l in self.val_labels:
            label_cpu = l.detach().cpu().numpy()
            label_cpu = label_cpu.tolist()
            labels_all += label_cpu

        # calculate the F1 score for the whole epoch
        f1 = f1_score(labels_all, preds_all, average='binary')
        self.log('f1_score', f1, sync_dist=True)


    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=0.02, weight_decay=1e-4)
        scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.02, epochs=20, steps_per_epoch=330)
        return [optimizer], [scheduler]

# %%
early_stopping = EarlyStopping('f1_score', mode='max')
checkpoint_callback = ModelCheckpoint(
    dirpath='lighting_checkpoint',
    filename='{epoch}-{val_loss:.2f}-{f1_score:.2f}',
    monitor='f1_score',
    mode='max'
)
# %%
pl.seed_everything(0)
model = CutSentModel()
trainer = pl.Trainer(max_epochs=20, callbacks=[early_stopping, checkpoint_callback], gpus=1)
trainer.fit(model, train_dataloader, test_dataloader)
# %%
model_new = CutSentModel.load_from_checkpoint('lighting_checkpoint/epoch=6-val_loss=0.36-f1_score=0.90.ckpt')
model_new.eval()
script = model.to_torchscript()
torch.jit.save(script, "cut_sentence.pt")
# %%
with open("stoi.pickle", "wb") as f:
    pickle.dump(stoi, f);

with open("stoi_pos.pickle", "wb") as f:
    pickle.dump(stoi_pos, f);
# %%
