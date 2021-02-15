'''
    File name: detector_utils.py
    Author: [Mochammad F Rahman]
    Date created: / /2019
    Date last modified:  / /2019
    Python Version: >= 3.5
    qoalai version: v0.4
    License: MIT License
    Maintainer: [Mochammad F Rahman]
'''

import cv2
import json
import time
import random
import requests
import numpy as np
import tensorflow as tf
from qoalai.tensor_operations import *
from qoalai.networks.inception_utils import *
from qoalai.networks.inception_v4 import *
from qoalai.networks.resnet_v2 import *
from qoalai.networks.vgg import *
from qoalai.networks.nasnet5 import * 
import qoalai.networks.densenet as densenet
from comdutils.file_utils import *


class ImageRecognition(object):
    def __init__(self,
                 classes, 
                 input_height = 400,
                 input_width = 400, 
                 input_channel = 3):

        """Constructor
        
        Arguments:
            classes {list of string} -- the image classes list

        Keyword Arguments:
            input_height {int} -- the height of input image (default: {512})
            input_width {int} -- the width of input image (default: {512})
            input_channel {int} -- the channel of input image (default: {3})
        """

        self.classes = classes
        self.input_height = input_height
        self.input_width = input_width
        self.input_channel = input_channel

        self.input_placeholder = tf.placeholder(tf.float32, shape=(None, self.input_height, self.input_width, self.input_channel))
        self.output_placeholder = tf.placeholder(tf.float32, shape=(None, len(self.classes)))


    def build_resnetv2(self, 
                       input_tensor,
                       is_training,
                       top_layer_depth = 128): 
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
            is_training {bool} -- [description]
        
        Keyword Arguments:
            top_layer_depth {int} -- [description] (default: {128})
        
        Returns:
            [type] -- [description]
        """
        
        out = None
        with slim.arg_scope(resnet_arg_scope()):
            out, end_points = resnet_v2_101(inputs = input_tensor,
                                            num_classes=1001,
                                            is_training=is_training,
                                            global_pool=True,
                                            output_stride=None,
                                            spatial_squeeze=True,
                                            reuse=None,
                                            scope='resnet_v2_101')
            base_var_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
        
        with tf.variable_scope('resnet_v2_101'):
            depth = out.get_shape().as_list()[-1]
            out = new_fc_layer(out, 
                                num_inputs = depth, 
                                num_outputs = len(self.classes), 
                                name = 'fc1', 
                                dropout_val=1, 
                                activation="NONE",
                                lrelu_alpha=0.2, 
                                data_type=tf.float32,
                                is_training=is_training,
                                use_bias=False)

            if len(self.classes) == 1:
                out = tf.nn.sigmoid(out)
            else:
                out = tf.nn.softmax(out)

        return out, base_var_list


    def build_inceptionv4_basenet(self, 
                                  input_tensor, 
                                  is_training = False, 
                                  final_endpoint='Mixed_7d',
                                  top_layer_depth = 128):
        """Fucntion for creating inception v4 base network
        
        Arguments:
            input_tensor {tensorflow tensor} -- The input tensor
            is_training {bool} -- training or not 
        
        Returns:
            [type] -- [description]
        """
        print ('-------------------------------------------------------')
        print (" NOTICE, your inception v4 base model is end with node:")
        print (final_endpoint)
        print ('-------------------------------------------------------')

        inception_v4_arg_scope = inception_arg_scope
        arg_scope = inception_v4_arg_scope()
        # build inception v4 base graph
        with slim.arg_scope(arg_scope):
            # get output (logits)
            out, end_points = inception_v4(input_tensor, 
                                           num_classes=1, 
                                           final_endpoint=final_endpoint, 
                                           is_training=is_training)
            # get inception variable name
            base_var_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)

        with tf.variable_scope('InceptionV4'):
            size = out.get_shape().as_list()[1]
            while(True):
                if size == 1:
                    break

                out = new_conv2d_layer(out, 
                                    filter_shape=[3, 3, out.get_shape().as_list()[-1], top_layer_depth], 
                                    name='cv1', 
                                    dropout_val=0.85, 
                                    activation = 'LRELU', 
                                    lrelu_alpha=0.2,
                                    padding='SAME', 
                                    strides=[1, 2, 2, 1],
                                    data_type=tf.float32,  
                                    is_training=is_training,
                                    use_bias=True,
                                    use_batchnorm=True) 
                size = out.get_shape().as_list()[1]
            
            depth = out.get_shape().as_list()[-1]
            out = tf.reshape(out, [tf.shape(out)[0], -1])
            out = new_fc_layer(out, 
                                num_inputs = depth, 
                                num_outputs = len(self.classes), 
                                name = 'fc1', 
                                dropout_val=1, 
                                activation="NONE",
                                lrelu_alpha=0.2, 
                                data_type=tf.float32,
                                is_training=is_training,
                                use_bias=False)

            if len(self.classes) == 1:
                out = tf.nn.sigmoid(out)
            else:
                out = tf.nn.softmax(out)
            
            self.out = out
        return out, base_var_list


    def build_densenet_base(self, input_tensor,
                            dropout_rate,
                            is_training,
                            top_layer_depth = 128):
        """[summary]
        
        Arguments:
            input_tensordropout_rate {[type]} -- [description]
            is_training {bool} -- [description]
        """
        arg_scoope = densenet.densenet_arg_scope()
        with slim.arg_scope(arg_scoope):
            out = densenet.densenet121(inputs=input_tensor, 
                                       num_classes=1, 
                                       is_training=is_training)
            base_var_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)

        with tf.variable_scope('densenet121'):
            size = out.get_shape().as_list()[1]
            while(True):
                if size == 1:
                    break

                out = new_conv2d_layer(out, 
                                        filter_shape=[3, 3, out.get_shape().as_list()[-1], top_layer_depth], 
                                        name='cv1', 
                                        dropout_val=0.85, 
                                        activation = 'LRELU', 
                                        lrelu_alpha=0.2,
                                        padding='SAME', 
                                        strides=[1, 2, 2, 1],
                                        data_type=tf.float32,  
                                        is_training=is_training,
                                        use_bias=True,
                                        use_batchnorm=True) 
                size = out.get_shape().as_list()[1]
            
            depth = out.get_shape().as_list()[-1]
            out = tf.reshape(out, [tf.shape(out)[0], -1])
            out = new_fc_layer(out, 
                                num_inputs = depth, 
                                num_outputs = len(self.classes), 
                                name = 'fc1', 
                                dropout_val=1, 
                                activation="NONE",
                                lrelu_alpha=0.2, 
                                data_type=tf.float32,
                                is_training=is_training,
                                use_bias=False)

            if len(self.classes) == 1:
                out = tf.nn.sigmoid(out)
            else:
                out = tf.nn.softmax(out)

            self.out = out
        return out, base_var_list 


    def build_pnasnet_large_base(self, input_tensor,
                                is_training): 

        out, _ = build_pnasnet_large(images=input_tensor,
                                    num_classes = len(self.classes),
                                    is_training=is_training,
                                    final_endpoint=None,
                                    config=None)
        base_var_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES) 
        
        print ("============", out)
        with tf.variable_scope('pnasnet_large'):
            depth = out.get_shape().as_list()[-1]
            out = new_fc_layer(out, 
                                num_inputs = depth, 
                                num_outputs = len(self.classes), 
                                name = 'fc1', 
                                dropout_val=1, 
                                activation="NONE",
                                lrelu_alpha=0.2, 
                                data_type=tf.float32,
                                is_training=is_training,
                                use_bias=False)
            print ('..............', out)
            if len(self.classes) == 1:
                out = tf.nn.sigmoid(out)
            else:
                out = tf.nn.softmax(out)
        return out, base_var_list


    def build_vgg19_base(self, input_tensor,
                            dropout_rate,
                            is_training):
        """[summary]
        
        Arguments:
            input_tensordropout_rate {[type]} -- [description]
            is_training {bool} -- [description]
        """
        arg_scope = vgg_arg_scope()
        with slim.arg_scope(arg_scope):
            out, _ = vgg_19(inputs=input_tensor, 
                        dropout_keep_prob=1. - dropout_rate, 
                        is_training=is_training,
                        spatial_squeeze=False,
                        global_pool=True)
            base_var_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)

        with tf.variable_scope('vgg_19'):
            print ('..............', out)
            depth = out.get_shape().as_list()[-1] * out.get_shape().as_list()[-2] * out.get_shape().as_list()[-3]
            out = tf.reshape(out, [tf.shape(out)[0], -1])
            print ('..............', out, depth)
            out = new_fc_layer(out, 
                                num_inputs = depth, 
                                num_outputs = len(self.classes), 
                                name = 'fc1', 
                                dropout_val=1, 
                                activation="NONE",
                                lrelu_alpha=0.2, 
                                data_type=tf.float32,
                                is_training=is_training,
                                use_bias=False)
            print ('..............', out)
            if len(self.classes) == 1:
                out = tf.nn.sigmoid(out)
            else:
                out = tf.nn.softmax(out)

        return out, base_var_list
        

    def batch_generator(self, batch_size, dataset_path, message):
        """Train Generator
        
        Arguments:
            batch_size {integer} -- the size of the batch
            image_name_list {list of string} -- the list of image name
        """
        file_list_by_class = {}
        idx = {}
        for i in self.classes:
            file_list_by_class[i] = get_filenames(dataset_path + i)
            random.shuffle(file_list_by_class[i])
            idx[i] = 0
        
        perclass_sample = int(batch_size/len(self.classes))

        print ("------------------------INFO IMAGES-------------------")
        print ("Image Folder: " + dataset_path)
        for i in self.classes:
            print ("Number of Image in " + str(i) + ": ", len(file_list_by_class[i]))
        print ("------------------------------------------------------")

        # Infinite loop.
        while True:
            x_batch = []
            y_pred = []

            for i in self.classes:
                for j in range(perclass_sample):
                    if idx[i] >= len(file_list_by_class[i]):
                        random.shuffle(file_list_by_class[i])
                        print ("==>>> INFO: your " + message + " in class " + str(i) + " dataset is reshuffled again", idx[i])
                        idx[i] = 0
                    try:
                        tmp_x = cv2.imread(dataset_path + i + "/" + file_list_by_class[i][idx[i]])
                        tmp_x = cv2.cvtColor(tmp_x, cv2.COLOR_BGR2RGB)
                        tmp_x = cv2.resize(tmp_x, dsize=(self.input_width, self.input_height), interpolation=cv2.INTER_CUBIC)
                        tmp_x = tmp_x.astype(np.float32) / 255.
                        tmp_y = np.zeros((len(self.classes))).astype(np.float32)
                        tmp_y[self.classes.index(i)] = 1.
                        x_batch.append(tmp_x)
                        y_pred.append(tmp_y)

                    except Exception as e:
                        print ("-----------------------------------------------------------------------------")
                        print ('>>> WARNING: fail when handling ' +  file_list_by_class[i][idx[i]], e)
                        print ("-----------------------------------------------------------------------------")
                    
                    idx[i] += 1

            c = list(zip(x_batch, y_pred))
            random.shuffle(c)
            x_batch, y_pred = zip(*c)
            yield (np.array(x_batch), np.array(y_pred))


    def send_report(self, 
                    report_id, 
                    part_name,
                    report_endpoint): 
        report_payload = {}
        report_payload['task'] = 'report'
        report_payload['id'] = report_id
        report_payload['name'] = part_name
        report_payload['train_loss'] = round(self.train_loss[-1], 3)
        report_payload['train_acc'] = round(self.train_acc[-1], 3)
        report_payload['train_recall'] = '-'
        report_payload['train_precision'] =  '-'
        report_payload['train_f1'] = '-'
        report_payload['val_loss'] = round(self.val_loss[-1], 3)
        report_payload['val_acc'] = round(self.val_acc[-1], 3)
        report_payload['val_recall'] = round(self.val_recall[-1], 3)
        report_payload['val_precision'] = round(self.val_precision[-1], 3)
        report_payload['val_f1'] = round(self.val_f1[-1], 3)
        report_payload['running_time'] = self.total_time
        report_payload['cost'] = self.total_cost

        r = requests.post(report_endpoint, json=report_payload)
        print ("Report status code: ", r.status_code)

    

    def optimize(self, 
                 iteration, 
                 subdivition,
                 cost_tensor,
                 optimizer_tensor,
                 out_tensor, 
                 session,
                 saver, 
                 train_generator,
                 val_generator,
                 best_loss,
                 path_tosave_model='model/model1',
                 report_mode=False,
                 report_endpoint=None, 
                 report_payload=None,
                 report_id='0',
                 part_name='test'):
        """[summary]
        
        Arguments:
            iteration {[type]} -- [description]
            subdivition {[type]} -- [description]
            cost_tensor {[type]} -- [description]
            optimizer_tensor {[type]} -- [description]
            out_tensor {[type]} -- [description]
        
        Keyword Arguments:
            train_batch_size {int} -- [description] (default: {32})
            val_batch_size {int} -- [description] (default: {50})
            path_tosave_model {str} -- [description] (default: {'model/model1'})
        """
        from sklearn.metrics import accuracy_score
        start = time.time()

        self.train_loss = []
        self.val_loss = []
        self.train_acc = []
        self.val_acc = []
        self.val_recall = []
        self.val_precision = [] 
        self.val_f1 = []
        best_loss = best_loss
        best_f1 = 0.
        
        for i in range(iteration):
            sign = "-"
            t_losses = []
            t_accs = []

            for j in range(subdivition):
                x_train, y_train = next(train_generator)
                feed_dict = {}
                feed_dict[self.input_placeholder] = x_train
                feed_dict[self.output_placeholder] = y_train
                session.run(optimizer_tensor, feed_dict)
                loss = session.run(cost_tensor, feed_dict)
                t_losses.append(loss)

                t_out = session.run(out_tensor, feed_dict)
                t_out = np.argmax(t_out, axis=1)
                y_train =  np.argmax(y_train, axis=1)
                acc = accuracy_score(t_out, y_train)
                t_accs.append(acc)
                print ("> Train sub", j, 'loss : ', loss, 'acc: ', acc)
                
            x_val, y_val = next(val_generator)
            feed_dict = {}
            feed_dict[self.input_placeholder] = x_val
            feed_dict[self.output_placeholder] = y_val
            loss = session.run(cost_tensor, feed_dict)

            val_out = session.run(out_tensor, feed_dict)
            val_out = np.argmax(val_out, axis=1)
            y_val =  np.argmax(y_val, axis=1)
            val_acc = accuracy_score(val_out, y_val)

            t_loss = sum(t_losses) / (len(t_losses) + 0.0001)
            t_acc = sum(t_accs) / (len(t_accs) + 0.0001)
            self.train_loss.append(t_loss)
            self.val_loss.append(loss)
            self.train_acc.append(t_acc)
            self.val_acc.append(val_acc)

            tp = np.sum(val_out * y_val)
            fp = np.sum(np.absolute(val_out - y_val) * np.absolute(y_val-1))
            fn = np.sum(np.absolute(np.absolute(val_out - 1) - np.absolute(y_val -1)) * y_val)
            precision = float(tp /(tp + fp + 0.001))
            recall = float(tp /(tp + fn + 0.001))
            f1 = float(2 * precision * recal /(precision + recal + 0.001))
            self.val_precision.append(precision)
            self.val_recall.append(recall)
            self.val_f1.append(f1)
                
            if best_f1 < f1:
                best_f1 = f1
                sign = "************* model saved based on f1"
                saver.save(session, path_tosave_model)
        
            print (">> epoch: ", i, "train loss: ", round(t_loss, 3), "val loss: ", round(loss, 3), "train acc: ", round(t_acc, 3), "val acc: ", round(val_acc, 3), sign)
            print ("            precision: {}, recall: {}, f1: {}".format(precision, recall, f1))
            
            if report_mode and report_endpoint != None: 
                self.total_time = None 
                self.total_cost = None
                self.send_report(report_id, part_name)
                    




    
