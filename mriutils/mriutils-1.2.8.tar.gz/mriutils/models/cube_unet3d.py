#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 01:12:02 2020

@author: kuangmeng
"""

from tensorflow.keras.layers import Concatenate, LeakyReLU, Conv3D, LSTM, Reshape, UpSampling3D, Input, BatchNormalization, MaxPooling3D, Multiply
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os
import tensorflow as tf
from modules.losses import Loss
from modules.metrics import Metric
strategy = tf.distribute.MirroredStrategy()
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class CUBE_UNet3D:
    def __init__(self, input_shape, model_level = 2, n_classes = 2, loss = None, metric = None, pretrained_weights = None):
        self.input_shape = input_shape
        self.layers = input_shape[0]
        self.size = input_shape[1] * input_shape[2]
        self.width = input_shape[1]
        self.height = input_shape[2]
        self.channels = input_shape[3]
        self.n_classes = n_classes
        self.model_level = model_level
        self.pretrained_weights = pretrained_weights
        with strategy.scope():
            self.model = self.structure()
            self.model.compile(optimizer = Adam(lr = 1e-5), 
                           loss = Loss(loss).loss, 
                           metrics = [Metric(metric).metric])
    
    def LSTMLayer(self, input_tensor):
        if int(self.model_level) != 2:
            return input_tensor
        old_shape = input_tensor.shape
        new_shape = (old_shape[1], old_shape[2] * old_shape[3] * old_shape[4])
        ret_shape = (old_shape[1], old_shape[2], old_shape[3], 1)
        tmp = Reshape(new_shape)(input_tensor)
        whole_seq_output, final_memory_state, final_carry_state = LSTM(old_shape[2] * old_shape[3], return_sequences=True, return_state=True)(tmp)
        return Reshape(ret_shape)(whole_seq_output)

    def Atten(self, input_tensor):
        if int(self.model_level) == 0:
            return input_tensor
        cnn_layer = Conv3D(filters = input_tensor.shape[-1], kernel_size= (1, 3, 3), padding='same')
        query_encoding = cnn_layer(input_tensor)
        key_encoding = cnn_layer(input_tensor)
        query_value_attention = cnn_layer(Multiply()([query_encoding, key_encoding]))
        attention_score = tf.keras.activations.softmax(query_value_attention, axis = -1)
        return Multiply()([key_encoding, attention_score])

    def structure(self):
        inputs = Input(self.input_shape)
        conv1 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 32)(inputs)
        conv1 = BatchNormalization()(conv1)
        conv1 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 64)(conv1)
        conv1 = BatchNormalization()(conv1)
        meg1 = LeakyReLU()(conv1)
        conv1 = MaxPooling3D(pool_size=(1, 2, 2))(meg1)
        conv2 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 64)(conv1)
        conv2 = BatchNormalization()(conv2)
        conv2 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 128)(conv2)
        conv2 = BatchNormalization()(conv2)
        meg2 = LeakyReLU()(conv2)
        conv2 = MaxPooling3D(pool_size=(1, 2, 2))(meg2)
        conv3 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 128)(conv2)
        conv3 = BatchNormalization()(conv3)
        conv3 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 256)(conv3)
        conv3 = BatchNormalization()(conv3)
        meg3 = LeakyReLU()(conv3)
        conv3 = MaxPooling3D(pool_size=(1, 2, 2))(meg3)
        conv4 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 256)(conv3)
        conv4 = BatchNormalization()(conv4)
        conv4 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 512)(conv4)
        conv4 = BatchNormalization()(conv4)
        meg4 = LeakyReLU()(conv4)
        meg4 = self.LSTMLayer(meg4)
        conv4 = MaxPooling3D(pool_size=(1, 2, 2))(meg4)
        flat = Conv3D(kernel_size = (1, 1, 1), padding = 'same', filters = 512)(conv4)
        up1 = UpSampling3D(size = (1, 2, 2))(flat)
        meg4 = self.Atten(meg4)
        up1 = Concatenate(axis = -1)([meg4,up1])
        up1 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 256)(up1)
        up1 = BatchNormalization()(up1)
        up1 = self.LSTMLayer(up1)
        up1 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 256)(up1)
        up1 = BatchNormalization()(up1)
        up1 = LeakyReLU()(up1)
        up2 = UpSampling3D(size = (1, 2, 2))(up1)
        meg3 = self.Atten(meg3)
        up2 = Concatenate(axis = -1)([meg3,up2])
        up2 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 128)(up2)
        up2 = BatchNormalization()(up2)
        up2 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 128)(up2)
        up2 = BatchNormalization()(up2)
        up2 = LeakyReLU()(up2)
        up3 = UpSampling3D(size = (1, 2, 2))(up2)
        meg2 = self.Atten(meg2)
        up3 = Concatenate(axis = -1)([meg2, up3])
        up3 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 64)(up3)
        up3 = BatchNormalization()(up3)
        up3 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 64)(up3)
        up3 = BatchNormalization()(up3)
        up3 = LeakyReLU()(up3)
        up4 = UpSampling3D(size = (1, 2, 2))(up3)
        meg1 = self.Atten(meg1)
        up4 = Concatenate(axis = -1)([meg1, up4])
        up4 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 32)(up4)
        up4 = BatchNormalization()(up4)
        up4 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 32)(up4)
        up4 = BatchNormalization()(up4)
        up4 = LeakyReLU()(up4)
        up5 = Conv3D(kernel_size = (1, 1, 1), padding = 'same', filters = self.n_classes)(up4)
        outputs = tf.keras.layers.Softmax(axis=-1)(up5)
        model = Model(inputs, outputs)
        model.summary()
        if(self.pretrained_weights):
        	    model.load_weights(self.pretrained_weights)
        return model
