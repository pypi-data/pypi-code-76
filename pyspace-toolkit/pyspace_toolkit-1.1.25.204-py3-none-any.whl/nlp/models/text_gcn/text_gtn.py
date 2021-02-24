# %%
# from layers import *
# from metrics import *

import numpy as np
import tensorflow as tf2
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()

# %%
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import math
from matplotlib import pyplot as plt
import pdb


class GTN(nn.Module):
    
    def __init__(self, num_edge, num_channels, w_in, w_out, num_class,num_layers,norm):
        super(GTN, self).__init__()
        self.num_edge = num_edge
        self.num_channels = num_channels
        self.w_in = w_in
        self.w_out = w_out
        self.num_class = num_class
        self.num_layers = num_layers
        self.is_norm = norm
        layers = []
        for i in range(num_layers):
            if i == 0:
                layers.append(GTLayer(num_edge, num_channels, first=True))
            else:
                layers.append(GTLayer(num_edge, num_channels, first=False))
        self.layers = nn.ModuleList(layers)
        self.weight = nn.Parameter(torch.Tensor(w_in, w_out))
        self.bias = nn.Parameter(torch.Tensor(w_out))
        self.loss = nn.CrossEntropyLoss()
        self.linear1 = nn.Linear(self.w_out*self.num_channels, self.w_out)
        self.linear2 = nn.Linear(self.w_out, self.num_class)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.weight)
        nn.init.zeros_(self.bias)

    def gcn_conv(self,X,H):
        X = torch.mm(X, self.weight)
        H = self.norm(H, add=True)
        return torch.mm(H.t(),X)

    def normalization(self, H):
        for i in range(self.num_channels):
            if i==0:
                H_ = self.norm(H[i,:,:]).unsqueeze(0)
            else:
                H_ = torch.cat((H_,self.norm(H[i,:,:]).unsqueeze(0)), dim=0)
        return H_

    def norm(self, H, add=False):
        H = H.t()
        if add == False:
            H = H*((torch.eye(H.shape[0])==0).type(torch.FloatTensor))
        else:
            H = H*((torch.eye(H.shape[0])==0).type(torch.FloatTensor)) + torch.eye(H.shape[0]).type(torch.FloatTensor)
        deg = torch.sum(H, dim=1)
        deg_inv = deg.pow(-1)
        deg_inv[deg_inv == float('inf')] = 0
        deg_inv = deg_inv*torch.eye(H.shape[0]).type(torch.FloatTensor)
        H = torch.mm(deg_inv,H)
        H = H.t()
        return H

    def forward(self, A, X, target_x, target):
        A = A.unsqueeze(0).permute(0,3,1,2) 
        Ws = []
        for i in range(self.num_layers):
            if i == 0:
                H, W = self.layers[i](A)
            else:
                H = self.normalization(H)
                H, W = self.layers[i](A, H)
            Ws.append(W)
        
        #H,W1 = self.layer1(A)
        #H = self.normalization(H)
        #H,W2 = self.layer2(A, H)
        #H = self.normalization(H)
        #H,W3 = self.layer3(A, H)
        for i in range(self.num_channels):
            if i==0:
                X_ = F.relu(self.gcn_conv(X,H[i]))
            else:
                X_tmp = F.relu(self.gcn_conv(X,H[i]))
                X_ = torch.cat((X_,X_tmp), dim=1)
        X_ = self.linear1(X_)
        X_ = F.relu(X_)
        y = self.linear2(X_[target_x])
        loss = self.loss(y, target)
        return loss, y, Ws

