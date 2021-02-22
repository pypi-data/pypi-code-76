#!/usr/bin/env python

import keras 
from keras import backend as K

class Loss:
    def __init__(self, loss = None, customization = None):
        self.loss = keras.losses.CategoricalCrossentropy()
        if 'dice_iou' in loss:
            self.loss = self.dice_iou_loss
        elif 'dice' in loss:
            self.loss = self.dice_loss
        elif 'iou' in loss:
            self.loss = self.iou_loss
        elif customization != None:
            self.loss = customization
        
    def iou_coef(self, y_true_f, y_pred_f, smooth = 1):
        intersection = K.sum(y_true_f * y_pred_f)
        return (intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth - intersection)

    def dice_coef(self, y_true_f, y_pred_f, smooth = 1):
        intersection = K.sum(y_true_f * y_pred_f)
        return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

    def dice_loss(self, y_true, y_pred):
        ret_loss = 0.0
        for index in range(y_true.shape[-1]):
            y_true_f = K.flatten(y_true[:,:,:,:,index])
            y_pred_f = K.flatten(y_pred[:,:,:,:,index])
            ret_loss += self.dice_coef(y_true_f, y_pred_f)
        return 1 - (ret_loss / y_true.shape[-1])
    
    def iou_loss(self, y_true, y_pred):
        ret_loss = 0.0
        for index in range(y_true.shape[-1]):
            y_true_f = K.flatten(y_true[:,:,:,:,index])
            y_pred_f = K.flatten(y_pred[:,:,:,:,index])
            ret_loss += self.iou_coef(y_true_f, y_pred_f)
        return 1 - (ret_loss / y_true.shape[-1])

    def dice_iou_loss(self, y_true, y_pred):
        ret_loss = 0.0
        for index in range(y_true.shape[-1]):
            y_true_f = K.flatten(y_true[:,:,:,:,index])
            y_pred_f = K.flatten(y_pred[:,:,:,:,index])
            ret_loss += self.dice_coef(y_true_f, y_pred_f) * self.iou_coef(y_true_f, y_pred_f)
        return 1 - (ret_loss / y_true.shape[-1])

