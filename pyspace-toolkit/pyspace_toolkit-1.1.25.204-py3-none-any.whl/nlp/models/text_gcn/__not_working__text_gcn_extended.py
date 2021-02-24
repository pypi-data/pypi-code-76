# %%
# from layers import *
# from metrics import *

import numpy as np
import tensorflow as tf2
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()

# %%
# flags = tf.app.flags
# FLAGS = flags.FLAGS


# %%
def uniform(shape, scale=0.05, name=None):
    """Uniform init."""
    initial = tf2.random.uniform(shape, minval=-scale, maxval=scale, dtype=tf2.float32)
    return tf2.Variable(initial, name=name)


# %%
def glorot(shape, name=None):
    """Glorot & Bengio (AISTATS 2010) init."""
    init_range = np.sqrt(6.0/(shape[0]+shape[1]))
    initial = tf2.random.uniform(shape, minval=-init_range, maxval=init_range, dtype=tf2.float32)
    return tf2.Variable(initial, name=name)


# %%
def zeros(shape, name=None):
    """All zeros."""
    initial = tf2.zeros(shape, dtype=tf2.float32)
    return tf2.Variable(initial, name=name)


# %%
def ones(shape, name=None):
    """All ones."""
    initial = tf2.ones(shape, dtype=tf2.float32)
    return tf2.Variable(initial, name=name)

# %%
def masked_softmax_cross_entropy(preds, labels, mask):
    """Softmax cross-entropy loss with masking."""
    print(preds)
    loss = tf2.nn.softmax_cross_entropy_with_logits(logits=preds, labels=labels)
    mask = tf2.cast(mask, dtype=tf2.float32)
    mask /= tf2.reduce_mean(mask)
    loss *= mask
    return tf2.reduce_mean(loss)


# %%
def masked_accuracy(preds, labels, mask):
    """Accuracy with masking."""
    correct_prediction = tf2.equal(tf2.argmax(preds, 1), tf2.argmax(labels, 1))

    accuracy_all = tf2.cast(correct_prediction, tf2.float32)
    mask = tf2.cast(mask, dtype=tf2.float32)
    mask /= tf2.reduce_mean(mask)
    accuracy_all *= mask
    return tf2.reduce_mean(accuracy_all)

# %%
def softmax_cross_entropy(preds, labels):
    loss = tf2.nn.softmax_cross_entropy_with_logits(logits=preds, labels=labels)
    return tf2.reduce_mean(loss)

# %%
def accuracy(preds, labels):
    correct_prediction = tf2.equal(tf2.argmax(preds, 1), tf2.argmax(labels, 1))
    accuracy_all = tf2.cast(correct_prediction, tf2.float32)
    return tf2.reduce_mean(accuracy_all)

# %%
# global unique layer ID dictionary for layer name assignment
_LAYER_UIDS = {}


# %%
def get_layer_uid(layer_name=''):
    """Helper function, assigns unique layer IDs."""
    if layer_name not in _LAYER_UIDS:
        _LAYER_UIDS[layer_name] = 1
        return 1
    else:
        _LAYER_UIDS[layer_name] += 1
        return _LAYER_UIDS[layer_name]


# %%
def sparse_dropout(x, keep_prob, noise_shape):
    """Dropout for sparse tensors."""
    random_tensor = keep_prob
    random_tensor += tf.random_uniform(noise_shape)
    dropout_mask = tf.cast(tf.floor(random_tensor), dtype=tf.bool)
    pre_out = tf.sparse_retain(x, dropout_mask)
    return pre_out * (1./keep_prob)


# %%
def dot(x, y, sparse=False):
    """Wrapper for tf.matmul (sparse vs dense)."""
    if sparse:
        res = tf.sparse_tensor_dense_matmul(x, y)
    else:
        res = tf.matmul(x, y)
    return res


