
# coding: utf-8

# In[1]:


import numpy as np
import time
import pandas as pd
np.random.seed(0)
from keras.models import Model
from keras.layers import Dense, Input, Dropout, LSTM, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.initializers import glorot_uniform
np.random.seed(1)


# In[2]:


def pretrained_embedding_layer(word_to_vec_map, word_to_index):
    """
    Creates a Keras Embedding() layer and loads in pre-trained GloVe 50-dimensional vectors.
    
    Arguments:
    word_to_vec_map -- dictionary mapping words to their GloVe vector representation.
    word_to_index -- dictionary mapping from words to their indices in the vocabulary (400,001 words)

    Returns:
    embedding_layer -- pretrained layer Keras instance
    """
    vocab_len = len(word_to_index) + 1                  # adding 1 to fit Keras embedding (requirement)
    emb_dim = word_to_vec_map["cucumber"].shape[0]      # define dimensionality of your GloVe word vectors (= 50)
    emb_matrix = np.zeros((vocab_len, emb_dim)) # Initialize the embedding matrix as a numpy array of zeros of shape (vocab_len, dimensions of word vectors = emb_dim)
    for word, index in word_to_index.items(): # Set each row "index" of the embedding matrix to be the word vector representation of the "index"th word of the vocabulary
        emb_matrix[index, :] = word_to_vec_map[word]
    embedding_layer = Embedding(vocab_len, emb_dim, trainable = False) # Define Keras embedding layer with the correct output/input sizes, make it trainable. Use Embedding(...). Make sure to set trainable=False. 
    embedding_layer.build((None,)) # Build the embedding layer, it is required before setting the weights of the embedding layer. Do not modify the "None".
    embedding_layer.set_weights([emb_matrix]) # Set the weights of the embedding layer to the embedding matrix. Your layer is now pretrained.
    return embedding_layer


# In[3]:


def sentences_to_indices(X, word_to_index, max_len):
    """
    Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
    The output shape should be such that it can be given to `Embedding()` (described in Figure 4). 
    
    Arguments:
    X -- array of sentences (strings), of shape (m, 1)
    word_to_index -- a dictionary containing the each word mapped to its index
    max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this. 
    
    Returns:
    X_indices -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
    """
    m = X.shape[0]                                   # number of training examples
    X_indices = np.zeros((m, max_len)) # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
    for i in range(m):                               # loop over training examples
        sentence_words = X[i].lower().split() # Convert the ith training sentence in lower case and split is into words. You should get a list of words.
        j = 0 # Initialize j to 0
        for w in sentence_words: # Loop over the words of sentence_words
            X_indices[i, j] = word_to_index[w] # Set the (i,j)th entry of X_indices to the index of the correct word.
            j = j + 1 # Increment j to j + 1
    return X_indices
def train(word_to_vec_map, word_to_index, X_train_indices, Y_train_oh, X_test_indices, Y_test_oh, hpar):
    """
    Arguments:
    input_shape -- shape of the input, usually (max_len,)
    word_to_vec_map -- dictionary mapping every word in a vocabulary into its 50-dimensional vector representation
    word_to_index -- dictionary mapping from words to their indices in the vocabulary (400,001 words)

    Returns:
    model -- a model instance in Keras
    """
    input_shape = X_train_indices.shape[1:] # exclude the nubmer of samples
    output_num = Y_train_oh.shape[-1]
    embedding_layer = pretrained_embedding_layer(word_to_vec_map, word_to_index) # Create the embedding layer pretrained with GloVe Vectors (≈1 line)
    #-----------------------------------------
    sentence_indices = Input(shape=input_shape, dtype='int32') # Define sentence_indices as the input of the graph, it should be of shape input_shape and dtype 'int32' (as it contains indices).
    X = embedding_layer(sentence_indices) # Propagate sentence_indices through your embedding layer, you get back the embeddings
    for i in range(0, len(hpar['layer_lstm_hidden_state_dim_at_middle'])):
        X = LSTM(hpar['layer_lstm_hidden_state_dim_at_middle'][i], return_sequences=True)(X) # Propagate the embeddings through an LSTM layer with 128-dimensional hidden state # Be careful, the returned output should be a batch of sequences.
        X = Dropout(hpar['layer_dropout_rate_at_middle'][i])(X) # Add dropout with a probability of 0.5
    X = LSTM(hpar['layer_lstm_hidden_state_dim_at_output'])(X)# Propagate X trough another LSTM layer with 128-dimensional hidden state # Be careful, the returned output should be a single hidden state, not a batch of sequences.
    X = Dropout(hpar['layer_dropout_rate_at_output'])(X) # Add dropout with a probability of 0.5
