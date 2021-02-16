
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import time
import math
#-------------------------------
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, BatchNormalization, Conv1D, MaxPooling1D, Flatten, Dropout
from keras.optimizers import SGD, Adam


# In[2]:


def train(x_train, y_train, x_test, y_test, hpar):
    input_shape = x_train.shape[1:]
    output_num = y_train.shape[1]
    if hpar['layer_activ_function_at_output'] == 'sigmoid': # loss function
        loss_func = 'binary_crossentropy'
    elif hpar['layer_activ_function_at_output'] == 'softmax':
        loss_func = 'categorical_crossentropy'
    if hpar['optimizer'] == 'gradient descent': # optimizer
        optimizer = SGD(lr=hpar['learning_rate'])
    elif hpar['optimizer'] == 'adam':
        optimizer = Adam(lr=hpar['learning_rate'])
    #-----------------------------------------------------
    model = Sequential()
    model.add(Dropout(hpar['layer_dropout_rate_at_input'], input_shape=input_shape))
    model.add(BatchNormalization())
    for i in range(0, len(hpar['layer_conv_filter'])):
        conv_ksize = hpar['layer_conv_filter'][i][0]
        conv_filters = hpar['layer_conv_filter'][i][1]
        conv_stride = hpar['layer_conv_stride'][i]
        conv_pad = hpar['layer_conv_padding'][i]
        pool_ksize = hpar['layer_pool_filter'][i]
        pool_stride = hpar['layer_pool_stride'][i]
        pool_pad = hpar['layer_pool_padding'][i]
        model.add(Conv1D(conv_filters, conv_ksize, strides=conv_stride, padding=conv_pad))
        model.add(Dropout(hpar['layer_dropout_rate_at_conv'][i]))
        model.add(BatchNormalization())
        model.add(Activation(hpar['layer_activ_function_at_conv'])) # 'sigmoid', 'tanh', 'relu'
        model.add(MaxPooling1D(pool_size=pool_ksize, strides=pool_stride, padding=pool_pad))
    model.add(Flatten())
    for i in range(len(hpar['layer_fc'])):
        model.add(Dense(hpar['layer_fc'][i]))
        model.add(Dropout(hpar['layer_dropout_rate_at_fc'][i]))
        model.add(BatchNormalization())
        model.add(Activation(hpar['layer_activ_function_at_fc'])) # 'sigmoid', 'tanh', 'relu'
    model.add(Dense(output_num))
    model.add(BatchNormalization())
    model.add(Activation(hpar['layer_activ_function_at_output']))
    model.compile(optimizer = optimizer, loss = loss_func, metrics = ['accuracy'])
    #-----------------------------------------------------
    model.summary()
    loss = []
    accu = []
    for i in range(1, 1 + max(1, hpar['num_epochs'] // hpar['print_cost'])):
        tic = time.time()
        fout = model.fit(x_train, y_train, epochs=hpar['print_cost'], batch_size=hpar['minibatch_size'], verbose=0)
        toc = time.time()
        loss = loss + fout.history['loss'] # training set
        accu = accu + fout.history['acc'] # training set
        score_train = model.evaluate(x_train, y_train, batch_size=hpar['minibatch_size'], verbose=0)
        score_test = model.evaluate(x_test, y_test, batch_size=hpar['minibatch_size'], verbose=0)
        print('>> epochs = ', (i*hpar['print_cost']),'; Train loss/acc = %f/%f'%(score_train[0],score_train[1]), '; Test loss/acc = %f/%f'%(score_test[0],score_test[1]), '; time = %f sec '%(toc-tic))
    mout = {'model': model,
            'loss': loss,
            'accu': accu}
    return mout


# In[3]:


if False:
    hpar = {}
    hpar['layer_dropout_rate_at_input'] = 0.0
    hpar['layer_conv_filter'] = [[7,8], [3,16]] # [height, width, channel]
    hpar['layer_conv_stride'] = [1, 1] # [height, width]
    hpar['layer_conv_padding'] = ['SAME', 'SAME']
    hpar['layer_dropout_rate_at_conv'] = [0.0, 0.0]
    hpar['layer_activ_function_at_conv'] = ['sigmoid', 'tanh', 'relu'][1]
    hpar['layer_pool_filter'] = [4, 4] # [height, width]
    hpar['layer_pool_stride'] = [4, 4] # [height, width]
    hpar['layer_pool_padding'] = ['VALID', 'VALID']
    hpar['layer_fc'] = []
    hpar['layer_dropout_rate_at_fc'] = [0.0] # ex) [0.0, 0.0, 0.0]
    hpar['layer_activ_function_at_fc'] = ['sigmoid', 'tanh', 'relu'][1]
    hpar['layer_activ_function_at_output'] = ['sigmoid', 'softmax'][1]
    hpar['learning_rate'] = 0.4
    hpar['num_epochs'] = 3000
    hpar['minibatch_size'] = 999999
    hpar['optimizer'] = ["gradient descent", "momentum", "adam"][0]
    hpar['print_cost'] = 100 # print epoch step; no print when it is zero
    mout = train(x_train, y_train_one_hot, x_test, y_test_one_hot, hpar)
    #-------------------------------------------------------------
    plt.plot(mout['loss'])
    plt.show()
    plt.plot(mout['accu'])
    plt.show()
    #-------------------------------------------------------------
    yp_test_one_hot = mout['model'].predict(x_test)
    yp_test = np.argmax(yp_test_one_hot, axis = 1).reshape(y_test.shape)
    accuracy_test = np.mean(y_test == yp_test)
    print(accuracy_test)  


# In[4]:


'''
What's new from cnn1d_ks20180119?
(1) drop-out layer added
(2) some parameter names changed
'''