# %%
class Layer(object):
    """Base layer class. Defines basic API for all layer objects.
    Implementation inspired by keras (http://keras.io).

    # Properties
        name: String, defines the variable scope of the layer.
        logging: Boolean, switches Tensorflow histogram logging on/off

    # Methods
        _call(inputs): Defines computation graph of layer
            (i.e. takes input, returns output)
        __call__(inputs): Wrapper for _call()
        _log_vars(): Log all variables
    """

    def __init__(self, **kwargs):
        allowed_kwargs = {'name', 'logging'}
        for kwarg in kwargs.keys():
            assert kwarg in allowed_kwargs, 'Invalid keyword argument: ' + kwarg
        name = kwargs.get('name')
        if not name:
            layer = self.__class__.__name__.lower()
            name = layer + '_' + str(get_layer_uid(layer))
        self.name = name
        self.vars = {}
        logging = kwargs.get('logging', False)
        self.logging = logging
        self.sparse_inputs = False

    def _call(self, inputs):
        return inputs

    def __call__(self, inputs):
        with tf.name_scope(self.name):
            if self.logging and not self.sparse_inputs:
                tf.summary.histogram(self.name + '/inputs', inputs)
            outputs = self._call(inputs)
            if self.logging:
                tf.summary.histogram(self.name + '/outputs', outputs)
            return outputs

    def _log_vars(self):
        for var in self.vars:
            tf.summary.histogram(self.name + '/vars/' + var, self.vars[var])


# %%
class GraphConvolution(Layer):
    """Graph convolution layer."""
    def __init__(self, input_dim, output_dim, placeholders, dropout=0.,
                 sparse_inputs=False, act=tf.nn.relu, bias=False,
                 featureless=False, **kwargs):
        super(GraphConvolution, self).__init__(**kwargs)

        if dropout:
            self.dropout = placeholders['dropout']
        else:
            self.dropout = 0.

        self.act = act
        self.support = placeholders['support']
        self.sparse_inputs = sparse_inputs
        self.featureless = featureless
        self.bias = bias

        # helper variable for sparse dropout
        self.num_features_nonzero = placeholders['num_features_nonzero']

        with tf.variable_scope(self.name + '_vars'):
            for i in range(len(self.support)):
                self.vars['weights_' + str(i)] = glorot([input_dim, output_dim],
                                                        name='weights_' + str(i))
            if self.bias:
                self.vars['bias'] = zeros([output_dim], name='bias')

        if self.logging:
            self._log_vars()

    def _call(self, inputs):
        x = inputs

        # dropout
        if self.sparse_inputs:
            x = sparse_dropout(x, 1-self.dropout, self.num_features_nonzero)
        else:
            # x = tf.nn.dropout(x, 1-self.dropout)
            x = tf.nn.dropout(x, rate=self.dropout)

        # convolve
        supports = list()
        for i in range(len(self.support)):
            if not self.featureless:
                pre_sup = dot(x, self.vars['weights_' + str(i)],
                              sparse=self.sparse_inputs)
            else:
                pre_sup = self.vars['weights_' + str(i)]
            support = dot(self.support[i], pre_sup, sparse=True)
            supports.append(support)
        output = tf.add_n(supports)

        # bias
        if self.bias:
            output += self.vars['bias']
        self.embedding = output #output
        return self.act(output)
class GraphConvolutionExtended(Layer):
    """Graph convolution layer."""
    def __init__(self, input_dim, output_dim, placeholders, dropout=0.,
                 support=None, sparse_inputs=False, act=tf.nn.relu, bias=False,
                 featureless=False, **kwargs):
        super(GraphConvolutionExtended, self).__init__(**kwargs)

        if dropout:
            self.dropout = placeholders['dropout']
        else:
            self.dropout = 0.

        self.act = act
        if support is None:
            self.support = placeholders['support'][0]
        else:
            self.support = support
        self.sparse_inputs = sparse_inputs
        self.featureless = featureless
        self.bias = bias

        # helper variable for sparse dropout
        self.num_features_nonzero = placeholders['num_features_nonzero']

        with tf.variable_scope(self.name + '_vars'):
            for i in range(1):
                self.vars['weights_' + str(i)] = glorot([input_dim, output_dim],
                                                        name='weights_' + str(i))
            if self.bias:
                self.vars['bias'] = zeros([output_dim], name='bias')

        if self.logging:
            self._log_vars()

    def _call(self, inputs):
        x = inputs

        # dropout
        if self.sparse_inputs:
            x = sparse_dropout(x, 1-self.dropout, self.num_features_nonzero)
        else:
            # x = tf.nn.dropout(x, 1-self.dropout)
            x = tf.nn.dropout(x, rate=self.dropout)

        # convolve
        # supports = list()
        # for i in range(len(self.support)):
        #     if not self.featureless:
        #         pre_sup = dot(x, self.vars['weights_' + str(i)],
        #                       sparse=self.sparse_inputs)
        #     else:
        #         pre_sup = self.vars['weights_' + str(i)]
        #     support = dot(self.support[i], pre_sup, sparse=True)
        #     supports.append(support)
        # output = tf.add_n(supports)
        if not self.featureless:
            pre_sup = dot(x, self.vars['weights_0'],
                          sparse=self.sparse_inputs)
        else:
            pre_sup = self.vars['weights_0']
        output = dot(self.support, pre_sup, sparse=True)

        # bias
        if self.bias:
            output += self.vars['bias']

        self.embedding = output #output
        return self.act(output)