class GTLayer(nn.Module):
    
    def __init__(self, in_channels, out_channels, first=True):
        super(GTLayer, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.first = first
        if self.first == True:
            self.conv1 = GTConv(in_channels, out_channels)
            self.conv2 = GTConv(in_channels, out_channels)
        else:
            self.conv1 = GTConv(in_channels, out_channels)
    
    def forward(self, A, H_=None):
        if self.first == True:
            a = self.conv1(A)
            b = self.conv2(A)
            H = torch.bmm(a,b)
            W = [(F.softmax(self.conv1.weight, dim=1)).detach(),(F.softmax(self.conv2.weight, dim=1)).detach()]
        else:
            a = self.conv1(A)
            H = torch.bmm(H_,a)
            W = [(F.softmax(self.conv1.weight, dim=1)).detach()]
        return H,W

class GTConv(nn.Module):
    
    def __init__(self, in_channels, out_channels):
        super(GTConv, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.weight = nn.Parameter(torch.Tensor(out_channels,in_channels,1,1))
        self.bias = None
        self.scale = nn.Parameter(torch.Tensor([0.1]), requires_grad=False)
        self.reset_parameters()
    def reset_parameters(self):
        n = self.in_channels
        nn.init.constant_(self.weight, 0.1)
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, A):
        A = torch.sum(A*F.softmax(self.weight, dim=1), dim=1)
        return A

################################################################################################
################################################################################################
################################################################################################
################################################################################################

import os
import sys

import time
import datetime
import random
import pickle as pkl
from math import log

import nltk
from nltk.corpus import stopwords
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

import numpy as np
import scipy.sparse as sp

from sklearn import metrics

# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()

# from models import GCN

# import networkx as nx
# from sklearn import svm
# from sklearn.feature_extraction.text import TfidfVectorizer
# from scipy.spatial.distance import cosine


class TextGTN_TransductiveClassifier:
    
    def __init__(self, verbose=1, output_folder='./'):
        
        self.verbose = verbose
        output_folder = output_folder + '/' if output_folder[-1] != '/' else output_folder
        self.output_folder = output_folder
        
        self.model_date = datetime.datetime.now().strftime('%Y%m%d__%H%M')
        
        # nltk.download('stopwords')
        # self.stop_words = set(stopwords.words('english'))
        pass
      
    def prepare_input_data(self, ):
        
        meta_data_list = []
        for i in range(len(self.sentences)):
            meta = str(i) + '\t' + self.train_or_test_list[i] + '\t' + self.labels[i]
            meta_data_list.append(meta)
            
        ##########################################################
        
        self.meta_data_list = meta_data_list
        
    def clean_input_data(self, ):
        
        doc_content_list = self.sentences

        ##########################################################
        
        # def clean_str(string):
        #     """
        #     Tokenization/string cleaning for all datasets except for SST.
        #     Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
        #     """
        #     string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        #     string = re.sub(r"\'s", " \'s", string)
        #     string = re.sub(r"\'ve", " \'ve", string)
        #     string = re.sub(r"n\'t", " n\'t", string)
        #     string = re.sub(r"\'re", " \'re", string)
        #     string = re.sub(r"\'d", " \'d", string)
        #     string = re.sub(r"\'ll", " \'ll", string)
        #     string = re.sub(r",", " , ", string)
        #     string = re.sub(r"!", " ! ", string)
        #     string = re.sub(r"\(", " \( ", string)
        #     string = re.sub(r"\)", " \) ", string)
        #     string = re.sub(r"\?", " \? ", string)
        #     string = re.sub(r"\s{2,}", " ", string)
        #     return string.strip().lower()

        ##########################################################
        
        word_freq = {}  # to remove rare words

        for doc_content in doc_content_list:
            # temp = clean_str(doc_content)
            temp = doc_content
            words = temp.split()
            for word in words:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1

        clean_docs = []
        for doc_content in doc_content_list:
            # temp = clean_str(doc_content)
            temp = doc_content
            words = temp.split()
            doc_words = []
            for word in words:
                # word not in stop_words and word_freq[word] >= 5
                if True:
                    doc_words.append(word)
                    continue

                if dataset == 'mr':
                    doc_words.append(word)
                elif word not in stop_words and word_freq[word] >= 5:
                    doc_words.append(word)

            doc_str = ' '.join(doc_words).strip()
            #if doc_str == '':
                #doc_str = temp
            clean_docs.append(doc_str)

        ##########################################################
        
        self.clean_docs = clean_docs
    
    def show_corpus_statistics(self, ):
        
        lines = self.clean_docs
        
        ##########################################################
        
        min_len = 10000
        aver_len = 0
        max_len = 0 
        
        for line in lines:
            line = line.strip()
            temp = line.split()
            aver_len = aver_len + len(temp)
            if len(temp) < min_len:
                min_len = len(temp)
            if len(temp) > max_len:
                max_len = len(temp)
        # f.close()
        aver_len = 1.0 * aver_len / len(lines)
        print('    > min_len : ' + str(min_len))
        print('    > max_len : ' + str(max_len))
        print('    > average_len : ' + str(aver_len))
    
    def shuffle_input_data(self, ):
        
        
        lines = self.meta_data_list
        doc_content_list = self.clean_docs
        
        ##########################################################
        
        # shulffing
        doc_name_list = []
        doc_train_list = []
        doc_test_list = []

        for line in lines:
            doc_name_list.append(line.strip())
            temp = line.split("\t")
            if temp[1].find('test') != -1:
                doc_test_list.append(line.strip())
            elif temp[1].find('train') != -1:
                doc_train_list.append(line.strip())
                

        train_ids = []
        for train_name in doc_train_list:
            train_id = doc_name_list.index(train_name)
            train_ids.append(train_id)
        random.shuffle(train_ids)

        test_ids = []
        for test_name in doc_test_list:
            test_id = doc_name_list.index(test_name)
            test_ids.append(test_id)
        random.shuffle(test_ids)

        ids = train_ids + test_ids
        
        shuffle_doc_name_list = []
        shuffle_doc_words_list = []
        for id in ids:
            shuffle_doc_name_list.append(doc_name_list[int(id)])
            shuffle_doc_words_list.append(doc_content_list[int(id)])
        shuffle_doc_name_str = '\n'.join(shuffle_doc_name_list)
        shuffle_doc_words_str = '\n'.join(shuffle_doc_words_list)

        
        ##########################################################
        
        self.shuffle_doc_name_list = shuffle_doc_name_list
        self.shuffle_doc_words_list = shuffle_doc_words_list
        
        self.train_ids = train_ids
        self.test_ids = test_ids
        self.ids = ids
        
        test_size = len(test_ids)
        self.test_size = test_size
      
    def build_vocab(self,):
        
        shuffle_doc_name_list = self.shuffle_doc_name_list
        shuffle_doc_words_list = self.shuffle_doc_words_list
        
        ##########################################################
        
        # build vocab
        word_freq = {}
        word_set = set()
        for doc_words in shuffle_doc_words_list:
            words = doc_words.split()
            for word in words:
                word_set.add(word)
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1

        vocab = list(word_set)
        vocab_size = len(vocab)

        word_doc_list = {}

        for i in range(len(shuffle_doc_words_list)):
            doc_words = shuffle_doc_words_list[i]
            words = doc_words.split()
            appeared = set()
            for word in words:
                if word in appeared:
                    continue
                if word in word_doc_list:
                    doc_list = word_doc_list[word]
                    doc_list.append(i)
                    word_doc_list[word] = doc_list
                else:
                    word_doc_list[word] = [i]
                appeared.add(word)

        word_doc_freq = {}
        for word, doc_list in word_doc_list.items():
            word_doc_freq[word] = len(doc_list)

        word_id_map = {}
        for i in range(vocab_size):
            word_id_map[vocab[i]] = i

            
        ##########################################################
            
        self.vocab_size = vocab_size
        self.vocab = vocab
        
        self.word_doc_freq = word_doc_freq
        self.word_id_map = word_id_map

    def build_labels(self,):
        
        shuffle_doc_name_list = self.shuffle_doc_name_list
        
        ##########################################################
        
        # label list
        label_set = set()
        for doc_meta in shuffle_doc_name_list:
            temp = doc_meta.split('\t')
            label_set.add(temp[2])
        label_list = list(label_set)

        
        ##########################################################
        
        self.label_list = label_list

    def set_validation(self, ):
        
        shuffle_doc_name_list = self.shuffle_doc_name_list
        train_ids = self.train_ids
        
        ##########################################################
        
        train_size = len(train_ids)
        val_size = int(self.validation_ratio * train_size)
        real_train_size = train_size - val_size 

        real_train_doc_names = shuffle_doc_name_list[:real_train_size]
        real_train_doc_names_str = '\n'.join(real_train_doc_names)

        ##########################################################
        
        self.real_train_size = real_train_size
        self.train_size = train_size
    
    def build_embeddings(self, ):
        
        # def loadWord2Vec(filename):
        #     """Read Word Vectors"""
        #     vocab = []
        #     embd = []
        #     word_vector_map = {}
        #     file = open(filename, 'r')
        #     for line in file.readlines():
        #         row = line.strip().split(' ')
        #         if(len(row) > 2):
        #             vocab.append(row[0])
        #             vector = row[1:]
        #             length = len(vector)
        #             for i in range(length):
        #                 vector[i] = float(vector[i])
        #             embd.append(vector)
        #             word_vector_map[row[0]] = vector
        #     print('Loaded Word Vectors!')
        #     file.close()
        #     return vocab, embd, word_vector_map
        
        # Read Word Vectors
        # word_vector_file = 'data/glove.6B/glove.6B.200d.txt'
        # vocab, embd, word_vector_map = loadWord2Vec(word_vector_file)
        # word_embeddings_dim = len(embd[0])
        
        # Read Word Vectors
        # word_vector_file = 'data/glove.6B/glove.6B.300d.txt'
        # word_vector_file = 'data/corpus/' + dataset + '_word_vectors.txt'
        #_, embd, word_vector_map = loadWord2Vec(word_vector_file)
        # word_embeddings_dim = len(embd[0])
        

        '''
        Word definitions begin
        '''
        '''
        definitions = []

        for word in vocab:
            word = word.strip()
            synsets = wn.synsets(clean_str(word))
            word_defs = []
            for synset in synsets:
                syn_def = synset.definition()
                word_defs.append(syn_def)
            word_des = ' '.join(word_defs)
            if word_des == '':
                word_des = '<PAD>'
            definitions.append(word_des)

        string = '\n'.join(definitions)


        f = open('data/corpus/' + dataset + '_vocab_def.txt', 'w')
        f.write(string)
        f.close()

        tfidf_vec = TfidfVectorizer(max_features=1000)
        tfidf_matrix = tfidf_vec.fit_transform(definitions)
        tfidf_matrix_array = tfidf_matrix.toarray()
        print(tfidf_matrix_array[0], len(tfidf_matrix_array[0]))

        word_vectors = []

        for i in range(len(vocab)):
            word = vocab[i]
            vector = tfidf_matrix_array[i]
            str_vector = []
            for j in range(len(vector)):
                str_vector.append(str(vector[j]))
            temp = ' '.join(str_vector)
            word_vector = word + ' ' + temp
            word_vectors.append(word_vector)

        string = '\n'.join(word_vectors)

        f = open('data/corpus/' + dataset + '_word_vectors.txt', 'w')
        f.write(string)
        f.close()

        word_vector_file = 'data/corpus/' + dataset + '_word_vectors.txt'
        _, embd, word_vector_map = loadWord2Vec(word_vector_file)
        word_embeddings_dim = len(embd[0])
        '''

        '''
        Word definitions end
        '''
        
        ##########################################################

        vocab_size = self.vocab_size
        vocab = self.vocab
        
        ##########################################################
        
        word_embeddings_dim = 300
        word_vector_map = {}
        
        
        word_vectors = np.random.uniform(-0.01, 0.01, (vocab_size, word_embeddings_dim))

        for i in range(len(vocab)):
            word = vocab[i]
            if word in word_vector_map:
                vector = word_vector_map[word]
                word_vectors[i] = vector
        
        ##########################################################
        
        self.word_embeddings_dim = word_embeddings_dim
        self.word_vector_map = word_vector_map
        self.word_vectors = word_vectors
    
    def build_x(self, ):
        
        real_train_size = self.real_train_size
        shuffle_doc_words_list = self.shuffle_doc_words_list
        
        word_embeddings_dim = self.word_embeddings_dim
        word_vector_map = self.word_vector_map
        
        ##########################################################
        
        # x: feature vectors of training docs, no initial features
        row_x = []
        col_x = []
        data_x = []
        for i in range(real_train_size):
            doc_vec = np.array([0.0 for k in range(word_embeddings_dim)])
            doc_words = shuffle_doc_words_list[i]
            words = doc_words.split()
            doc_len = len(words)
            for word in words:
                if word in word_vector_map:
                    word_vector = word_vector_map[word]
                    doc_vec = doc_vec + np.array(word_vector)

            for j in range(word_embeddings_dim):
                row_x.append(i)
                col_x.append(j)
                # np.random.uniform(-0.25, 0.25)
                data_x.append(doc_vec[j] / doc_len)  # doc_vec[j]/ doc_len

        # x = sp.csr_matrix((real_train_size, word_embeddings_dim), dtype=np.float32)
        x = sp.csr_matrix((data_x, (row_x, col_x)), shape=(real_train_size, word_embeddings_dim))

        ##########################################################
        
        self.x = x
        
    def build_y(self, ):
        
        
        real_train_size = self.real_train_size
        shuffle_doc_name_list = self.shuffle_doc_name_list
        label_list = self.label_list
                
        ##########################################################
        
        y = []
        for i in range(real_train_size):
            doc_meta = shuffle_doc_name_list[i]
            temp = doc_meta.split('\t')
            label = temp[2]
            one_hot = [0 for l in range(len(label_list))]
            label_index = label_list.index(label)
            one_hot[label_index] = 1
            y.append(one_hot)
        y = np.array(y)
        
        ##########################################################
        
        self.y = y
    
    def build_tx(self,):
        
        train_size = self.train_size
        test_size = self.test_size 
        
        shuffle_doc_words_list = self.shuffle_doc_words_list
        
        word_embeddings_dim = self.word_embeddings_dim
        word_vector_map = self.word_vector_map
        
        ##########################################################
        
        # tx: feature vectors of test docs, no initial features

        row_tx = []
        col_tx = []
        data_tx = []
        for i in range(test_size):
            doc_vec = np.array([0.0 for k in range(word_embeddings_dim)])
            doc_words = shuffle_doc_words_list[i + train_size]
            words = doc_words.split()
            doc_len = len(words)
            for word in words:
                if word in word_vector_map:
                    word_vector = word_vector_map[word]
                    doc_vec = doc_vec + np.array(word_vector)

            for j in range(word_embeddings_dim):
                row_tx.append(i)
                col_tx.append(j)
                # np.random.uniform(-0.25, 0.25)
                data_tx.append(doc_vec[j] / doc_len)  # doc_vec[j] / doc_len

        # tx = sp.csr_matrix((test_size, word_embeddings_dim), dtype=np.float32)
        tx = sp.csr_matrix((data_tx, (row_tx, col_tx)),shape=(test_size, word_embeddings_dim))

        ##########################################################
        
        self.tx = tx
        
    def build_ty(self,):
        
        train_size = self.train_size
        test_size = self.test_size 
        shuffle_doc_name_list = self.shuffle_doc_name_list
        label_list = self.label_list
        
        ##########################################################
        
        ty = []
        for i in range(test_size):
            doc_meta = shuffle_doc_name_list[i + train_size]
            temp = doc_meta.split('\t')
            label = temp[2]
            one_hot = [0 for l in range(len(label_list))]
            label_index = label_list.index(label)
            one_hot[label_index] = 1
            ty.append(one_hot)
        ty = np.array(ty)
        
        ##########################################################
        
        self.ty = ty

    def build_allx(self, ):
        
        word_vectors = self.word_vectors
        
        shuffle_doc_words_list = self.shuffle_doc_words_list
        
        word_embeddings_dim = self.word_embeddings_dim
        word_vector_map = self.word_vector_map
        
        train_size = self.train_size
        test_size = self.test_size
        
        vocab_size = self.vocab_size
        
        ##########################################################

        
        row_allx = []
        col_allx = []
        data_allx = []

        for i in range(train_size):
            doc_vec = np.array([0.0 for k in range(word_embeddings_dim)])
            doc_words = shuffle_doc_words_list[i]
            words = doc_words.split()
            doc_len = len(words)
            for word in words:
                if word in word_vector_map:
                    word_vector = word_vector_map[word]
                    doc_vec = doc_vec + np.array(word_vector)

            for j in range(word_embeddings_dim):
                row_allx.append(int(i))
                col_allx.append(j)
                # np.random.uniform(-0.25, 0.25)
                data_allx.append(doc_vec[j] / doc_len)  # doc_vec[j]/doc_len
        for i in range(vocab_size):
            for j in range(word_embeddings_dim):
                row_allx.append(int(i + train_size))
                col_allx.append(j)
                data_allx.append(word_vectors.item((i, j)))


        row_allx = np.array(row_allx)
        col_allx = np.array(col_allx)
        data_allx = np.array(data_allx)

        allx = sp.csr_matrix((data_allx, (row_allx, col_allx)), shape=(train_size + vocab_size, word_embeddings_dim))

        ##########################################################
        
        self.allx = allx
    
    def build_ally(self, ):
        
        train_size = self.train_size
        shuffle_doc_name_list = self.shuffle_doc_name_list
        label_list = self.label_list
        vocab_size = self.vocab_size
        
        ##########################################################
        
        ally = []
        for i in range(train_size):
            doc_meta = shuffle_doc_name_list[i]
            temp = doc_meta.split('\t')
            label = temp[2]
            one_hot = [0 for l in range(len(label_list))]
            label_index = label_list.index(label)
            one_hot[label_index] = 1
            ally.append(one_hot)

        for i in range(vocab_size):
            one_hot = [0 for l in range(len(label_list))]
            ally.append(one_hot)

        ally = np.array(ally)
        
        ##########################################################
        
        self.ally = ally
    
    def build_windows(self, ):
        
        shuffle_doc_words_list = self.shuffle_doc_words_list
        
        ##########################################################
        
        # word co-occurence with context windows
        window_size = 20
        windows = []

        for doc_words in shuffle_doc_words_list:
            words = doc_words.split()
            length = len(words)
            if length <= window_size:
                windows.append(words)
            else:
                # print(length, length - window_size + 1)
                for j in range(length - window_size + 1):
                    window = words[j: j + window_size]
                    windows.append(window)
                    # print(window)
        
        ##########################################################
        
        self.windows = windows
        
    def build_word_window_freq(self,):
        
        windows = self.windows
        
        ##########################################################
        
        word_window_freq = {}
        for window in windows:
            appeared = set()
            for i in range(len(window)):
                if window[i] in appeared:
                    continue
                if window[i] in word_window_freq:
                    word_window_freq[window[i]] += 1
                else:
                    word_window_freq[window[i]] = 1
                appeared.add(window[i])
                
        ##########################################################
        
        self.word_window_freq = word_window_freq

    def build_word_pair_count(self,):
        windows = self.windows
        word_id_map = self.word_id_map
        
        ##########################################################
        
        word_pair_count = {}
        for window in windows:
            for i in range(1, len(window)):
                for j in range(0, i):
                    word_i = window[i]
                    word_i_id = word_id_map[word_i]
                    word_j = window[j]
                    word_j_id = word_id_map[word_j]
                    if word_i_id == word_j_id:
                        continue
                    word_pair_str = str(word_i_id) + ',' + str(word_j_id)
                    if word_pair_str in word_pair_count:
                        word_pair_count[word_pair_str] += 1
                    else:
                        word_pair_count[word_pair_str] = 1
                    # two orders
                    word_pair_str = str(word_j_id) + ',' + str(word_i_id)
                    if word_pair_str in word_pair_count:
                        word_pair_count[word_pair_str] += 1
                    else:
                        word_pair_count[word_pair_str] = 1
                        
                        
        ##########################################################
        
        self.word_pair_count = word_pair_count
        
    def build_pmi(self,):
        
        train_size = self.train_size
        vocab = self.vocab
        windows = self.windows
        word_pair_count = self.word_pair_count
        word_window_freq = self.word_window_freq

        ##########################################################
        
        row = []
        col = []
        weight = []

        # pmi as weights

        num_window = len(windows)

        for key in word_pair_count:
            temp = key.split(',')
            i = int(temp[0])
            j = int(temp[1])
            count = word_pair_count[key]
            word_freq_i = word_window_freq[vocab[i]]
            word_freq_j = word_window_freq[vocab[j]]
            pmi = log((1.0 * count / num_window) /
                      (1.0 * word_freq_i * word_freq_j/(num_window * num_window)))
            if pmi <= 0:
                continue
            row.append(train_size + i)
            col.append(train_size + j)
            weight.append(pmi)

            
        ##########################################################
        
        # word vector cosine similarity as weights

        '''
        for i in range(vocab_size):
            for j in range(vocab_size):
                if vocab[i] in word_vector_map and vocab[j] in word_vector_map:
                    vector_i = np.array(word_vector_map[vocab[i]])
                    vector_j = np.array(word_vector_map[vocab[j]])
                    similarity = 1.0 - cosine(vector_i, vector_j)
                    if similarity > 0.9:
                        print(vocab[i], vocab[j], similarity)
                        row.append(train_size + i)
                        col.append(train_size + j)
                        weight.append(similarity)
        '''
        
        
        ##########################################################
        
        self.pmi_parameters = (row, col, weight)

    def build_doc_word_frequency(self,):
        
        shuffle_doc_words_list = self.shuffle_doc_words_list
        word_id_map = self.word_id_map
        
        ##########################################################
        
        # doc word frequency
        doc_word_freq = {}

        for doc_id in range(len(shuffle_doc_words_list)):
            doc_words = shuffle_doc_words_list[doc_id]
            words = doc_words.split()
            for word in words:
                word_id = word_id_map[word]
                doc_word_str = str(doc_id) + ',' + str(word_id)
                if doc_word_str in doc_word_freq:
                    doc_word_freq[doc_word_str] += 1
                else:
                    doc_word_freq[doc_word_str] = 1

        ##########################################################
        
        self.doc_word_freq = doc_word_freq
    
    def build_adj(self,):
        
        shuffle_doc_words_list = self.shuffle_doc_words_list
        word_id_map = self.word_id_map
        doc_word_freq = self.doc_word_freq
        vocab_size = self.vocab_size
        train_size = self.train_size
        vocab = self.vocab
        test_size= self.test_size
        word_doc_freq = self.word_doc_freq
        
        row, col, weight = self.pmi_parameters
        
        ##########################################################
        
        for i in range(len(shuffle_doc_words_list)):
            doc_words = shuffle_doc_words_list[i]
            words = doc_words.split()
            doc_word_set = set()
            for word in words:
                if word in doc_word_set:
                    continue
                j = word_id_map[word]
                key = str(i) + ',' + str(j)
                freq = doc_word_freq[key]
                if i < train_size:
                    row.append(i) # train
                else:
                    row.append(i - train_size + vocab_size + train_size) # test
                col.append(train_size + j)
                idf = log(1.0 * len(shuffle_doc_words_list) /
                          word_doc_freq[vocab[j]])
                weight.append(freq * idf)
                doc_word_set.add(word)

        node_size = train_size + vocab_size + test_size
        adj = sp.csr_matrix( (weight, (row, col)), shape=(node_size, node_size))
    
        ##########################################################
        
        adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj) # make it symmetric
        self.adj = adj
    
    ################################################################################
    
    def preprocess(self, ):
    
        print('prepare input data') if self.verbose == 1 else None
        self.prepare_input_data()
        print('clean input data') if self.verbose == 1 else None
        self.clean_input_data()
        print('show corpus statistics') if self.verbose == 1 else None
        self.show_corpus_statistics() if self.verbose == 1 else None
        print('shuffle input data') if self.verbose == 1 else None
        self.shuffle_input_data()
        print('build vocab') if self.verbose == 1 else None
        self.build_vocab()
        print('build labels') if self.verbose == 1 else None
        self.build_labels()
        print('set validation') if self.verbose == 1 else None
        self.set_validation()
        print('build embeddings') if self.verbose == 1 else None
        self.build_embeddings()
        print('build x') if self.verbose == 1 else None
        # x: feature vectors of training docs, no initial features
        self.build_x()
        print('build y') if self.verbose == 1 else None
        self.build_y()
        print('build tx') if self.verbose == 1 else None
        # tx: feature vectors of test docs, no initial features
        self.build_tx()
        print('build ty') if self.verbose == 1 else None
        self.build_ty()
        print('build allx') if self.verbose == 1 else None
        # allx: the the feature vectors of both labeled and unlabeled training instances # (a superset of x) # unlabeled training instances -> words
        self.build_allx()
        print('build ally') if self.verbose == 1 else None
        self.build_ally()
        
        print('build windows') if self.verbose == 1 else None
        self.build_windows()
        print('build word window freq') if self.verbose == 1 else None
        self.build_word_window_freq()
        print('build word pair count') if self.verbose == 1 else None
        self.build_word_pair_count()
        print('build pmi') if self.verbose == 1 else None
        self.build_pmi()
        print('build doc wod freq') if self.verbose == 1 else None
        self.build_doc_word_frequency()
        print('build adj') if self.verbose == 1 else None
        self.build_adj()
    
    ################################################################################
        
    @staticmethod
    def construct_feed_dict(features, support, labels, labels_mask, placeholders):
            """Construct feed dictionary."""
            feed_dict = dict()
            feed_dict.update({placeholders['labels']: labels})
            feed_dict.update({placeholders['labels_mask']: labels_mask})
            feed_dict.update({placeholders['features']: features})
            feed_dict.update({placeholders['support'][i]: support[i] for i in range(len(support))})
            feed_dict.update({placeholders['num_features_nonzero']: features[1].shape})
            return feed_dict
        
    ################################################################################
        
    def set_model_parameters(self,):

        
        args = type("xClass", (object,), {})
        args.dataset = 'text_gtn_' + self.model_date
        args.model = 'gtn' # 'gcn'
        args.learning_rate = 0.01
        args.epoch = 40
        args.node_dim = 64
        args.num_channels = 2
        args.lr = 0.005
        args.weight_decay = 0.001
        args.num_layers = 2
        args.norm = True
        args.adaptive_lr = False

        self.args = args

        #################################

    def create_model(self, ):


        node_features = self.node_features
        edges = self.adj
        labels = self.labels

        ################################
        epochs = self.args.epoch
        node_dim = self.args.node_dim
        num_channels = self.args.num_channels
        lr = self.args.lr
        weight_decay = self.args.weight_decay
        num_layers = self.args.num_layers
        norm = self.args.norm
        adaptive_lr = self.args.adaptive_lr
        #################################
        
        num_nodes = edges[0].shape[0]

        for i,edge in enumerate(edges):
            if i ==0:
                A = torch.from_numpy(edge.todense()).type(torch.FloatTensor).unsqueeze(-1)
            else:
                A = torch.cat([A,torch.from_numpy(edge.todense()).type(torch.FloatTensor).unsqueeze(-1)], dim=-1)
        A = torch.cat([A,torch.eye(num_nodes).type(torch.FloatTensor).unsqueeze(-1)], dim=-1)
        
        node_features = torch.from_numpy(node_features).type(torch.FloatTensor)
        train_node = torch.from_numpy(np.array(labels[0])[:,0]).type(torch.LongTensor)
        train_target = torch.from_numpy(np.array(labels[0])[:,1]).type(torch.LongTensor)
        valid_node = torch.from_numpy(np.array(labels[1])[:,0]).type(torch.LongTensor)
        valid_target = torch.from_numpy(np.array(labels[1])[:,1]).type(torch.LongTensor)
        test_node = torch.from_numpy(np.array(labels[2])[:,0]).type(torch.LongTensor)
        test_target = torch.from_numpy(np.array(labels[2])[:,1]).type(torch.LongTensor)
        
        num_classes = torch.max(train_target).item()+1

        #################################

        model = GTN(num_edge=A.shape[-1],
                            num_channels=num_channels,
                            w_in = node_features.shape[1],
                            w_out = node_dim,
                            num_class=num_classes,
                            num_layers=num_layers,
                            norm=norm)
        if adaptive_lr == 'false':
            optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=0.001)
        else:
            optimizer = torch.optim.Adam([{'params':model.weight},
                                        {'params':model.linear1.parameters()},
                                        {'params':model.linear2.parameters()},
                                        {"params":model.layers.parameters(), "lr":0.5}
                                        ], lr=0.005, weight_decay=0.001)
        loss = nn.CrossEntropyLoss()

    def _train(self,):
        
        model = self.model
        
        ##########################################################
        for i in range(epochs):
            for param_group in optimizer.param_groups:
                if param_group['lr'] > 0.005:
                    param_group['lr'] = param_group['lr'] * 0.9
            print('Epoch:  ',i+1)
            model.zero_grad()
            model.train()
            loss,y_train,Ws = model(A, node_features, train_node, train_target)
            train_f1 = torch.mean(f1_score(torch.argmax(y_train.detach(),dim=1), train_target, num_classes=num_classes)).cpu().numpy()
            print('Train - Loss: {}, Macro_F1: {}'.format(loss.detach().cpu().numpy(), train_f1))
            loss.backward()
            optimizer.step()
            model.eval()
            # Valid
            with torch.no_grad():
                val_loss, y_valid,_ = model.forward(A, node_features, valid_node, valid_target)
                val_f1 = torch.mean(f1_score(torch.argmax(y_valid,dim=1), valid_target, num_classes=num_classes)).cpu().numpy()
                print('Valid - Loss: {}, Macro_F1: {}'.format(val_loss.detach().cpu().numpy(), val_f1))
                test_loss, y_test,W = model.forward(A, node_features, test_node, test_target)
                test_f1 = torch.mean(f1_score(torch.argmax(y_test,dim=1), test_target, num_classes=num_classes)).cpu().numpy()
                print('Test - Loss: {}, Macro_F1: {}\n'.format(test_loss.detach().cpu().numpy(), test_f1))
        print("Optimization Finished!")
        
        ##########################################################
        pass        
    
    def _test(self,):
        
        model = self.model
        sess = self.sess
        evaluate = self._evaluate
        placeholders = self.placeholders
        FLAGS = self.FLAGS

        features = self.features
        support = self.support
        
        y_test = self.y_test
        test_mask = self.test_mask
        
        ##########################################################
        
        # Testing
        test_cost, test_acc, pred, labels, test_duration = evaluate(features, support, y_test, test_mask, placeholders)
        print("Test set results:", "cost=", "{:.5f}".format(test_cost),"accuracy=", "{:.5f}".format(test_acc), "time=", "{:.5f}".format(test_duration))

        test_pred = []
        test_labels = []
        print(len(test_mask))
        for i in range(len(test_mask)):
            if test_mask[i]:
                test_pred.append(pred[i])
                test_labels.append(labels[i])

        print("Test Precision, Recall and F1-Score...")
        print(metrics.classification_report(test_labels, test_pred, digits=4))
        print("Macro average Test Precision, Recall and F1-Score...")
        print(metrics.precision_recall_fscore_support(test_labels, test_pred, average='macro'))
        print("Micro average Test Precision, Recall and F1-Score...")
        print(metrics.precision_recall_fscore_support(test_labels, test_pred, average='micro'))

        ##########################################################
        
        self.test_pred = test_pred
        self.test_labels = test_labels
        self.test_acc = test_acc
    
    def write_embeddings(self,):
        
        outs = self.outs
        
        train_size = self.train_size
        test_size = self.test_size
        adj = self.adj
        
        vocab_size = self.vocab_size
        
        ##########################################################
        
        # doc and word embeddings
        word_embeddings = outs[3][train_size: adj.shape[0] - test_size]
        train_doc_embeddings = outs[3][:train_size]  # include val docs
        test_doc_embeddings = outs[3][adj.shape[0] - test_size:]

        words = self.vocab

        vocab_size = len(words)
        word_vectors = []
        for i in range(vocab_size):
            word = words[i].strip()
            word_vector = word_embeddings[i]
            word_vector_str = ' '.join([str(x) for x in word_vector])
            word_vectors.append(word + ' ' + word_vector_str)

        word_embeddings_str = '\n'.join(word_vectors)
        f = open(self.output_folder + 'text_gcn_word_vectors_'+ self.model_date +'.txt', 'w')
        f.write(word_embeddings_str)
        f.close()

        ##########################################################
        
        doc_vectors = []
        doc_id = 0
        for i in range(train_size):
            doc_vector = train_doc_embeddings[i]
            doc_vector_str = ' '.join([str(x) for x in doc_vector])
            doc_vectors.append('doc_' + str(doc_id) + ' ' + doc_vector_str)
            doc_id += 1

        for i in range(test_size):
            doc_vector = test_doc_embeddings[i]
            doc_vector_str = ' '.join([str(x) for x in doc_vector])
            doc_vectors.append('doc_' + str(doc_id) + ' ' + doc_vector_str)
            doc_id += 1

        doc_embeddings_str = '\n'.join(doc_vectors)
        f = open(self.output_folder + 'text_gcn__doc_vectors_'+ self.model_date +'.txt', 'w')
        f.write(doc_embeddings_str)
        f.close()
    
    ################################################################################
    
    def train(self, df, validation_ratio=0.0):
        
        self.sentences          = df['text'].values
        self.labels             = df['label'].values
        self.train_or_test_list = df['tot'].values
        
        self.validation_ratio = validation_ratio
        
        ############################################################################
        self.preprocess()
        ############################################################################
        
        self.set_model_parameters()
        self.create_model()
        
        self._train()
        # self._test()
        
        # self.write_embeddings()
        
# textgcn = TextGCN_TransductiveClassifier(verbose=0)
# textgcn.train(train)