#!/usr/bin/env python
# coding: utf-8

# https://towardsdatascience.com/a-guide-to-an-efficient-way-to-build-neural-network-architectures-part-i-hyper-parameter-8129009f131b
# 
# https://towardsdatascience.com/a-guide-to-an-efficient-way-to-build-neural-network-architectures-part-ii-hyper-parameter-42efca01e5d7

# In[ ]:


import re
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Activation, Dropout
from tensorflow.keras.layers import Conv1D, Conv2D, Conv3D, MaxPooling1D, MaxPooling2D, MaxPooling3D, Flatten
from tensorflow.keras.optimizers import SGD, Adam, RMSprop, Adadelta, Adagrad
from tensorflow.keras.regularizers import l1, l2, l1_l2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model

def create_nn_model(X_train, Y_train, X_valid, Y_valid, param, verbose=False):
    model = Sequential(param['layers'])
    model.summary()
    model.compile(optimizer=eval(param['optimizer']+"(lr=param['learning_rate'])"), # e.g. Adam(lr=param['learning_rate'])
                  loss=param['loss'], 
                  metrics=param['metrics'])
    model.fit(X_train, Y_train, 
              validation_data=(X_valid, Y_valid),
              epochs=param['epochs'], 
              batch_size=param['batch_size'],
              class_weight=param['class_weight'], 
              callbacks=param['callbacks'],
              verbose=verbose)
    return model


# In[ ]:


# #--- datasets ----------------------------------------------------------
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.datasets import make_moons, make_circles, make_classification # https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html#sphx-glr-auto-examples-classification-plot-classifier-comparison-py
# from sklearn.metrics import accuracy_score
# from keras.utils import to_categorical

# def generate_2D_dataset(dataset='two-ellipse', n_samples=1000, random_state=123):
#     np.random.seed(random_state)
#     X = np.random.rand(n_samples,2)
#     if dataset=='line': Y = np.int32((X[:,1] - X[:,0] + 0.3) > 0)
#     elif dataset=='semi-circle': Y = np.int32((X[:,0]**2 + X[:,1]**2 - 0.7**2) > 0)
#     elif dataset=='circle': Y = np.int32(((X[:,0]-0.5)**2 + (X[:,1]-0.5)**2 - 0.3**2) > 0)
#     elif dataset=='ellipse': Y = np.int32((((X[:,0]-0.5)/0.4)**2 + ((X[:,1]-0.2)/0.05)**2 - 1) > 0)
#     elif dataset=='two-ellipse': Y = np.int32(((((X[:,0]-0.5)/0.4)**2 + ((X[:,1]-0.2)/0.05)**2 - 1) > 0) & (((X[:,0]-0.7)**2 + (X[:,1]-0.7)**2 - 0.1**2) > 0))
#     return X, Y

# X, Y = make_moons(n_samples=2000, noise=0.2, random_state=123)
# # X, Y = make_circles(n_samples=2000, noise=0.2, factor=0.5, random_state=123)
# # X, Y = generate_2D_dataset(dataset='line', n_samples=2000, random_state=123)
# # X, Y = generate_2D_dataset(dataset='semi-circle', n_samples=2000, random_state=123)
# # X, Y = generate_2D_dataset(dataset='circle', n_samples=2000, random_state=123)
# # X, Y = generate_2D_dataset(dataset='ellipse', n_samples=2000, random_state=123)
# # X, Y = generate_2D_dataset(dataset='two-ellipse', n_samples=2000, random_state=123)

# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=123); print('X_train.shape =', X_train.shape); print('Y_train.shape =', Y_train.shape); print('X_test.shape =', X_test.shape); print('Y_test.shape =', Y_test.shape)
# Y_train_oh = to_categorical(Y_train, num_classes=2); print('Y_train_oh.shape =', Y_train_oh.shape)
# Y_test_oh = to_categorical(Y_test, num_classes=2); print('Y_test_oh.shape =', Y_test_oh.shape)

# #--- parameters ----------------------------------------------------------
# param = {}

# param['layers'] = [
#     Dense(20, input_shape=X_train.shape[1:]), BatchNormalization(), Activation('relu'), Dropout(0.0), # Activation: 'sigmoid', 'tanh', 'relu', 'softmax'
#     Dense(10), BatchNormalization(), Activation('relu'), Dropout(0.0),
#     Dense(5), BatchNormalization(), Activation('relu'), Dropout(0.0),
#     Dense(Y_train_oh.shape[1]), Activation('softmax')
# ]

# param['optimizer'] = ['SGD', 'Adam', 'RMSprop','Adadelta','Adagrad'][2]
# param['learning_rate'] = 0.01
# param['loss'] = ['binary_crossentropy', 'categorical_crossentropy'][1]
# param['metrics']=['accuracy']