# %%
class Model(object):
    def __init__(self, **kwargs):
        allowed_kwargs = {'name', 'logging'}
        for kwarg in kwargs.keys():
            assert kwarg in allowed_kwargs, 'Invalid keyword argument: ' + kwarg
        name = kwargs.get('name')
        if not name:
            name = self.__class__.__name__.lower()
        self.name = name

        logging = kwargs.get('logging', False)
        self.logging = logging

        self.vars = {}
        self.placeholders = {}

        self.layers = []
        self.activations = []

        self.inputs = None
        self.outputs = None

        self.loss = 0
        self.accuracy = 0
        self.optimizer = None
        self.opt_op = None

    def _build(self):
        raise NotImplementedError

    def build(self):
        """ Wrapper for _build() """
        with tf.variable_scope(self.name):
            self._build()

        # Build sequential layer model
        self.activations.append(self.inputs)
        for layer in self.layers:
            hidden = layer(self.activations[-1])
            self.activations.append(hidden)
        self.outputs = self.activations[-1]

        # Store model variables for easy access
        variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=self.name)
        self.vars = {var.name: var for var in variables}

        # Build metrics
        self._loss()
        self._accuracy()

        self.opt_op = self.optimizer.minimize(self.loss)

    def predict(self):
        pass

    def _loss(self):
        raise NotImplementedError

    def _accuracy(self):
        raise NotImplementedError

    def save(self, sess=None):
        if not sess:
            raise AttributeError("TensorFlow session not provided.")
        saver = tf.train.Saver(self.vars)
        save_path = saver.save(sess, "tmp/%s.ckpt" % self.name)
        print("Model saved in file: %s" % save_path)

    def load(self, sess=None):
        if not sess:
            raise AttributeError("TensorFlow session not provided.")
        saver = tf.train.Saver(self.vars)
        save_path = "tmp/%s.ckpt" % self.name
        saver.restore(sess, save_path)
        print("Model restored from file: %s" % save_path)


# %%
class GCN(Model):
    def __init__(self, placeholders, input_dim, **kwargs):
        super(GCN, self).__init__(**kwargs)

        self.inputs = placeholders['features']
        self.input_dim = input_dim
        # self.input_dim = self.inputs.get_shape().as_list()[1]  # To be supported in future Tensorflow versions
        self.output_dim = placeholders['labels'].get_shape().as_list()[1]
        self.placeholders = placeholders
        
        self.FLAGS = placeholders['FLAGS']

        # self.optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.FLAGS.learning_rate)

        self.build()

    def _loss(self):
        # Weight decay loss
        for var in self.layers[0].vars.values():
            self.loss += self.FLAGS.weight_decay * tf.nn.l2_loss(var)

        # Cross entropy error
        self.loss += masked_softmax_cross_entropy(self.outputs, self.placeholders['labels'],
                                                  self.placeholders['labels_mask'])

    def _accuracy(self):
        self.accuracy = masked_accuracy(self.outputs, self.placeholders['labels'],
                                        self.placeholders['labels_mask'])
        self.pred = tf.argmax(self.outputs, 1)
        self.labels = tf.argmax(self.placeholders['labels'], 1)

    def _build(self):

        self.layers.append(GraphConvolution(input_dim=self.input_dim,
                                            output_dim=self.FLAGS.hidden1,
                                            placeholders=self.placeholders,
                                            act=tf.nn.relu,
                                            dropout=True,
                                            featureless=True,
                                            sparse_inputs=True,
                                            logging=self.logging))

        self.layers.append(GraphConvolution(input_dim=self.FLAGS.hidden1,
                                            output_dim=self.output_dim,
                                            placeholders=self.placeholders,
                                            act=lambda x: x, #
                                            dropout=True,
                                            logging=self.logging))

    def predict(self):
        return tf.nn.softmax(self.outputs)
