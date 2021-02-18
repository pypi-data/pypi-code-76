import innvestigate as inn
from keras import Sequential
import keras as ks
import numpy as np


class analyser:
    def __init__(self):
        self.epsilon = 0.01

    def split_model(self, model):
        # run check to see if model contains an embedding layer, innvestigate does not support embedding layers.
        layers = [l for l in model.layers]  # get all layer names in model
        for i, layer in enumerate(layers):
            if 'embeddings' in layer.__str__():  # check where a layer is of type embeddings
                if i == len(layers):
                    print(
                        "you have an embedding layer as your final output layer, are you sure that it is correct? \n alpacka does not currently support this configuration")
                    break
                # split original model into pre and post embedding layer
                emb_pre = model.layers[:i + 1]
                lrp_post = model.layers[i + 1:]
        # rebuild the split model pre the embedding layer
        emb_model = Sequential()  # create new model for the post embedding
        for lay in emb_pre:
            emb_model.add(lay)
        emb_model.compile(optimizer=model.optimizer,
                          loss=model.loss)  # optimizer and loss are needed to compile the model, but no backward pass on the model will be performed

        # rebuild the split model post the embedding layer
        lrp_model = Sequential()  # create new model for the post embedding
        for lay in lrp_post:
            lrp_model.add(lay)
        lrp_model.compile(optimizer=model.optimizer,
                          loss=model.loss)  # optimizer and loss are needed to compile the model, but no backward pass on the model will be performed

        # the models for some reason needs to make one prediction before they are "fully compiled and can be used by innvestigate"
        tmp_sent = np.zeros(emb_model._build_input_shape[1])  # make a dummy sentence
        tmp_sent = np.expand_dims(tmp_sent, 0)
        pre = emb_model.predict(tmp_sent)
        _ = lrp_model.predict(pre)

        return emb_model, lrp_model

    def create_analyser(self, lrp_model):
        analyzer = inn.create_analyzer('lrp.epsilon', lrp_model, epsilon=self.epsilon, neuron_selection_mode='all')
        return analyzer

    def fit_analyser(self, analyser, data):
        analyser.fit(data)
        return analyser


class lrp_pipe:
    def __init__(self):
        self.Dot = 10
        self.Verbose = True
        self.maxlen = None  #
        self.num_words = None
        self.epsilon = 0.01

    def tokenize_data(self, data_text):
        "create a tokenizer that transforms words from letters to text"

        t = ks.preprocessing.text.Tokenizer(num_words=self.num_words)
        t.fit_on_texts(data_text)

        "Tranform the letter sentences to integer representations"
        data_int = t.texts_to_sequences(data.preprocessed_text.astype(str))
        data_int = ks.preprocessing.sequence.pad_sequences(data_int, self.maxlen, padding='post')
        "cols = len +1 due to index 0 is reserved and unused in the tokenizer "
        if t.num_words is None:
            cols = len(t.index_word) + 1
        else:
            cols = self.maxlen + 1

        index_words = t.index_word
        words = [elm for elm in index_words.values()]
        dictionary = {i: words[i] for i in range(0, cols - 1)}

        return data_int, dictionary

    def load_model(self, path_model):
        model = ks.models.load_model(path_model)
        self.maxlen = model.input_shape[1]
        return model

    def calculate_lrp(self, model, tokenized_data):
        pass


def main(data, model_path):
    labels = data[data.columns[0]].astype(int)
    texts = data[data.columns[1]].astype(str)
    lrp = lrp_pipe()
    ann = analyser()
    model = lrp.load_model(model_path)
    emb_mod, lrp_mod = ann.split_model(model)
    lyser = ann.create_analyser(lrp_mod)
    data_int, dictionary = lrp.tokenize_data(texts)

    # lrp_result = lrp.calculate_lrp(model,data_int[:10])
    return [data_int, dictionary, model, emb_mod, lrp_mod, lyser]


if __name__ == '__main__':
    import pandas as pd

    data = pd.read_csv('fear_data_nov10.csv', usecols=['label', 'preprocessed_text'],
                       dtype={'label': 'int', 'preprocessed_text': 'str'})
    data.dropna()
    model_path = 'Baseline_0'
    ret = main(data, model_path)

    ann = ret[-1]
    text = ret[0]
    sent = text[0]
    sent = np.expand_dims(sent, 0)
    emb_mod = ret[-3]

    tmp = emb_mod.predict(sent)
    lrp = ann.analyze(tmp)
