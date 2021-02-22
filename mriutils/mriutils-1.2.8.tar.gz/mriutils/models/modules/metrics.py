#!/usr/bin/env python

from keras import metrics
from keras import backend as K

class Metric:
    def __init__(self, metric = None, customization = None):
        self.metric = metrics.categorical_accuracy
        if 'dice' in metric:
            self.metric = self.dice_score
        elif 'iou' in metric:
            self.metric = self.iou
        elif 'sensitivity' in metric:
            self.metric = self.sensitivity
        elif 'ppv' in metric:
            self.metric = self.ppv
        elif customization != None:
            self.metric = customization

    def dice_coef(self, y_true_f, y_pred_f, smooth = 1):
        intersection = K.sum(y_true_f * y_pred_f)
        return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

    def iou_coef(self, y_true_f, y_pred_f, smooth = 1):
        intersection = K.sum(y_true_f * y_pred_f)
        return (intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth - intersection)

    def dice_score(self, y_true, y_pred):
        ret_loss = 0.0
        for index in range(1, y_true.shape[-1]):
            y_true_f = K.flatten(y_true[:,:,:,:,index])
            y_pred_f = K.flatten(y_pred[:,:,:,:,index])
            ret_loss += self.dice_coef(y_true_f, y_pred_f)
        return ret_loss / (y_true.shape[-1] - 1)

    def iou(self, y_true, y_pred):
        ret_loss = 0.0
        for index in range(1, y_true.shape[-1]):
            y_true_f = K.flatten(y_true[:,:,:,:,index])
            y_pred_f = K.flatten(y_pred[:,:,:,:,index])
            ret_loss += self.iou_coef(y_true_f, y_pred_f)
        return ret_loss / (y_true.shape[-1] - 1)

    def S(self, y_true_f, y_pred_f, smooth = 1e-5):
        intersection = K.sum(y_true_f * y_pred_f)
        return intersection / (K.sum(y_pred_f) + smooth)

    def sensitivity(self, y_true, y_pred):
        ret_sen = 0.0
        for index in range(1, y_true.shape[-1]):
            y_true_f = K.flatten(y_true[:,:,:,:,index])
            y_pred_f = K.flatten(y_pred[:,:,:,:,index])
            ret_sen += self.S(y_true_f, y_pred_f)
        return ret_sen / (y_true.shape[-1] - 1)

    def ppv_cal(self, y_true_f, y_pred_f, smooth = 1e-5):
        intersection = K.sum(y_true_f * y_pred_f)
        return intersection / (K.sum(y_true_f) + smooth)

    def ppv(self, y_true, y_pred):
        ret_ppv = 0.0
        for index in range(1, y_true.shape[-1]):
            y_true_f = K.flatten(y_true[:,:,:,:,index])
            y_pred_f = K.flatten(y_pred[:,:,:,:,index])
            ret_ppv += self.ppv_cal(y_true_f, y_pred_f)
        return ret_ppv / (y_true.shape[-1] - 1)
   