#    X = Dense(5, activation='softmax')(X) # Propagate X through a Dense layer with softmax activation to get back a batch of 5-dimensional vectors.
    X = Dense(output_num)(X) # Propagate X through a Dense layer with softmax activation to get back a batch of 5-dimensional vectors.
    X = Activation('softmax')(X) # Add a softmax activation
    model = Model(inputs = sentence_indices, outputs = X) # Create Model instance which converts sentence_indices into X.
    #-----------------------------------------
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    log_df = pd.DataFrame(np.nan, index=range(hpar['num_epochs']), columns = ['loss', 'acc', 'loss_train', 'acc_train', 'loss_test', 'acc_test'])
    for i in range(1, 1 + max(1, hpar['num_epochs'] // hpar['print_cost'])):
        tic = time.time()
        fout = model.fit(X_train_indices, Y_train_oh, epochs=hpar['print_cost'], batch_size=hpar['minibatch_size'], shuffle=True, verbose=0)
        toc = time.time()
        log_df['loss'].loc[range((i-1)*hpar['print_cost'],i*hpar['print_cost'])] = fout.history['loss']
        log_df['acc'].loc[range((i-1)*hpar['print_cost'],i*hpar['print_cost'])] = fout.history['acc']
        loss_train, acc_train = model.evaluate(X_train_indices, Y_train_oh, verbose=0) # score = [loss, acc]
        loss_test, acc_test = model.evaluate(X_test_indices, Y_test_oh, verbose=0) # score = [loss, acc]
        log_df['loss_train'].loc[i*hpar['print_cost'] - 1] = loss_train
        log_df['acc_train'].loc[i*hpar['print_cost'] - 1] = acc_train
        log_df['loss_test'].loc[i*hpar['print_cost'] - 1] = loss_test
        log_df['acc_test'].loc[i*hpar['print_cost'] - 1] = acc_test
        print('>> epochs = ', (i*hpar['print_cost']),'; Train loss/acc = %f/%f'%(loss_train, acc_train), '; Test loss/acc = %f/%f'%(loss_test, acc_test), '; time = %f sec '%(toc-tic))
    mout = {'model': model,
            'log': log_df}
    return mout


# In[4]:


if False:
    import csv
    import emoji
    import matplotlib.pyplot as plt

    def read_glove_vecs(glove_file):
    #    with open(glove_file, 'r') as f:
        with open(glove_file, 'r', encoding="utf8") as f: # Bomsoo modified : https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
            words = set()
            word_to_vec_map = {}
            for line in f:
                line = line.strip().split()
                curr_word = line[0]
                words.add(curr_word)
                word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)
        
            i = 1
            words_to_index = {}
            index_to_words = {}
            for w in sorted(words):
                words_to_index[w] = i
                index_to_words[i] = w
                i = i + 1
        return words_to_index, index_to_words, word_to_vec_map
    def read_csv(filename = 'data/emojify_data.csv'):
        phrase = []
        emoji = []
        with open (filename) as csvDataFile:
            csvReader = csv.reader(csvDataFile)

            for row in csvReader:
                phrase.append(row[0])
                emoji.append(row[1])
        X = np.asarray(phrase)
        Y = np.asarray(emoji, dtype=int)

        return X, Y
    emoji_dictionary = {"0": "\u2764\uFE0F",    # :heart: prints a black instead of red heart depending on the font
                        "1": ":baseball:",
                        "2": ":smile:",
                        "3": ":disappointed:",
                        "4": ":fork_and_knife:"}
    def label_to_emoji(label):
        """
        Converts a label (int or string) into the corresponding emoji code (string) ready to be printed
        """
        return emoji.emojize(emoji_dictionary[str(label)], use_aliases=True)

    # loading datasets
    word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('../datasets/coursera_dnn5_week2_Emojify/data/glove.6B.50d.txt')
    X_train, Y_train = read_csv('../datasets/coursera_dnn5_week2_Emojify/data/train_emoji.csv')
    X_test, Y_test = read_csv('../datasets/coursera_dnn5_week2_Emojify/data/tesss.csv')

    # converting datasets
    maxLen = len(max(X_train, key=len).split())
    X_train_indices = sentences_to_indices(X_train, word_to_index, maxLen)
    Y_train_oh = np.eye(5)[Y_train] # convert_to_one_hot
    X_test_indices = sentences_to_indices(X_test, word_to_index, max_len = maxLen)
    Y_test_oh = np.eye(5)[Y_test] # convert_to_one_hot 

    # training
    hpar = {}
    hpar['layer_lstm_hidden_state_dim_at_middle'] = [128, 128, 128] # list
    hpar['layer_dropout_rate_at_middle'] = [0.5, 0.5, 0.5] # list
    hpar['layer_lstm_hidden_state_dim_at_output'] = 128
    hpar['layer_dropout_rate_at_output'] = 0.5
    hpar['num_epochs'] = 100
    hpar['print_cost'] = 10
    hpar['minibatch_size'] = 32
    mout = train(word_to_vec_map, word_to_index, X_train_indices, Y_train_oh, X_test_indices, Y_test_oh, hpar)
    mout['log'].plot().legend(bbox_to_anchor=(1, 1)) # plot(marker='o')
    plt.show()
    
    # This code allows you to see the mislabelled examples
    pred = mout['model'].predict(X_test_indices)
    for i in range(len(X_test)):
        x = X_test_indices
        num = np.argmax(pred[i])
        if(num != Y_test[i]):
            print('Expected emoji:'+ label_to_emoji(Y_test[i]) + ' prediction: '+ X_test[i] + label_to_emoji(num).strip())    
            
    # Change the sentence below to see your prediction. Make sure all the words are in the Glove embeddings.  
    x_test = np.array(['not feeling happy'])
    x_test_indices = sentences_to_indices(x_test, word_to_index, maxLen)
    print(x_test[0] +' '+  label_to_emoji(np.argmax(mout['model'].predict(x_test_indices))))    