# param['epochs'] = 10000
# param['batch_size'] = 999999
# # param['batch_size'] = 64
# param['class_weight'] = None

# # param['callbacks'] = None
# filename_best_model = 'best_model.h5'
# es = EarlyStopping(monitor='val_loss', mode='min', patience=1000, verbose=0) # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
# mc = ModelCheckpoint(filename_best_model, monitor='val_accuracy', mode='max', save_best_only=True, verbose=0) # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
# param['callbacks'] = [es,mc] # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/

# #--- train model ----------------------------------------------------------
# %time model = create_nn_model(X_train, Y_train_oh, X_test, Y_test_oh, param)
# print(model.history.history['val_accuracy'][-1])
# print(accuracy_score(Y_test, np.argmax(model.predict(X_test), axis=1)))

# best_model = load_model(filename_best_model)
# print(max(model.history.history['val_accuracy']))
# print(accuracy_score(Y_test, np.argmax(best_model.predict(X_test), axis=1)))

# #--- plot ----------------------------------------------------------
# plt.plot(model.history.history['loss'], label='loss: train')
# plt.plot(model.history.history['val_loss'], label='loss: validation')
# plt.legend(); plt.show()

# plt.plot(model.history.history['accuracy'], label='accuracy: train')
# plt.plot(model.history.history['val_accuracy'], label='accuracy: validation')
# plt.legend(); plt.show()

# #--- plot decision boundary ----------------------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# def plot_2d_decision_bourndary(model, X_train, Y_train, X_test, Y_test, resolution=300):
#     # X, Y, Z for contour plot
#     x = np.linspace(X_train[:,0].min(),  X_train[:,0].max(), num=resolution)
#     y = np.linspace(X_train[:,1].min(),  X_train[:,1].max(), num=resolution)
#     X, Y = np.meshgrid(x, y)
#     Z_oh = model.predict(np.column_stack((X.ravel(),Y.ravel()))) # assumes that the model gives an one-hot output
#     Z = np.reshape(np.argmax(Z_oh, axis=-1), X.shape)

#     # plot
#     fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(12, 6))
#     sns.scatterplot(x=X_train[:,0], y=X_train[:,1], hue=Y_train[:], ax=ax[0]) # train dataset
#     ax[0].contour(X, Y, Z, colors = 'black') # contour plot
#     ax[0].legend(loc='upper right')
#     sns.scatterplot(x=X_test[:,0], y=X_test[:,1], hue=Y_test[:], ax=ax[1]) # test dataset
#     ax[1].contour(X, Y, Z, colors = 'black') # contour plot
#     ax[1].legend(loc='upper right')
#     plt.show()
    
# plot_2d_decision_bourndary(model, X_train, Y_train, X_test, Y_test)
# plot_2d_decision_bourndary(best_model, X_train, Y_train, X_test, Y_test)


# In[ ]:


# #-- image dataset ---------------------------------------------
# import tensorflow as tf
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from keras.utils import to_categorical
    
# def data():
#     (X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.fashion_mnist.load_data() # https://www.tensorflow.org/tutorials/keras/classification
#     class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat','Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        
#     X_train, X_valid, Y_train, Y_valid = train_test_split(X_train, Y_train, test_size=0.2, random_state=12345)

#     X_train = X_train.reshape(tuple(list(X_train.shape)+[1])) / 255.0
#     X_valid = X_valid.reshape(tuple(list(X_valid.shape)+[1])) / 255.0
#     X_test = X_test.reshape(tuple(list(X_test.shape)+[1])) / 255.0
    
#     Y_train_oh = to_categorical(Y_train, num_classes=len(class_names))
#     Y_valid_oh = to_categorical(Y_valid, num_classes=len(class_names))
#     Y_test_oh = to_categorical(Y_test, num_classes=len(class_names))

#     return class_names, X_train, Y_train, Y_train_oh, X_valid, Y_valid, Y_valid_oh, X_test, Y_test, Y_test_oh

# class_names, X_train, Y_train, Y_train_oh, X_valid, Y_valid, Y_valid_oh, X_test, Y_test, Y_test_oh = data()

# #--- plot train samples --------------------------------------
# plt.figure(figsize=(10,10))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(X_train[i].squeeze(), cmap=plt.cm.binary)
#     plt.xlabel(class_names[Y_train[i]])
# plt.show()

# #--- train model ----------------------------------------------------------
# param = {}

# # param['layers'] = [
# #     Flatten(input_shape=(28, 28)),
# #     Dense(128, activation='relu'),
# #     Dense(Y_train_oh.shape[1], activation='softmax')
# # ]

