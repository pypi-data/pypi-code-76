# %%
import logging
import os
import typing
import warnings
from typing import Any, Dict, List, Optional, Text, Tuple, Type

import numpy as np
from scipy.sparse import csr_matrix

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

import rasa.utils.io as io_utils
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.classifiers import LABEL_RANKING_LENGTH
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.components import Component
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.constants import DENSE_FEATURE_NAMES, SPARSE_FEATURE_NAMES, TEXT
from rasa.nlu.featurizers.featurizer import sequence_to_sentence_features
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
import rasa.utils.common as common_utils

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    import sklearn

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pyspace_resources
import fasttext

import pickle
from sklearn.model_selection import train_test_split

from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Embedding, Bidirectional, Dropout, LSTM, Dense, TimeDistributed
from tensorflow.keras.optimizers import Adam

class KerasBiLSTM(IntentClassifier):
    # varying batch size
    # stratified batch
    # batch normalization layer
    # tqdm callback

    defaults = {
        "batch_size": 64,
        "epochs": 12,
        "learning_rate": 0.001,
        "validation_size": 0.1,
        "lstm_kernel_regularization": 0.002,
        "lstm_hidden_dim": 300,

    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        clf = None,
        le = None,
        # TODO 1 # max_len: = None,
        word_index = None,
    ) -> None:

        super().__init__(component_config)

        self.kerasindexer = KerasTokenizer()
        self.max_len = 32

        if le is not None and clf is not None and word_index is not None:
            self.le = le
            self.clf = clf
            # TODO 1 # self.max_len = max_len
            self.kerasindexer = KerasTokenizer()
            self.kerasindexer.word_index = word_index
            print(word_index)

        # self.le.inverse_transform(y)
        # tokenizer.word_index

    def generate_data(self, intent_examples, train_predict='predict'):

        texts = [[t.text for t in message.get(TOKENS_NAMES[TEXT])] for message in intent_examples]

        if train_predict == 'train':
            labels = [e.get("intent") for e in intent_examples]
            self.le = LabelEncoder()
            y = self.le.fit_transform(labels)
            y = tf.keras.utils.to_categorical(np.asarray(y))

            # TODO 1 # self.max_len = max([len(x) for x in texts])
            self.kerasindexer = KerasTokenizer()
            self.kerasindexer.fit_on_texts(texts)

        elif train_predict == 'predict':
            y = None
        
        
        sequences = self.kerasindexer.texts_to_sequences(texts)
        data = pad_sequences(sequences, maxlen=self.max_len, padding='post', truncating='post')
        X = data

        return X, y

    @staticmethod
    def read_embedding_matrix(word_index, ):

        EMBEDDING_DIM = 300
        pyres_path = pyspace_resources.__file__.rsplit('/',1)[0]
        ft_path = f'{pyres_path}/fasttext/tr/cc.tr.300.bin'
        ft = fasttext.load_model(ft_path)

        embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
        for word, i in word_index.items():
            embedding_matrix[i] = ft.get_word_vector(word)

        return embedding_matrix

    @staticmethod
    def create_model(embedding_matrix, max_len, out_len, learning_rate=0.001, lstm_hidden_dim=300, lstm_kernel_regularization=0.002):

        model = Sequential()
        model.add(Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1], weights=[embedding_matrix], 
                            input_length=max_len, trainable=True))
        # model.add(Bidirectional(LSTM(200, return_sequences=True)))
        # model.add(Bidirectional(LSTM(200, return_sequences=False)))
        model.add(Bidirectional(LSTM(lstm_hidden_dim, return_sequences=False, kernel_regularizer=tf.keras.regularizers.l2(lstm_kernel_regularization))))
        model.add(Dropout(0.5))
        model.add(Dense(out_len, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=learning_rate), metrics=['accuracy'])
        
        return model

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        X, y = self.generate_data(training_data.intent_examples, train_predict='train')
        embedding_matrix = self.read_embedding_matrix(self.kerasindexer.word_index)
        self.clf = self.create_model(embedding_matrix, self.max_len, len(self.le.classes_), 
                                        self.component_config["learning_rate"], self.component_config["lstm_hidden_dim"], self.component_config["lstm_kernel_regularization"],
                                    )

        validation_size=self.component_config["validation_size"]
        if validation_size:
            X_train, X_val, y_train, y_val = train_test_split(X, y, stratify=y, test_size=validation_size, random_state=42)
            
            callback = EarlyStopping(monitor='val_acc', min_delta=0, patience=6, verbose=1, mode='min', restore_best_weights=True)
            reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.6, patience=2, min_lr=0.00001)

            keras_history = self.clf.fit(x=X_train, y=y_train, epochs=self.component_config["epochs"], batch_size=self.component_config["batch_size"], 
                                    shuffle=True, verbose=2, validation_data=[X_val,y_val],
                                    callbacks=[callback, reduce_lr],
                                )
            #print(val_acc = keras_history.history["val_acc"][-1])
            print(keras_history.history["val_accuracy"][-1])
        else:
            keras_history = self.clf.fit(x=X, y=y, epochs=self.component_config["epochs"], batch_size=self.component_config["batch_size"],  
                                    shuffle=True, verbose=2, 
                                )
        # val_acc = keras_history.history["val_acc"][-1]
        pass

    def process(self, message: Message, **kwargs: Any) -> None:
        """Return the most likely intent and its probability for a message."""

        X, _ = self.generate_data([message], train_predict='predict')
                
        intent_ids, probabilities = self.predict(X)
        intents = self.le.inverse_transform(np.ravel(intent_ids))

        probabilities = probabilities.flatten()

        if intents.size > 0 and probabilities.size > 0:
            ranking = list(zip(list(intents), list(probabilities)))[
                :LABEL_RANKING_LENGTH
            ]

            intent = {"name": intents[0], "confidence": float(probabilities[0])}

            intent_ranking = [
                {"name": intent_name, "confidence": float(score)}
                for intent_name, score in ranking
            ]
        else:
            intent = {"name": None, "confidence": 0.0}
            intent_ranking = []

        import json
        intent = json.loads(json.dumps(intent))
        intent_ranking = json.loads(json.dumps(intent_ranking))
        message.set("intent", intent, add_to_output=True)
        message.set("intent_ranking", intent_ranking, add_to_output=True)

    def predict_prob(self, X: np.ndarray) -> np.ndarray:

        probabilities = self.clf.predict(X)
        # print(self.le.inverse_transform([np.argmax(probabilities[0])]))
        ##########################################
        # probability normalization
        
        # if self.prob_norm:
        if False:
            probabilities = probabilities[0]

            sorted_indices = np.argsort(probabilities)[::-1]
            top_indices = sorted_indices[:self.prob_norm_select_N_items]
            other_indices = sorted_indices[self.prob_norm_select_N_items:]

            multiplier = min(1 / np.sum(probabilities[top_indices]), self.prob_norm_limit_X_times)

            probabilities[top_indices] = probabilities[top_indices] * multiplier
            remaining_ratio = 1 - np.sum(probabilities[top_indices])

            remaining_multiplier = remaining_ratio / np.sum(probabilities[other_indices])
            probabilities[other_indices] = probabilities[other_indices] * remaining_multiplier

            probabilities = probabilities.reshape(1, -1)
        ##########################################

        return probabilities

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Given a bow vector of an input text, predict most probable label.
        Return only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of
        # the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this model into the passed directory."""

        classifier_file_name = file_name + "_classifier.pkl"
        self.clf.save( os.path.join(model_dir, classifier_file_name) ) 

        preprocessing_file_name = file_name + "_preprocessing.pkl"
        preprocessing_variables = [self.le.classes_, self.kerasindexer.word_index]
        
        with open(os.path.join(model_dir, preprocessing_file_name), 'wb') as f:
            pickle.dump(preprocessing_variables, f)

        return {"classifier": classifier_file_name, "preprocessing": preprocessing_file_name}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["KerasBiLSTM"] = None,
        **kwargs: Any,
    ) -> "KerasBiLSTM":
    
        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        preprocessing_file = os.path.join(model_dir, meta.get("preprocessing"))

        clf = tf.keras.models.load_model(classifier_file)
        with open(preprocessing_file, 'rb') as f:
            preprocessing_variables = pickle.load(f)
        classes, word_index = preprocessing_variables

        le = LabelEncoder()
        le.classes_ = classes

        return cls(meta, clf, le, word_index)