class GCN_Extended(Model):
    def __init__(self, placeholders, input_dim, **kwargs):
        super(GCN_Extended, self).__init__(**kwargs)

        self.inputs = placeholders['features']
        self.input_dim = input_dim
        # self.input_dim = self.inputs.get_shape().as_list()[1]  # To be supported in future Tensorflow versions
        self.output_dim = placeholders['labels'].get_shape().as_list()[1]
        self.placeholders = placeholders
        self.supports = placeholders['support']
        
        self.FLAGS = placeholders['FLAGS']

        # self.optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.FLAGS.learning_rate)

        self.build()

    def _loss(self):
        # Weight decay loss
        for var in self.layers[0].vars.values():
            self.loss += self.FLAGS.weight_decay * tf.nn.l2_loss(var)

        # Cross entropy error
        # self.loss += masked_softmax_cross_entropy(self.outputs, self.placeholders['labels'], self.placeholders['labels_mask'])
        self.loss += softmax_cross_entropy(self.outputs, self.placeholders['labels'])

    def _accuracy(self):
        # self.accuracy = masked_accuracy(self.outputs, self.placeholders['labels'], self.placeholders['labels_mask'])
        self.accuracy = accuracy(self.outputs, self.placeholders['labels'])

        self.pred = tf.argmax(self.outputs, 1)
        self.labels = tf.argmax(self.placeholders['labels'], 1)

    def _build(self):

        self.layers.append(GraphConvolution(input_dim=self.input_dim,
                                            output_dim=self.FLAGS.hidden1,
                                            placeholders=self.placeholders,
                                            act=tf.nn.relu,
                                            dropout=True,
                                            featureless=True,
                                            # sparse_inputs=True,
                                            sparse_inputs=False,
                                            logging=self.logging))

        self.layers.append(GraphConvolution(input_dim=self.FLAGS.hidden1,
                                            output_dim=self.output_dim,
                                            placeholders=self.placeholders,
                                            act=lambda x: x, #
                                            dropout=True,
                                            logging=self.logging))

    def predict(self):
        return tf.nn.softmax(self.outputs)
class GCN_Extended_v2(Model):
    def __init__(self, placeholders, input_dim, **kwargs):
        super(GCN_Extended_v2, self).__init__(**kwargs)
        self.inputs = placeholders['features']
        self.input_dim = input_dim
        # self.input_dim = self.inputs.get_shape().as_list()[1]  # To be supported in future Tensorflow versions
        self.output_dim = placeholders['labels'].get_shape().as_list()[1]
        self.placeholders = placeholders
        self.supports = placeholders['support']

        self.FLAGS = placeholders['FLAGS']

        global_step = tf.Variable(0, trainable=False)
        # learning_rate = tf.compat.v1.train.exponential_decay(self.FLAGS.learning_rate,global_step,100000, 0.96, staircase=True)
        learning_rate = tf.train.exponential_decay(self.FLAGS.learning_rate,global_step, 10, 0.96, staircase=True)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        # self.optimizer = tf.train.AdamOptimizer(learning_rate=self.FLAGS.learning_rate)

        self.build()

    def _loss(self):
        # Weight decay loss
        for var in self.layers[0].vars.values():
            self.loss += self.FLAGS.weight_decay * tf.nn.l2_loss(var)

        # Cross entropy error
        self.loss += softmax_cross_entropy(self.outputs, self.placeholders['labels'])

    def _accuracy(self):
        self.accuracy = accuracy(self.outputs, self.placeholders['labels'])

    def _build(self):
        # appr_support = self.placeholders['support'][0]
        self.layers.append(GraphConvolutionExtended(input_dim=self.input_dim,
                                            output_dim=self.FLAGS.hidden1,
                                            placeholders=self.placeholders,
                                            support=self.supports[0],
                                            act=tf.nn.relu,
                                            dropout=True,
                                            sparse_inputs=False,
                                            logging=self.logging))

        self.layers.append(GraphConvolutionExtended(input_dim=self.FLAGS.hidden1,
                                            output_dim=self.output_dim,
                                            placeholders=self.placeholders,
                                            support=self.supports[0],
                                            act=lambda x: x,
                                            dropout=True,
                                            logging=self.logging))

    def predict(self):
        return tf.nn.softmax(self.outputs)



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


class TextGCN_TransductiveClassifier:
    
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
        # Set random seed
        seed = random.randint(1, 200)
        np.random.seed(seed)
        tf.set_random_seed(seed)
        # tf.random.set_seed(seed)
        # Settings
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

        flags = type("xClass", (object,), {})
        flags.dataset = 'text_gcn_' + self.model_date
        flags.model = 'gcn' # 'gcn'
        flags.learning_rate = 0.01
        flags.epochs = 200
        flags.hidden1 = 200
        flags.dropout = 0.2
        flags.weight_decay = 0
        flags.early_stopping = 300
        flags.max_degree = 3
        FLAGS = flags
        
        self.FLAGS = FLAGS
    
        ###########################################################
        ###########################################################
        ###########################################################
        
        x = self.x
        y = self.y
        tx = self.tx
        ty = self.ty
        allx = self.allx
        ally = self.ally
        
        train_size = self.train_size

        adj = self.adj
        
        ##########################################################
        def sparse_to_tuple(sparse_mx):
            """Convert sparse matrix to tuple representation."""
            def to_tuple(mx):
                if not sp.isspmatrix_coo(mx):
                    mx = mx.tocoo()
                coords = np.vstack((mx.row, mx.col)).transpose()
                values = mx.data
                shape = mx.shape
                return coords, values, shape

            if isinstance(sparse_mx, list):
                for i in range(len(sparse_mx)):
                    sparse_mx[i] = to_tuple(sparse_mx[i])
            else:
                sparse_mx = to_tuple(sparse_mx)

            return sparse_mx

        def preprocess_features(features):
            """Row-normalize feature matrix and convert to tuple representation"""
            rowsum = np.array(features.sum(1))
            r_inv = np.power(rowsum, -1).flatten()
            r_inv[np.isinf(r_inv)] = 0.
            r_mat_inv = sp.diags(r_inv)
            features = r_mat_inv.dot(features)
            return sparse_to_tuple(features)

        def nontuple_preprocess_features(features):
            """Row-normalize feature matrix and convert to tuple representation"""
            rowsum = np.array(features.sum(1))
            r_inv = np.power(rowsum, -1).flatten()
            r_inv[np.isinf(r_inv)] = 0.
            r_mat_inv = sp.diags(r_inv)
            features = r_mat_inv.dot(features)
            return features


        features = sp.vstack((allx, tx)).tolil()
        features = sp.identity(features.shape[0])
        
        labels = np.vstack((ally, ty))

        train_size = train_size
        val_size = train_size - x.shape[0]
        test_size = tx.shape[0]

        idx_train = range(len(y))
        idx_val = range(len(y), len(y) + val_size)
        idx_test = range(allx.shape[0], allx.shape[0] + test_size)
        idx_vocab = range(train_size, allx.shape[0])

        def sample_mask(idx, l):
            """Create mask."""
            mask = np.zeros(l)
            mask[idx] = 1
            return np.array(mask, dtype=np.bool)

        train_mask = sample_mask(idx_train, labels.shape[0])
        val_mask = sample_mask(idx_val, labels.shape[0])
        test_mask = sample_mask(idx_test, labels.shape[0])
        vocab_mask = sample_mask(idx_vocab, labels.shape[0])

        y_train = np.zeros(labels.shape)
        y_val = np.zeros(labels.shape)
        y_test = np.zeros(labels.shape)
        y_vocab = np.zeros(labels.shape)

        y_train[train_mask, :] = labels[train_mask, :]
        y_val[val_mask, :] = labels[val_mask, :]
        y_test[test_mask, :] = labels[test_mask, :]
        y_vocab[vocab_mask, :] = labels[vocab_mask, :]
        
        ##########################################################
        def normalize_adj(adj):
            """Symmetrically normalize adjacency matrix."""
            adj = sp.coo_matrix(adj)
            rowsum = np.array(adj.sum(1))
            d_inv_sqrt = np.power(rowsum, -0.5).flatten()
            d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.
            d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
            return adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt).tocoo()

        def preprocess_adj(adj):
            """Preprocessing of adjacency matrix for simple GCN model and conversion to tuple representation."""
            adj_normalized = normalize_adj(adj + sp.eye(adj.shape[0]))
            return sparse_to_tuple(adj_normalized)
        def nontuple_preprocess_adj(adj):
            if adj.shape[0] == adj.shape[1]:
                adj_normalized = normalize_adj(sp.eye(adj.shape[0]) + adj)
            else:
                rowsum = np.array(adj.sum(1))
                rowdegree_inv = np.power(rowsum, -0.5).flatten()
                rowdegree_inv[np.isinf(rowdegree_inv)] = 0.
                rowdegree_mat_inv = sp.diags(rowdegree_inv)

                colsum = np.array(adj.sum(0))
                coldegree_inv = np.power(colsum, -0.5).flatten()
                coldegree_inv[np.isinf(coldegree_inv)] = 0.
                coldegree_mat_inv = sp.diags(coldegree_inv)

                adj_normalized = rowdegree_mat_inv.dot(adj).dot(coldegree_mat_inv).tocoo()        
            # adj_normalized = sp.eye(adj.shape[0]) + normalize_adj(adj)
            return adj_normalized.tocsr()

        
        ##########################################################
        

        train_index = np.where(train_mask)[0]
        vocab_index = np.where(vocab_mask)[0]
        tmp_index = list(train_index) + list(vocab_index)
        val_index = np.where(val_mask)[0]
        test_index = np.where(test_mask)[0]

        adj_train       = adj[train_index, :][:, tmp_index]
        adj_train_vocab = adj[tmp_index, :][:, tmp_index]
        # adj_train = adj[tmp_index, :][:, tmp_index]
        normADJ_train = nontuple_preprocess_adj(adj_train)
        normADJ_train_vocab = nontuple_preprocess_adj(adj_train_vocab)
        normADJ = nontuple_preprocess_adj(adj)

        # idx_train = range(allx.shape[0])
        # train_mask = sample_mask(idx_train, labels.shape[0])
        # y_train = np.zeros(labels.shape)
        # y_train[train_mask, :] = labels[train_mask, :]
        # y_train = y_train[tmp_index,:]
        
        train_mask = train_mask[train_index]
        y_train = y_train[train_index]

        val_mask = val_mask[val_index]
        y_val = y_val[val_index]

        test_mask = test_mask[test_index]
        y_test = y_test[test_index]

        # nontuple_train_features = nontuple_features[tmp_index,:][:,tmp_index]
        # nontuple_features = nontuple_preprocess_features(features)
        # features = preprocess_features(features)
        features = nontuple_preprocess_features(features).todense()
        train_features = features[tmp_index]
        # train_features = features[tmp_index,:][:,tmp_index]

        self.adj_train = adj_train

        self.normADJ_train = normADJ_train
        self.normADJ_train_vocab = normADJ_train_vocab
        self.normADJ = normADJ
        # self.nontuple_train_features = nontuple_train_features
        ##########################################################


        self.train_index = train_index
        self.vocab_index = vocab_index
        self.tmp_index = tmp_index
        self.val_index = val_index
        self.test_index  = test_index 
        
        # self.support = [preprocess_adj(adj)]
        self.features = features
        self.train_features = train_features

        self.y_train = y_train
        self.y_val = y_val
        self.y_test = y_test
        
        self.train_mask = train_mask
        self.val_mask = val_mask
        self.test_mask = test_mask
        
        self.train_size = train_size
        self.val_size = val_size
        self.test_size = test_size
        
    def create_model(self, ):
        
        features = self.features
        train_features = self.train_features
        # nontuple_train_features = self.nontuple_train_features
        y_train = self.y_train
        FLAGS = self.FLAGS
        num_supports = 1
        # model_func = GCN
        model_func = GCN_Extended_v2

        def sparse_to_tuple(sparse_mx):
            """Convert sparse matrix to tuple representation."""
            def to_tuple(mx):
                if not sp.isspmatrix_coo(mx):
                    mx = mx.tocoo()
                coords = np.vstack((mx.row, mx.col)).transpose()
                values = mx.data
                shape = mx.shape
                return coords, values, shape

            if isinstance(sparse_mx, list):
                for i in range(len(sparse_mx)):
                    sparse_mx[i] = to_tuple(sparse_mx[i])
            else:
                sparse_mx = to_tuple(sparse_mx)

            return sparse_mx

        ##########################################################
        
        print(train_features.shape)
        # Define placeholders
        placeholders = {
            'support': [tf.sparse_placeholder(tf.float32) for _ in range(num_supports)],
            # 'features': tf.placeholder(tf.float32, shape=(None, train_features.shape[1])),
            'features': tf.placeholder(tf.float32, shape=(None, features.shape[1])),
            # 'features': tf.sparse_placeholder(tf.float32, shape=tf.constant(features[2], dtype=tf.int64)),
            # 'features': tf.sparse_placeholder(tf.float32, shape=tf.constant(sparse_to_tuple(nontuple_train_features)[2], dtype=tf.int64)),
            # 'features': tf.placeholder(tf.float32, shape=(None, features.shape[1])),
            # 'features': tf.sparse_placeholder(tf.float32, shape=tf.constant(train_features.shape[0], dtype=tf.int64)),
            # 'features': tf.placeholder(tf.float32, shape=(None, features.shape[1])),
            # 'features': tf.sparse_placeholder(tf.float32, shape=(None, features.shape[1])),
            # 'features': tf.sparse_placeholder(tf.float32, shape=tf.constant(features.shape[1], dtype=tf.int64)),
            'labels': tf.placeholder(tf.float32, shape=(None, y_train.shape[1])),
            'labels_mask': tf.placeholder(tf.int32),
            'dropout': tf.placeholder_with_default(0., shape=()),
            # helper variable for sparse dropout
            'num_features_nonzero': tf.placeholder(tf.int32),
            'FLAGS': FLAGS,
        }

        # Create model
        # model = model_func(placeholders, input_dim=features[2][1], logging=True)
        model = model_func(placeholders, input_dim=features.shape[-1], logging=True)
        # model = model_func(placeholders, input_dim=train_features.shape[-1], logging=True)
        
        session_conf = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
        sess = tf.Session(config=session_conf)
        sess.run(tf.global_variables_initializer())
        
        ##########################################################
        
        self.sess = sess
        self.model = model
        self.placeholders = placeholders
   
    # Define model evaluation function
    def _evaluate(self, features, support, labels, mask, placeholders):
        
        sess = self.sess
        model = self.model
        
        ##########################################################
        
        construct_feed_dict = self.construct_feed_dict
        
        ##########################################################
        
        t_test = time.time()
        feed_dict_val = construct_feed_dict(features, support, labels, mask, placeholders)
        outs_val = sess.run([model.loss, model.accuracy, model.pred, model.labels], feed_dict=feed_dict_val)
        return outs_val[0], outs_val[1], outs_val[2], outs_val[3], (time.time() - t_test)
    
    def _train(self,):
        
        model = self.model
        sess = self.sess
        evaluate = self._evaluate
        placeholders = self.placeholders
        FLAGS = self.FLAGS

        features = self.features
        # support = self.support
        
        y_train = self.y_train
        train_mask = self.train_mask

        y_val = self.y_val
        val_mask = self.val_mask
        

        val_index = self.val_index
        test_index = self.test_index 

        test_mask = self.test_mask 
        y_test = self.y_test 


        
        ##########################################################
        adj_train = self.adj_train
        #nontuple_train_features = self.nontuple_train_features        
        normADJ_train = self.normADJ_train
        normADJ_train_vocab = self.normADJ_train_vocab
        normADJ = self.normADJ
        
        train_features = self.train_features
        ##########################################################
        
        construct_feed_dict = self.construct_feed_dict
        def iterate_minibatches_listinputs(inputs, batchsize, shuffle=False):
            assert inputs is not None
            numSamples = inputs[0].shape[0]
            if shuffle:
                indices = np.arange(numSamples)
                np.random.shuffle(indices)
            for start_idx in range(0, numSamples - batchsize + 1, batchsize):
                if shuffle:
                    excerpt = indices[start_idx:start_idx + batchsize]
                else:
                    excerpt = slice(start_idx, start_idx + batchsize)
                yield [input[excerpt] for input in inputs]
        def sparse_to_tuple(sparse_mx):
            """Convert sparse matrix to tuple representation."""
            def to_tuple(mx):
                if not sp.isspmatrix_coo(mx):
                    mx = mx.tocoo()
                coords = np.vstack((mx.row, mx.col)).transpose()
                values = mx.data
                shape = mx.shape
                return coords, values, shape

            if isinstance(sparse_mx, list):
                for i in range(len(sparse_mx)):
                    sparse_mx[i] = to_tuple(sparse_mx[i])
            else:
                sparse_mx = to_tuple(sparse_mx)

            return sparse_mx


        ##########################################################
        valSupport = [sparse_to_tuple(normADJ[val_index, :])]
        testSupport = [sparse_to_tuple(normADJ[test_index, :])]

        cost_val = []

        # Train model
        for epoch in range(FLAGS.epochs):

            t = time.time()

            batches = iterate_minibatches_listinputs([normADJ_train, y_train, train_mask], batchsize=256, shuffle=True)

            for batch in batches:
                [normADJ_batch, y_train_batch, train_mask_batch] = batch
                support_batch = [sparse_to_tuple(normADJ_batch)]
                features_batch = train_features # sparse_to_tuple(nontuple_train_features)

                # Construct feed dictionary
                feed_dict = construct_feed_dict(features_batch, support_batch, y_train_batch, train_mask_batch, placeholders)
                feed_dict.update({placeholders['dropout']: FLAGS.dropout})

                # Training step
                outs = sess.run([model.opt_op, model.loss, model.accuracy, model.layers[0].embedding], feed_dict=feed_dict)

            # Validation
            cost, acc, pred, labels, duration = evaluate(features, support, y_val, val_mask, placeholders)
            cost_val.append(cost)

            print("Epoch:", '%04d' % (epoch + 1), "train_loss=", "{:.5f}".format(outs[1]),
                  "train_acc=", "{:.5f}".format(outs[2]), "val_loss=", "{:.5f}".format(cost),
                  "val_acc=", "{:.5f}".format(acc), "time=", "{:.5f}".format(time.time() - t))

            # # Construct feed dictionary
            # feed_dict = construct_feed_dict(features, support, y_train, train_mask, placeholders)
            # feed_dict.update({placeholders['dropout']: FLAGS.dropout})
            # 
            # # Training step
            # outs = sess.run([model.opt_op, model.loss, model.accuracy,model.layers[0].embedding], feed_dict=feed_dict)
            # 
            # # Validation
            # cost, acc, pred, labels, duration = evaluate(features, support, y_val, val_mask, placeholders)
            # cost_val.append(cost)
            # 
            # print("Epoch:", '%04d' % (epoch + 1), "train_loss=", "{:.5f}".format(outs[1]),
            #       "train_acc=", "{:.5f}".format(outs[2]), "val_loss=", "{:.5f}".format(cost),
            #       "val_acc=", "{:.5f}".format(acc), "time=", "{:.5f}".format(time.time() - t))
            # 
            # if epoch > FLAGS.early_stopping and cost_val[-1] > np.mean(cost_val[-(FLAGS.early_stopping+1):-1]):
            #     print("Early stopping...")
            #     break

        print("Optimization Finished!")
        
        ##########################################################
        
        self.outs = outs
    
    def _test(self,):
        
        model = self.model
        sess = self.sess
        evaluate = self._evaluate
        placeholders = self.placeholders
        FLAGS = self.FLAGS

        features = self.features
        # support = self.support
        
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
        self._test()
        
        self.write_embeddings()
        
# textgcn = TextGCN_TransductiveClassifier(verbose=0)
# textgcn.train(train)