# param['layers'] = [
#     Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=X_train.shape[1:]),
#     Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same'),
#     MaxPooling2D(pool_size=(2, 2), strides=2),
#     Dropout(0.2),
#     Conv2D(64, kernel_size=(3, 3), activation='relu'),
#     Conv2D(64, kernel_size=(3, 3), activation='relu'),
#     BatchNormalization(),
#     MaxPooling2D(pool_size=(2, 2), strides=2),
#     Dropout(0.3),
#     Flatten(),
#     Dense(256, activation='relu'),
#     BatchNormalization(),
#     Dropout(0.7),
#     Dense(Y_train_oh.shape[1], activation='softmax')
# ]

# # param['optimizer'] = ['SGD', 'Adam', 'RMSprop','Adadelta','Adagrad'][2]
# param['optimizer'] = ['SGD', 'Adam', 'RMSprop','Adadelta','Adagrad'][1]
# param['learning_rate'] = 0.01
# param['loss'] = ['binary_crossentropy', 'categorical_crossentropy'][1]
# # param['loss'] = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
# param['metrics']=['accuracy']

# # param['epochs'] = 10
# param['epochs'] = 50
# # param['batch_size'] = 999999
# param['batch_size'] = 254
# param['class_weight'] = None

# # param['callbacks'] = None
# filename_best_model = 'best_model.h5'
# es = EarlyStopping(monitor='val_loss', mode='min', patience=1000, verbose=0) # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
# mc = ModelCheckpoint(filename_best_model, monitor='val_accuracy', mode='max', save_best_only=True, verbose=0) # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
# param['callbacks'] = [es,mc] # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/

# #--- train model ----------------------------------------------------------
# %time model = create_nn_model(X_train, Y_train_oh, X_valid, Y_valid_oh, param, verbose=True)
# # %time model = create_nn_model(X_train, Y_train, X_valid, Y_valid, param, verbose=True)
# print('Validation accuracy (last):', model.history.history['val_accuracy'][-1])
# print('Validation accuracy (last):', accuracy_score(Y_valid, np.argmax(model.predict(X_valid), axis=1)))

# best_model = load_model(filename_best_model)
# print('Validation accuracy (best):', max(model.history.history['val_accuracy']))
# print('Validation accuracy (best):', accuracy_score(Y_valid, np.argmax(best_model.predict(X_valid), axis=1)))

# test_loss, test_acc = model.evaluate(X_test,  Y_test_oh, verbose=2)
# # test_loss, test_acc = model.evaluate(X_test,  Y_test, verbose=2)
# print('Test accuracy:', test_acc)

# #--- plot ----------------------------------------------------------
# plt.plot(model.history.history['loss'], label='loss: train')
# plt.plot(model.history.history['val_loss'], label='loss: validation')
# plt.legend(); plt.show()

# plt.plot(model.history.history['accuracy'], label='accuracy: train')
# plt.plot(model.history.history['val_accuracy'], label='accuracy: validation')
# plt.legend(); plt.show()

# #--- plot test samples ----------------------------------------------------------
# def plot_image(i, predictions_array, true_label, img):
#     predictions_array, true_label, img = predictions_array, true_label[i], img[i]
#     plt.grid(False)
#     plt.xticks([])
#     plt.yticks([])

#     plt.imshow(img, cmap=plt.cm.binary)

#     predicted_label = np.argmax(predictions_array)
#     if predicted_label == true_label:
#         color = 'blue'
#     else:
#         color = 'red'

#     plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
#                                 100*np.max(predictions_array),
#                                 class_names[true_label]),
#                                 color=color)

# def plot_value_array(i, predictions_array, true_label):
#     predictions_array, true_label = predictions_array, true_label[i]
#     plt.grid(False)
#     plt.xticks(range(10))
#     plt.yticks([])
#     thisplot = plt.bar(range(10), predictions_array, color="#777777")
#     plt.ylim([0, 1])
#     predicted_label = np.argmax(predictions_array)

#     thisplot[predicted_label].set_color('red')
#     thisplot[true_label].set_color('blue')

# Y_pred_oh = best_model.predict(X_valid)

# num_rows = 5
# num_cols = 3
# num_images = num_rows*num_cols
# plt.figure(figsize=(2*2*num_cols, 2*num_rows))
# for i in range(num_images):
#     plt.subplot(num_rows, 2*num_cols, 2*i+1)
#     plot_image(i, Y_pred_oh[i], Y_valid, X_valid.squeeze())
#     plt.subplot(num_rows, 2*num_cols, 2*i+2)
#     plot_value_array(i, Y_pred_oh[i], Y_valid)
# plt.tight_layout()
# plt.show()


# In[ ]:




